/**
 * Advika 3.0 — Hardware Safety Interrupt
 * Sub-millisecond emergency stop with hardware-level motor cutoff
 * 
 * This module uses ESP32's GPIO interrupt and hardware timer for
 * ultra-fast (< 1ms) response to collision or user E-Stop events.
 */

#ifndef SAFETY_INTERRUPT_H
#define SAFETY_INTERRUPT_H

#include <Arduino.h>
#include <driver/gpio.h>
#include <driver/timer.h>

// ─── Safety Configuration ─────────────────────────────────────────────
#define SAFETY_WATCHDOG_INTERVAL_US   500   // 500us watchdog check
#define SAFETY_DEBOUNCE_MS            50    // 50ms debounce for E-Stop
#define SAFETY_MAX_NO_HEARTBEAT_MS    500   // 500ms max without heartbeat

// ─── Pin Definitions (must match main.cpp) ────────────────────────────
#define ESTOP_PIN                     14
#define LEFT_PWM_PIN                  4
#define RIGHT_PWM_PIN                 9
#define LEFT_DIR_PIN1                 5
#define LEFT_DIR_PIN2                 6
#define RIGHT_DIR_PIN1                10
#define RIGHT_DIR_PIN2                11
#define STATUS_LED_PIN                2
#define BUZZER_PIN                    15

// ─── Safety State ─────────────────────────────────────────────────────
volatile bool safety_estop_triggered = false;
volatile bool safety_watchdog_expired = false;
volatile unsigned long last_heartbeat_ms = 0;
volatile unsigned long estop_debounce_start = 0;

// ─── Forward Declarations ─────────────────────────────────────────────
void IRAM_ATTR safety_estop_isr(void* arg);
void IRAM_ATTR safety_watchdog_isr(void* arg);
void safety_init_interrupts();
void safety_init_watchdog();
void safety_feed_heartbeat();
bool safety_is_active();
void safety_hard_stop();
void safety_soft_stop();

// ─── E-Stop ISR (GPIO Interrupt) ──────────────────────────────────────
void IRAM_ATTR safety_estop_isr(void* arg) {
    // Debounce: ignore rapid toggles
    unsigned long now = millis();
    if ((now - estop_debounce_start) < SAFETY_DEBOUNCE_MS) {
        return;
    }
    estop_debounce_start = now;

    // Check pin state (active LOW with pull-up)
    if (gpio_get_level((gpio_num_t)ESTOP_PIN) == 0) {
        safety_estop_triggered = true;
        safety_hard_stop();
    }
}

// ─── Watchdog Timer ISR ───────────────────────────────────────────────
void IRAM_ATTR safety_watchdog_isr(void* arg) {
    unsigned long now = millis();

    // If no heartbeat received within timeout, trigger emergency stop
    if ((now - last_heartbeat_ms) > SAFETY_MAX_NO_HEARTBEAT_MS) {
        safety_watchdog_expired = true;
        safety_hard_stop();
    }

    // Clear timer interrupt
    TIMERG0.int_clr_timers.t0 = 1;
    TIMERG0.hw_timer[0].config.alarm_en = 1;
}

// ─── Initialize Safety Interrupts ─────────────────────────────────────
void safety_init_interrupts() {
    // Configure E-Stop pin with internal pull-up
    gpio_config_t io_conf = {};
    io_conf.intr_type = GPIO_INTR_NEGEDGE;  // Trigger on falling edge
    io_conf.pin_bit_mask = (1ULL << ESTOP_PIN);
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpio_config(&io_conf);

    // Install GPIO ISR service
    gpio_install_isr_service(ESP_INTR_FLAG_IRAM);
    gpio_isr_handler_add((gpio_num_t)ESTOP_PIN, safety_estop_isr, NULL);

    // Initialize watchdog timer
    safety_init_watchdog();

    // Initialize heartbeat timestamp
    last_heartbeat_ms = millis();
}

// ─── Initialize Hardware Watchdog Timer ───────────────────────────────
void safety_init_watchdog() {
    timer_config_t timer_conf = {};
    timer_conf.divider = 80;           // 80MHz / 80 = 1MHz tick
    timer_conf.counter_dir = TIMER_COUNT_UP;
    timer_conf.counter_en = TIMER_PAUSE;
    timer_conf.alarm_en = TIMER_ALARM_EN;
    timer_conf.auto_reload = TIMER_AUTORELOAD_EN;

    timer_init(TIMER_GROUP_0, TIMER_0, &timer_conf);
    timer_set_counter_value(TIMER_GROUP_0, TIMER_0, 0);
    timer_set_alarm_value(TIMER_GROUP_0, TIMER_0, SAFETY_WATCHDOG_INTERVAL_US);
    timer_enable_intr(TIMER_GROUP_0, TIMER_0);
    timer_isr_register(TIMER_GROUP_0, TIMER_0, safety_watchdog_isr, NULL, ESP_INTR_FLAG_IRAM, NULL);
    timer_start(TIMER_GROUP_0, TIMER_0);
}

// ─── Feed Heartbeat (called from main loop) ───────────────────────────
void safety_feed_heartbeat() {
    last_heartbeat_ms = millis();

    // If previously expired but now getting heartbeats, clear flag
    if (safety_watchdog_expired) {
        safety_watchdog_expired = false;
    }
}

// ─── Check if Safety is Active ────────────────────────────────────────
bool safety_is_active() {
    return safety_estop_triggered || safety_watchdog_expired;
}

// ─── Hard Stop (immediate motor cutoff) ───────────────────────────────
void IRAM_ATTR safety_hard_stop() {
    // Immediately zero all PWM outputs
    ledcWrite(LEFT_PWM_PIN, 0);
    ledcWrite(RIGHT_PWM_PIN, 0);

    // Set all direction pins to brake mode (both HIGH or both LOW)
    gpio_set_level((gpio_num_t)LEFT_DIR_PIN1, 0);
    gpio_set_level((gpio_num_t)LEFT_DIR_PIN2, 0);
    gpio_set_level((gpio_num_t)RIGHT_DIR_PIN1, 0);
    gpio_set_level((gpio_num_t)RIGHT_DIR_PIN2, 0);

    // Turn off status LED to indicate stop
    gpio_set_level((gpio_num_t)STATUS_LED_PIN, 0);

    // Sound buzzer briefly (if available)
    gpio_set_level((gpio_num_t)BUZZER_PIN, 1);
    delayMicroseconds(100);
    gpio_set_level((gpio_num_t)BUZZER_PIN, 0);
}

// ─── Soft Stop (gradual deceleration via PID) ─────────────────────────
void safety_soft_stop() {
    // This is handled by the main PID loop
    // Set both setpoints to zero and let PID ramp down
    // Use in non-emergency situations
}

// ─── Reset Safety (requires explicit user action) ─────────────────────
void safety_reset() {
    // Only reset if E-Stop is physically released
    if (gpio_get_level((gpio_num_t)ESTOP_PIN) == 1 && !safety_watchdog_expired) {
        safety_estop_triggered = false;
        gpio_set_level((gpio_num_t)STATUS_LED_PIN, 1);
    }
}

#endif // SAFETY_INTERRUPT_H
