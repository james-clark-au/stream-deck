#pragma once
#include <Arduino.h>

#define DEBOUNCE_TIME_MS 20

namespace PushButton {

  static const uint8_t NO_PIN = 255;

  enum PressState {
    UNINITIALISED,
    NOT_HELD,
    PRESSED_AWAITING_CONFIRM,
    PRESSED,
    HELD,
    RELEASED_AWAITING_CONFIRM,
    RELEASED,
    CANCELLED,
  };

  class PushButton {
  public:
    uint8_t d_pin = NO_PIN;
    bool d_latch;
    unsigned long d_rising_edge_started_at;  // slight misnomer since we usually use short to ground for a pushbutton.
    unsigned long d_falling_edge_started_at; // so imagine this is "pushed signal" high / low.
    unsigned long d_pressed_at;
    unsigned long d_last_hold_time;
    bool d_cancel;
    
    PushButton() {  }


    explicit
    operator bool() const {
      return d_pin != NO_PIN;
    }


    uint8_t
    pin() {
      return d_pin;
    }


    void
    changePin(uint8_t pin) {
      d_pin = pin;
      pinMode(d_pin, INPUT_PULLUP);
      d_latch = false;
      d_rising_edge_started_at = 0;
      d_falling_edge_started_at = 0;
      d_pressed_at = 0;
      d_cancel = false;
    }


    PressState
    loop() {
      if (d_pin == NO_PIN) {
        return UNINITIALISED;
      }
      int measurement = digitalRead(d_pin);
      unsigned long current_time_ms = millis();

      if (measurement == LOW) {
        // Still LOW, still holding
        if (d_latch) {
          d_last_hold_time = current_time_ms - d_pressed_at;
          if (d_cancel) { return CANCELLED; }
          return HELD;
        }

        // Debounce - rising edge
        if (d_rising_edge_started_at == 0) {
          // Start waiting
          d_rising_edge_started_at = current_time_ms;
        } else if (current_time_ms - d_rising_edge_started_at < DEBOUNCE_TIME_MS) {
          // Still waiting
          if (d_cancel) { return CANCELLED; }
          return PRESSED_AWAITING_CONFIRM;
        } else {
          // Able to proceed.
          d_latch = true;
          d_rising_edge_started_at = 0;
          d_falling_edge_started_at = 0;
          d_pressed_at = current_time_ms;
          if (d_cancel) { return CANCELLED; }
          return PRESSED;
        }

      } else {
        // Still HIGH, still not holding
        if ( ! d_latch) {
          d_cancel = false;  // uncancel, button is released
          return NOT_HELD;
        }

        // Debounce - falling edge
        if (d_falling_edge_started_at == 0) {
          // Start waiting
          d_falling_edge_started_at = current_time_ms;
        } else if (current_time_ms - d_falling_edge_started_at < DEBOUNCE_TIME_MS) {
          // Still waiting
          if (d_cancel) { return CANCELLED; }
          return RELEASED_AWAITING_CONFIRM;
        } else {
          // Able to proceed.
          d_latch = false;
          d_last_hold_time = d_falling_edge_started_at - d_pressed_at;
          d_rising_edge_started_at = 0;
          d_falling_edge_started_at = 0;
          if (d_cancel) { return CANCELLED; }
          return RELEASED;
        }

      }
      return NOT_HELD;  // Should be unreachable.
    }


    unsigned long
    lastHoldTime() {
      return d_last_hold_time;
    }


    void
    cancel() {
      d_cancel = true;
    }

  };
}
