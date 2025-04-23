#pragma once
#include <Arduino.h>

namespace Heartbeat {
  class Heartbeat {
  public:
    unsigned long d_last_heartbeat_ms = 0;
    unsigned long d_timeout_ms = 0;
    bool d_enabled = false;
  
    Heartbeat(unsigned long timeout_ms) {
      d_last_heartbeat_ms = millis();
      d_timeout_ms = timeout_ms;
    }
    

    void
    beat() {
      d_last_heartbeat_ms = millis();
    }


    bool
    enabled() {
      return d_enabled;
    }

    void
    setEnabled(bool on) {
      beat();
      d_enabled = on;
    }


    bool
    beating() {
      if ( ! d_enabled) {
        return true;
      }
      unsigned long current_time_ms = millis();
      if (current_time_ms < d_last_heartbeat_ms) {
        // We've wrapped around. Let's just assume true for the moment. It doesn't have to be super accurate.
        d_last_heartbeat_ms = current_time_ms;  // imagine a freebie heartbeat.
        return true;
      }
      unsigned long wait = current_time_ms - d_last_heartbeat_ms;
      return (wait < d_timeout_ms);
    }

  };
} // namespace
