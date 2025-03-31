from Helpers import *


class Heartbeat:
  def __init__(self, timeout_ms):
    self.last_heartbeat_ms = 0
    self.timeout_ms = timeout_ms
    self.is_enabled = False

  
  def beat(self):
    self.last_heartbeat_ms = millis()
  
  
  def enabled(self):
    return self.is_enabled
  
  
  def set_enabled(self, onoff):
    self.beat()
    self.is_enabled = onoff
  
  
  def beating(self):
    if not self.is_enabled:
      return True
    current_time_ms = millis()
    if current_time_ms < self.last_heartbeat_ms:
      # Wrapped around.
      self.last_heartbeat_ms = current_time_ms  # Imagine a freebie heartbeat
      return True
    wait = current_time_ms - self.last_heartbeat_ms
    return (wait < self.timeout_ms)

