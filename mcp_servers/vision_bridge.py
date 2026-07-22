#!/usr/bin/env python3
"""
Advika 3.0 -- Vision Bridge MCP Server
FastMCP server for dual-camera frame capture, stitching, and object detection.
Uses OpenCV for image processing and YOLO for object detection.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

import cv2
import numpy as np
from fastmcp import FastMCP

# -- Logging Setup --
LOG_DIR = Path("/var/log/advika")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "vision_bridge.log")
    ]
)
logger = logging.getLogger("advika.vision_bridge")

# -- Configuration --
HORIZON_CAM = os.getenv("HORIZON_CAM", "/dev/video0")
FLOOR_CAM = os.getenv("FLOOR_CAM", "/dev/video2")
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", "640"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", "480"))
FPS = int(os.getenv("FPS", "30"))

# YOLO model path (download from Ultralytics or use custom)
YOLO_MODEL_PATH = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")

# -- Camera State --
horizon_cap: Optional[cv2.VideoCapture] = None
floor_cap: Optional[cv2.VideoCapture] = None
yolo_model = None

# -- MCP Server --
mcp = FastMCP("advika_vision_bridge")

# -- Data Classes --
@dataclass
class DetectedObject:
    class_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, w, h
    center: Tuple[int, int]
    distance_estimate_m: Optional[float] = None

# -- Camera Helpers --
def _init_cameras() -> bool:
    """Initialize both camera captures."""
    global horizon_cap, floor_cap

    try:
        if horizon_cap is None or not horizon_cap.isOpened():
            horizon_cap = cv2.VideoCapture(HORIZON_CAM, cv2.CAP_V4L2)
            horizon_cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            horizon_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            horizon_cap.set(cv2.CAP_PROP_FPS, FPS)
            logger.info(f"Horizon camera opened on {HORIZON_CAM}")

        if floor_cap is None or not floor_cap.isOpened():
            floor_cap = cv2.VideoCapture(FLOOR_CAM, cv2.CAP_V4L2)
            floor_cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            floor_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
            floor_cap.set(cv2.CAP_PROP_FPS, FPS)
            logger.info(f"Floor camera opened on {FLOOR_CAM}")

        return True
    except Exception as e:
        logger.error(f"Camera init failed: {e}")
        return False

def _release_cameras():
    """Release camera resources."""
    global horizon_cap, floor_cap
    if horizon_cap:
        horizon_cap.release()
        horizon_cap = None
    if floor_cap:
        floor_cap.release()
        floor_cap = None

def _capture_frame(cap: cv2.VideoCapture) -> Optional[np.ndarray]:
    """Capture a single frame from a camera."""
    if cap is None or not cap.isOpened():
        return None

    ret, frame = cap.read()
    if not ret:
        logger.warning("Frame capture failed")
        return None
    return frame

def _stitch_frames(horizon_frame: np.ndarray, floor_frame: np.ndarray) -> np.ndarray:
    """
    Stitch horizon and floor frames into a unified view.
    Horizon on top, floor on bottom with perspective correction.
    """
    # Resize to consistent dimensions
    h_w, h_h = FRAME_WIDTH, FRAME_HEIGHT
    f_w, f_h = FRAME_WIDTH, FRAME_HEIGHT

    horizon_resized = cv2.resize(horizon_frame, (h_w, h_h))
    floor_resized = cv2.resize(floor_frame, (f_w, f_h))

    # Apply perspective transform to floor camera for bird's eye view
    # Define source and destination points for floor perspective correction
    src_pts = np.float32([
        [0, 0],
        [f_w, 0],
        [f_w, f_h],
        [0, f_h]
    ])
    dst_pts = np.float32([
        [int(f_w * 0.2), 0],
        [int(f_w * 0.8), 0],
        [f_w, f_h],
        [0, f_h]
    ])

    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    floor_warped = cv2.warpPerspective(floor_resized, M, (f_w, f_h))

    # Stack vertically: horizon on top, floor on bottom
    stitched = np.vstack([horizon_resized, floor_warped])

    # Add divider line
    cv2.line(stitched, (0, h_h), (h_w, h_h), (0, 255, 0), 2)

    return stitched

def _init_yolo() -> bool:
    """Initialize YOLO object detection model."""
    global yolo_model

    try:
        from ultralytics import YOLO
        yolo_model = YOLO(YOLO_MODEL_PATH)
        logger.info(f"YOLO model loaded: {YOLO_MODEL_PATH}")
        return True
    except ImportError:
        logger.warning("Ultralytics not installed. Object detection disabled.")
        return False
    except Exception as e:
        logger.error(f"YOLO init failed: {e}")
        return False

def _detect_objects(frame: np.ndarray) -> List[DetectedObject]:
    """Run YOLO object detection on a frame."""
    if yolo_model is None:
        if not _init_yolo():
            return []

    results = yolo_model(frame, verbose=False)
    detections = []

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            cls_name = result.names[cls_id]

            # Estimate distance based on apparent object size
            # Simple heuristic: larger objects are closer
            bbox_area = (x2 - x1) * (y2 - y1)
            frame_area = FRAME_WIDTH * FRAME_HEIGHT
            size_ratio = bbox_area / frame_area

            # Rough distance estimate (calibrated for typical indoor objects)
            if size_ratio > 0.3:
                dist = 0.3
            elif size_ratio > 0.1:
                dist = 0.6
            elif size_ratio > 0.05:
                dist = 1.0
            elif size_ratio > 0.02:
                dist = 2.0
            else:
                dist = 3.0

            detections.append(DetectedObject(
                class_name=cls_name,
                confidence=round(conf, 3),
                bbox=(x1, y1, x2 - x1, y2 - y1),
                center=((x1 + x2) // 2, (y1 + y2) // 2),
                distance_estimate_m=round(dist, 2)
            ))

    return detections

def _annotate_frame(frame: np.ndarray, detections: List[DetectedObject]) -> np.ndarray:
    """Draw bounding boxes and labels on frame."""
    annotated = frame.copy()

    for det in detections:
        x, y, w, h = det.bbox
        cx, cy = det.center

        # Draw bounding box
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw label
        label = f"{det.class_name} {det.confidence:.2f}"
        if det.distance_estimate_m:
            label += f" @{det.distance_estimate_m}m"

        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        cv2.rectangle(annotated, (x, y - label_size[1] - 10), 
                     (x + label_size[0], y), (0, 255, 0), -1)
        cv2.putText(annotated, label, (x, y - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

        # Draw center point
        cv2.circle(annotated, (cx, cy), 3, (0, 0, 255), -1)

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    cv2.putText(annotated, timestamp, (10, 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return annotated

def _frame_to_base64(frame: np.ndarray, quality: int = 85) -> str:
    """Encode frame as base64 JPEG string."""
    import base64

    encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    _, buffer = cv2.imencode('.jpg', frame, encode_params)
    return base64.b64encode(buffer).decode('utf-8')

# -- MCP Tools --

@mcp.tool()
def mcp_capture_stitched_frame(annotate: bool = True, detect_objects: bool = True) -> Dict[str, Any]:
    """
    Capture and stitch dual-camera frames into a unified view.

    Args:
        annotate: Draw bounding boxes and labels on detected objects
        detect_objects: Run YOLO object detection

    Returns:
        Stitched frame as base64 JPEG and detection metadata
    """
    if not _init_cameras():
        return {
            "status": "error",
            "error": "Failed to initialize cameras"
        }

    # Capture frames
    horizon_frame = _capture_frame(horizon_cap)
    floor_frame = _capture_frame(floor_cap)

    if horizon_frame is None or floor_frame is None:
        return {
            "status": "error",
            "error": "Frame capture failed"
        }

    # Stitch frames
    stitched = _stitch_frames(horizon_frame, floor_frame)

    # Object detection
    detections = []
    if detect_objects:
        detections = _detect_objects(horizon_frame)

        if annotate:
            stitched = _annotate_frame(stitched, detections)

    # Encode to base64
    frame_b64 = _frame_to_base64(stitched)

    # Build detection metadata
    detection_meta = []
    for det in detections:
        detection_meta.append({
            "class": det.class_name,
            "confidence": det.confidence,
            "bbox": det.bbox,
            "center": det.center,
            "distance_estimate_m": det.distance_estimate_m
        })

    logger.info(f"Captured stitched frame. Detections: {len(detections)}")

    return {
        "status": "success",
        "frame_base64": frame_b64,
        "frame_dimensions": {
            "width": stitched.shape[1],
            "height": stitched.shape[0]
        },
        "detections": detection_meta,
        "detection_count": len(detections),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@mcp.tool()
def mcp_capture_single_camera(camera: str = "horizon", annotate: bool = True) -> Dict[str, Any]:
    """
    Capture a single camera frame.

    Args:
        camera: Which camera to use ("horizon" or "floor")
        annotate: Draw detection annotations

    Returns:
        Frame as base64 JPEG and detection metadata
    """
    if not _init_cameras():
        return {"status": "error", "error": "Failed to initialize cameras"}

    cap = horizon_cap if camera == "horizon" else floor_cap
    frame = _capture_frame(cap)

    if frame is None:
        return {"status": "error", "error": "Frame capture failed"}

    detections = _detect_objects(frame) if annotate else []

    if annotate and detections:
        frame = _annotate_frame(frame, detections)

    frame_b64 = _frame_to_base64(frame)

    return {
        "status": "success",
        "camera": camera,
        "frame_base64": frame_b64,
        "detections": [
            {
                "class": d.class_name,
                "confidence": d.confidence,
                "bbox": d.bbox,
                "center": d.center,
                "distance_estimate_m": d.distance_estimate_m
            } for d in detections
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@mcp.tool()
def mcp_find_object(target_class: str, confidence_threshold: float = 0.5) -> Dict[str, Any]:
    """
    Search for a specific object class in the current camera view.

    Args:
        target_class: Object class name to search for (e.g., "person", "chair", "bottle")
        confidence_threshold: Minimum confidence score (0.0 to 1.0)

    Returns:
        Object location, distance estimate, and bounding box
    """
    result = mcp_capture_stitched_frame(annotate=True, detect_objects=True)

    if result["status"] != "success":
        return result

    matches = [
        d for d in result["detections"]
        if d["class"].lower() == target_class.lower() 
        and d["confidence"] >= confidence_threshold
    ]

    if not matches:
        return {
            "status": "not_found",
            "target_class": target_class,
            "message": f"No {target_class} detected above confidence {confidence_threshold}",
            "all_detections": result["detections"]
        }

    # Return the highest confidence match
    best_match = max(matches, key=lambda x: x["confidence"])

    # Calculate angular offset from center
    frame_center_x = FRAME_WIDTH // 2
    object_center_x = best_match["center"][0]
    angular_offset_deg = ((object_center_x - frame_center_x) / FRAME_WIDTH) * 75  # 75deg FOV

    logger.info(f"Found {target_class}: confidence={best_match['confidence']}, "
               f"distance={best_match['distance_estimate_m']}m, offset={angular_offset_deg:.1f}deg")

    return {
        "status": "found",
        "target_class": target_class,
        "match": best_match,
        "angular_offset_deg": round(angular_offset_deg, 1),
        "frame_base64": result["frame_base64"]
    }

@mcp.tool()
def mcp_set_camera_settings(brightness: int = None, contrast: int = None, 
                           saturation: int = None, exposure: int = None) -> Dict[str, Any]:
    """
    Adjust camera settings.

    Args:
        brightness: Brightness value (-64 to 64)
        contrast: Contrast value (-64 to 64)
        saturation: Saturation value (-64 to 64)
        exposure: Exposure value (0 to 10000)

    Returns:
        Updated camera settings
    """
    if not _init_cameras():
        return {"status": "error", "error": "Failed to initialize cameras"}

    settings = {}

    for cap, name in [(horizon_cap, "horizon"), (floor_cap, "floor")]:
        if brightness is not None:
            cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        if contrast is not None:
            cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        if saturation is not None:
            cap.set(cv2.CAP_PROP_SATURATION, saturation)
        if exposure is not None:
            cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

        settings[name] = {
            "brightness": cap.get(cv2.CAP_PROP_BRIGHTNESS),
            "contrast": cap.get(cv2.CAP_PROP_CONTRAST),
            "saturation": cap.get(cv2.CAP_PROP_SATURATION),
            "exposure": cap.get(cv2.CAP_PROP_EXPOSURE)
        }

    return {"status": "success", "settings": settings}

# -- Main Entry Point --
if __name__ == "__main__":
    logger.info("Starting Advika 3.0 Vision Bridge MCP Server...")

    if not _init_cameras():
        logger.warning("Camera initialization failed. Running in simulation mode.")

    mcp.run()
