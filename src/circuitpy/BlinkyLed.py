import time
import digitalio

def millis():
  return time.monotonic() * 1000

class BlinkyLed:
  def __init__(self, pin, interval_ms):
    self.pin = pin
    self.interval_ms = interval_ms
    self.led = digitalio.DigitalInOut(pin)
    self.led.direction = digitalio.Direction.OUTPUT
  
  def loop(self):
    heartbeat = millis() % (self.interval_ms * 2)
    if heartbeat < self.interval_ms and self.led.value:
      self.led.value = False
    elif heartbeat >= self.interval_ms and not self.led.value:
      self.led.value = True

