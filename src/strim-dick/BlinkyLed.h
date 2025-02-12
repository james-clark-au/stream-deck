#pragma once

namespace BlinkyLed
{
  class BlinkyLed
  {
  public:
    uint8_t  d_pin      = 13;
    uint8_t  d_state    = LOW;
    uint32_t d_interval = 500;
  
    BlinkyLed(uint8_t pin, uint32_t interval_ms) {
      d_pin = pin;
      d_interval = interval_ms;
      pinMode(pin, OUTPUT);
    }
  
    void
    changePin(uint8_t pin) {
      // Bring old pin low first
      set(LOW);
      // Set new pin
      d_pin = pin;
      pinMode(d_pin, OUTPUT);
      digitalWrite(d_pin, d_state);
    }
  
    void
    changeInterval(uint32_t interval_ms) {
      set(LOW);
      d_interval = interval_ms;
    }
  
    void
    set(uint8_t state) {
      d_state = state;
      digitalWrite(d_pin, d_state);
    }
  
    void
    loop() {
      uint32_t heartBeat = millis() % (d_interval * 2);
      if (heartBeat < d_interval && d_state != LOW) {
        set(LOW);
      } else if (heartBeat >= d_interval && d_state != HIGH) {
        set(HIGH);
      }
    }
  };

} // namespace

