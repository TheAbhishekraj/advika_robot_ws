#!/bin/bash
# Advika 3.0 -- Auto-Start Daemon Services
# Run this script on boot via systemd or cron to start all robot services

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="/var/log/advika"
PID_DIR="/var/run/advika"

# Create directories
mkdir -p "$LOG_DIR" "$PID_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}  Advika 3.0 Robot Launch Script     ${NC}"
echo -e "${GREEN}=====================================${NC}"
echo ""

# Function to start a service in background
start_service() {
    local name=$1
    local cmd=$2
    local log_file=$3

    echo -e "${YELLOW}Starting $name...${NC}"

    nohup $cmd >> "$log_file" 2>&1 &
    local pid=$!
    echo $pid > "$PID_DIR/${name}.pid"

    sleep 2

    if kill -0 $pid 2>/dev/null; then
        echo -e "${GREEN}  $name started (PID: $pid)${NC}"
    else
        echo -e "${RED}  $name failed to start!${NC}"
        return 1
    fi
}

# Function to stop a service
stop_service() {
    local name=$1
    local pid_file="$PID_DIR/${name}.pid"

    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 $pid 2>/dev/null; then
            echo -e "${YELLOW}Stopping $name (PID: $pid)...${NC}"
            kill $pid
            rm "$pid_file"
            echo -e "${GREEN}  $name stopped${NC}"
        else
            echo -e "${YELLOW}  $name not running${NC}"
            rm -f "$pid_file"
        fi
    else
        echo -e "${YELLOW}  $name PID file not found${NC}"
    fi
}

# Parse command
case "${1:-start}" in
    start)
        echo "Starting Advika 3.0 services..."
        echo ""

        # 1. Start Hardware Bridge MCP Server
        start_service "hardware_bridge"             "python3 $WORKSPACE_DIR/mcp_servers/hardware_bridge.py"             "$LOG_DIR/hardware_bridge.log"

        # 2. Start Vision Bridge MCP Server
        start_service "vision_bridge"             "python3 $WORKSPACE_DIR/mcp_servers/vision_bridge.py"             "$LOG_DIR/vision_bridge.log"

        # 3. Start ROS2 Navigation (if available)
        if command -v ros2 &> /dev/null; then
            start_service "ros2_navigation"                 "bash -c 'source /opt/ros/jazzy/setup.bash && ros2 launch nav2_bringup navigation_launch.py'"                 "$LOG_DIR/ros2_navigation.log"
        else
            echo -e "${YELLOW}  ROS2 not found, skipping navigation stack${NC}"
        fi

        echo ""
        echo -e "${GREEN}All services started successfully!${NC}"
        echo "Logs: $LOG_DIR/"
        echo "PIDs: $PID_DIR/"
        ;;

    stop)
        echo "Stopping Advika 3.0 services..."
        echo ""

        stop_service "hardware_bridge"
        stop_service "vision_bridge"
        stop_service "ros2_navigation"

        echo ""
        echo -e "${GREEN}All services stopped.${NC}"
        ;;

    restart)
        $0 stop
        sleep 2
        $0 start
        ;;

    status)
        echo "Advika 3.0 Service Status:"
        echo ""

        for service in hardware_bridge vision_bridge ros2_navigation; do
            local pid_file="$PID_DIR/${service}.pid"
            if [ -f "$pid_file" ]; then
                local pid=$(cat "$pid_file")
                if kill -0 $pid 2>/dev/null; then
                    echo -e "${GREEN}  $service: RUNNING (PID: $pid)${NC}"
                else
                    echo -e "${RED}  $service: DEAD (PID file exists)${NC}"
                fi
            else
                echo -e "${YELLOW}  $service: STOPPED${NC}"
            fi
        done
        ;;

    test)
        echo "Running hardware diagnostic pipeline..."
        python3 "$WORKSPACE_DIR/scripts/test_peripherals.py"
        ;;

    *)
        echo "Usage: $0 {start|stop|restart|status|test}"
        exit 1
        ;;
esac
