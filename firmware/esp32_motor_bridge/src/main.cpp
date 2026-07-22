/**
 * Advika 3.0 — ESP32 Motor Bridge
 * Dual PID wheel control with encoder feedback
 * Communicates with Pi via UART using JSON-RPC 2.0 (MCP protocol)
 */

#include <Arduino.h>
#include <PID_v1.h>
#include <Encoder.h>
#include <ArduinoJson.h>

// ─── Pin Definitions ─────────────────────────────────────────────────
// Left Motor
#define LEFT_PWM_PIN    4
#define LEFT_DIR_PIN1   5
#define LEFT_DIR_PIN2   6
#define LEFT_ENC_A      7
#define LEFT_ENC_B      8

// Right Motor
#define RIGHT_PWM_PIN   9
#define RIGHT_DIR_PIN1  10
#define RIGHT_DIR_PIN2  11
#define RIGHT_ENC_A     12
#define RIGHT_ENC_B     13

// Status LED
#define LED_PIN         2

// E-Stop input
#define ESTOP_PIN       14

// ─── Constants ────────────────────────────────────────────────────────
#define PWM_FREQ        20000
#define PWM_RESOLUTION  8
#define PWM_MAX         255
#define ENCODER_PPR     334
#define GEAR_RATIO      34.0
#define WHEEL_DIAMETER  0.065  // meters
#define WHEEL_BASE      0.20   // meters
#define MAX_RPM         170.0
#define SAMPLE_TIME_MS  10

// ─── Global Variables ─────────────────────────────────────────────────
Encoder leftEncoder(LEFT_ENC_A, LEFT_ENC_B);
Encoder rightEncoder(RIGHT_ENC_A, RIGHT_ENC_B);

// PID variables
double leftSetpoint = 0, leftInput = 0, leftOutput = 0;
double rightSetpoint = 0, rightInput = 0, rightOutput = 0;

// PID tuning (loaded from config or defaults)
double Kp = 2.0, Ki = 0.5, Kd = 0.1;

PID leftPID(&leftInput, &leftOutput, &leftSetpoint, Kp, Ki, Kd, DIRECT);
PID rightPID(&rightInput, &rightOutput, &rightSetpoint, Kp, Ki, Kd, DIRECT);

// Encoder state
long lastLeftCount = 0;
long lastRightCount = 0;
unsigned long lastSampleTime = 0;

// Safety state
bool eStopActive = false;
bool motorsEnabled = true;

// ─── Function Prototypes ──────────────────────────────────────────────
void setupMotors();
void setupPID();
void handleSerial();
void processCommand(JsonDocument& doc);
void setMotorSpeeds(double leftVel, double rightVel);
void updateEncoders();
void checkEStop();
void sendTelemetry();
void sendError(const char* message, int id = -1);
void sendResult(JsonDocument& result, int id);

// ─── Setup ────────────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    delay(1000);

    pinMode(LED_PIN, OUTPUT);
    pinMode(ESTOP_PIN, INPUT_PULLUP);

    setupMotors();
    setupPID();

    digitalWrite(LED_PIN, HIGH);
    Serial.println("{\"jsonrpc\":\"2.0\",\"method\":\"initialized\",\"params\":{\"status\":\"ready\"}}");
}

// ─── Main Loop ────────────────────────────────────────────────────────
void loop() {
    unsigned long now = millis();

    // Check E-Stop every loop
    checkEStop();

    // Handle incoming serial commands
    handleSerial();

    // PID update at fixed interval
    if (now - lastSampleTime >= SAMPLE_TIME_MS) {
        updateEncoders();

        if (motorsEnabled && !eStopActive) {
            leftPID.Compute();
            rightPID.Compute();

            // Apply PID outputs to motors
            int leftPWM = constrain((int)leftOutput, -PWM_MAX, PWM_MAX);
            int rightPWM = constrain((int)rightOutput, -PWM_MAX, PWM_MAX);

            setMotorSpeeds(leftPWM, rightPWM);
        } else {
            setMotorSpeeds(0, 0);
        }

        lastSampleTime = now;
    }
}

// ─── Motor Setup ──────────────────────────────────────────────────────
void setupMotors() {
    pinMode(LEFT_PWM_PIN, OUTPUT);
    pinMode(LEFT_DIR_PIN1, OUTPUT);
    pinMode(LEFT_DIR_PIN2, OUTPUT);
    pinMode(RIGHT_PWM_PIN, OUTPUT);
    pinMode(RIGHT_DIR_PIN1, OUTPUT);
    pinMode(RIGHT_DIR_PIN2, OUTPUT);

    ledcAttach(LEFT_PWM_PIN, PWM_FREQ, PWM_RESOLUTION);
    ledcAttach(RIGHT_PWM_PIN, PWM_FREQ, PWM_RESOLUTION);

    setMotorSpeeds(0, 0);
}

// ─── PID Setup ────────────────────────────────────────────────────────
void setupPID() {
    leftPID.SetMode(AUTOMATIC);
    leftPID.SetOutputLimits(-PWM_MAX, PWM_MAX);
    leftPID.SetSampleTime(SAMPLE_TIME_MS);

    rightPID.SetMode(AUTOMATIC);
    rightPID.SetOutputLimits(-PWM_MAX, PWM_MAX);
    rightPID.SetSampleTime(SAMPLE_TIME_MS);
}

// ─── Serial Command Handler ───────────────────────────────────────────
void handleSerial() {
    static String buffer = "";

    while (Serial.available()) {
        char c = Serial.read();
        buffer += c;

        if (c == '\\n') {
            JsonDocument doc;
            DeserializationError error = deserializeJson(doc, buffer);

            if (!error) {
                processCommand(doc);
            } else {
                sendError("Invalid JSON");
            }

            buffer = "";
        }
    }
}

// ─── Command Processor ────────────────────────────────────────────────
void processCommand(JsonDocument& doc) {
    const char* method = doc["method"] | "";
    int id = doc["id"] | -1;

    if (strcmp(method, "drive") == 0) {
        // Parse drive command: linear_velocity (m/s), angular_velocity (rad/s), duration_ms
        double linear = doc["params"]["linear_velocity"] | 0.0;
        double angular = doc["params"]["angular_velocity"] | 0.0;
        int duration = doc["params"]["duration_ms"] | 0;

        // Clamp values
        linear = constrain(linear, -1.0, 1.0);
        angular = constrain(angular, -1.0, 1.0);
        duration = constrain(duration, 0, 2000);

        // Differential drive kinematics
        double leftVel = linear - (angular * WHEEL_BASE / 2.0);
        double rightVel = linear + (angular * WHEEL_BASE / 2.0);

        // Convert to encoder counts per sample (rough approximation)
        double countsPerMeter = (ENCODER_PPR * GEAR_RATIO) / (PI * WHEEL_DIAMETER);
        double sampleTimeSec = SAMPLE_TIME_MS / 1000.0;

        leftSetpoint = leftVel * countsPerMeter * sampleTimeSec;
        rightSetpoint = rightVel * countsPerMeter * sampleTimeSec;

        JsonDocument result;
        result["status"] = "accepted";
        result["left_target"] = leftSetpoint;
        result["right_target"] = rightSetpoint;
        result["duration_ms"] = duration;
        sendResult(result, id);

    } else if (strcmp(method, "stop") == 0) {
        leftSetpoint = 0;
        rightSetpoint = 0;
        setMotorSpeeds(0, 0);

        JsonDocument result;
        result["status"] = "stopped";
        sendResult(result, id);

    } else if (strcmp(method, "get_telemetry") == 0) {
        sendTelemetry();

    } else if (strcmp(method, "set_pid") == 0) {
        Kp = doc["params"]["kp"] | Kp;
        Ki = doc["params"]["ki"] | Ki;
        Kd = doc["params"]["kd"] | Kd;

        leftPID.SetTunings(Kp, Ki, Kd);
        rightPID.SetTunings(Kp, Ki, Kd);

        JsonDocument result;
        result["status"] = "pid_updated";
        result["kp"] = Kp;
        result["ki"] = Ki;
        result["kd"] = Kd;
        sendResult(result, id);

    } else if (strcmp(method, "reset_encoders") == 0) {
        leftEncoder.write(0);
        rightEncoder.write(0);
        lastLeftCount = 0;
        lastRightCount = 0;

        JsonDocument result;
        result["status"] = "encoders_reset";
        sendResult(result, id);

    } else {
        sendError("Unknown method", id);
    }
}

// ─── Set Motor Speeds ─────────────────────────────────────────────────
void setMotorSpeeds(double leftPWM, double rightPWM) {
    // Left motor direction
    if (leftPWM >= 0) {
        digitalWrite(LEFT_DIR_PIN1, HIGH);
        digitalWrite(LEFT_DIR_PIN2, LOW);
    } else {
        digitalWrite(LEFT_DIR_PIN1, LOW);
        digitalWrite(LEFT_DIR_PIN2, HIGH);
        leftPWM = -leftPWM;
    }

    // Right motor direction (reversed for differential drive)
    if (rightPWM >= 0) {
        digitalWrite(RIGHT_DIR_PIN1, LOW);
        digitalWrite(RIGHT_DIR_PIN2, HIGH);
    } else {
        digitalWrite(RIGHT_DIR_PIN1, HIGH);
        digitalWrite(RIGHT_DIR_PIN2, LOW);
        rightPWM = -rightPWM;
    }

    ledcWrite(LEFT_PWM_PIN, (int)leftPWM);
    ledcWrite(RIGHT_PWM_PIN, (int)rightPWM);
}

// ─── Update Encoders ──────────────────────────────────────────────────
void updateEncoders() {
    long currentLeft = leftEncoder.read();
    long currentRight = rightEncoder.read();

    leftInput = (double)(currentLeft - lastLeftCount);
    rightInput = (double)(currentRight - lastRightCount);

    lastLeftCount = currentLeft;
    lastRightCount = currentRight;
}

// ─── Check E-Stop ─────────────────────────────────────────────────────
void checkEStop() {
    bool estopPressed = (digitalRead(ESTOP_PIN) == LOW);

    if (estopPressed && !eStopActive) {
        eStopActive = true;
        motorsEnabled = false;
        leftSetpoint = 0;
        rightSetpoint = 0;
        setMotorSpeeds(0, 0);
        digitalWrite(LED_PIN, LOW);

        Serial.println("{\"jsonrpc\":\"2.0\",\"method\":\"estop_triggered\"}");
    } else if (!estopPressed && eStopActive) {
        eStopActive = false;
        motorsEnabled = true;
        digitalWrite(LED_PIN, HIGH);

        Serial.println("{\"jsonrpc\":\"2.0\",\"method\":\"estop_released\"}");
    }
}

// ─── Send Telemetry ───────────────────────────────────────────────────
void sendTelemetry() {
    JsonDocument doc;
    doc["jsonrpc"] = "2.0";
    doc["method"] = "telemetry";

    JsonObject params = doc["params"].to<JsonObject>();
    params["left_encoder"] = leftEncoder.read();
    params["right_encoder"] = rightEncoder.read();
    params["left_velocity"] = leftInput;
    params["right_velocity"] = rightInput;
    params["left_pwm"] = leftOutput;
    params["right_pwm"] = rightOutput;
    params["estop_active"] = eStopActive;
    params["motors_enabled"] = motorsEnabled;
    params["uptime_ms"] = millis();

    serializeJson(doc, Serial);
    Serial.println();
}

// ─── Send JSON-RPC Result ─────────────────────────────────────────────
void sendResult(JsonDocument& result, int id) {
    JsonDocument doc;
    doc["jsonrpc"] = "2.0";
    doc["id"] = id;
    doc["result"] = result;

    serializeJson(doc, Serial);
    Serial.println();
}

// ─── Send JSON-RPC Error ──────────────────────────────────────────────
void sendError(const char* message, int id) {
    JsonDocument doc;
    doc["jsonrpc"] = "2.0";
    if (id >= 0) doc["id"] = id;

    JsonObject error = doc["error"].to<JsonObject>();
    error["code"] = -32600;
    error["message"] = message;

    serializeJson(doc, Serial);
    Serial.println();
}
