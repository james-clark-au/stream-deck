# Holds hardware configuration of our 6 buttons and LEDs, lets you add behaviours
import time
import microcontroller
from digitalio import DigitalInOut, Pull

from PushButton import PushButton, PushState


class StrimDick:
  def __init__(self, lazy, config):
    self.buttons = []
    self.leds = []
    self.config = config
    self.lazy = lazy
    self.add_button(microcontroller.pin.GPIO3, microcontroller.pin.GPIO28)
    self.add_button(microcontroller.pin.GPIO4, microcontroller.pin.GPIO27)
    self.add_button(microcontroller.pin.GPIO5, microcontroller.pin.GPIO26)
    self.add_button(microcontroller.pin.GPIO6, microcontroller.pin.GPIO23)
    self.add_button(microcontroller.pin.GPIO7, microcontroller.pin.GPIO20)
    self.add_button(microcontroller.pin.GPIO8, microcontroller.pin.GPIO22)
    for idx, button in enumerate(self.buttons):
      if idx in self.config:
        behaviour = self.config[idx]
        behaviour.attached(self, idx)

  
  def add_button(self, sw_pin, led_pin):
    sw_io = DigitalInOut(sw_pin)
    sw_io.switch_to_input(pull=Pull.UP)
    self.buttons.append(PushButton(sw_io, False))
    led_io = DigitalInOut(led_pin)
    led_io.switch_to_output()
    self.leds.append(led_io)
  
  
  def set_leds(self, value):
    for led in self.leds:
      led.value = value
  
  
  def set_only_led(self, idx):
    self.set_leds(False)
    self.leds[idx].value = True
  

  def loop(self):
    for idx, button in enumerate(self.buttons):
      state = button.loop()
      if idx in self.config:
        behaviour = self.config[idx]
        behaviour.push_state(state)


  def eyecatch(self, dir=1):
    seq = range(0, 6)
    if dir == -1:
      seq = range(5, -1, -1)
    for i in seq:
      self.set_only_led(i)
      time.sleep(0.020)
    self.set_leds(False)
