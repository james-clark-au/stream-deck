from Helpers import *
from digitalio import DigitalInOut, Pull


class BlinkyLed:
  OFF = 0
  ON = 1
  BLINK = 2
  
  def __init__(self, pin, interval_ms):
    self.mode = BlinkyLed.OFF
    self.pin = pin
    self.interval_ms = interval_ms
    self.led = DigitalInOut(pin)
    self.led.switch_to_output()
  
  
  def set_mode(self, mode):
    self.mode = mode
    if mode == BlinkyLed.OFF:
      self.led.value = False
    elif mode == BlinkyLed.ON:
      self.led.value = True
  
  
  def on(self):
    self.set_mode(BlinkyLed.ON)


  def off(self):
    self.set_mode(BlinkyLed.OFF)


  def blink(self):
    self.set_mode(BlinkyLed.BLINK)
  
  
  def set_onoff(self, on):
    if on:
      self.on()
    else:
      self.off()
  
  
  def toggle(self):
    if self.mode == BlinkyLed.OFF:
      self.on()
      return True
    else:
      self.off()
      return False
  
  
  def loop(self):
    if self.mode == BlinkyLed.BLINK:
      heartbeat = millis() % (self.interval_ms * 2)
      if heartbeat < self.interval_ms and self.led.value:
        self.led.value = False
      elif heartbeat >= self.interval_ms and not self.led.value:
        self.led.value = True

