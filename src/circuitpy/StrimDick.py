# Holds hardware configuration of our 6 buttons and LEDs, lets you add behaviours
import microcontroller
from digitalio import DigitalInOut, Pull

from PushButton import PushButton, PushState
from BlinkyLed import BlinkyLed
from Helpers import *


class StreamDeck:
  def __init__(self, lazy, modes):
    self.buttons = []
    self.leds = []
    if isinstance(modes, (list, tuple)):
      self.modes = modes
    elif isinstance(modes, dict):
      self.modes = [ modes ]
    self.mode = 0
    self.lazy = lazy
    
    # Set up our actual physical pin layout
    self.add_button(microcontroller.pin.GPIO3, microcontroller.pin.GPIO28)
    self.add_button(microcontroller.pin.GPIO4, microcontroller.pin.GPIO27)
    self.add_button(microcontroller.pin.GPIO5, microcontroller.pin.GPIO26)
    self.add_button(microcontroller.pin.GPIO6, microcontroller.pin.GPIO23)
    self.add_button(microcontroller.pin.GPIO7, microcontroller.pin.GPIO20)
    self.add_button(microcontroller.pin.GPIO8, microcontroller.pin.GPIO22)
    # Load initial zeroeth config.
    self.attach_config(self.modes[self.mode])

  
  def add_button(self, sw_pin, led_pin):
    sw_io = DigitalInOut(sw_pin)
    sw_io.switch_to_input(pull=Pull.UP)
    self.buttons.append(PushButton(sw_io, False))
    self.leds.append(BlinkyLed(led_pin, 500))
  
  
  # Load a new set of button behaviours
  def set_mode(self, modenum):
    self.detach_config(self.modes[self.mode])
    self.mode = modenum
    self.flash(self.mode, 2, 3)
    self.lazy.say("MODE {}".format(self.mode))
    self.attach_config(self.modes[self.mode])


  def attach_config(self, config):
    # Trigger 'attached' callbacks for each configured Behaviour
    for idx, button in enumerate(self.buttons):
      if idx in config:
        behaviour = config[idx]
        behaviour.attached(self, idx)


  def detach_config(self, config):
    # Trigger 'detached' callbacks for each configured Behaviour
    for idx, button in enumerate(self.buttons):
      if idx in config:
        behaviour = config[idx]
        behaviour.detached()
  
  
  def next_mode(self):
    new_mode = (self.mode + 1) % len(self.modes)
    self.set_mode(new_mode)


  def prev_mode(self):
    new_mode = (self.mode + len(self.modes) - 1) % len(self.modes)
    self.set_mode(new_mode)
    
  
  # Set all LEDs on or off
  def set_leds(self, value):
    for led in self.leds:
      led.set_onoff(value)
  
  
  # Set all LEDs off except one on
  def set_only_led(self, idx):
    if idx not in range(len(self.leds)):
      return
    self.set_leds(False)
    self.leds[idx].on()
  

  # Set a specific LED to a BlinkyLed state
  def led_set_mode(self, idx, mode):
    if idx not in range(len(self.leds)):
      return
    self.leds[idx].set_mode(mode)
  
  
  # Set a specific LED on
  def led_on(self, idx):
    if idx not in range(len(self.leds)):
      return
    self.leds[idx].on()


  # Set a specific LED off
  def led_off(self, idx):
    if idx not in range(len(self.leds)):
      return
    self.leds[idx].off()


  # Set a specific LED to blink
  def led_blink(self, idx):
    if idx not in range(len(self.leds)):
      return
    self.leds[idx].blink()
  
  
  # Set a specific LED to be on or off based on a boolean
  def led_set_onoff(self, idx, on):
    if idx not in range(len(self.leds)):
      return
    self.leds[idx].set_onoff(on)
  
  
  # Toggle a specific LED 
  def led_toggle(self, idx):
    if idx not in range(len(self.leds)):
      return
    self.leds[idx].toggle()


  def loop(self):
    config = self.modes[self.mode]
    for idx, button in enumerate(self.buttons):
      state = button.loop()
      if idx in config:
        behaviour = config[idx]
        behaviour.push_state(state)
    for idx, led in enumerate(self.leds):
      led.loop()


  # Do a little animation of the lights
  def eyecatch(self, dir=1):
    seq = range(0, 6)
    if dir == -1:
      seq = range(5, -1, -1)
    for i in seq:
      self.set_only_led(i)
      snooze(20)
    self.set_leds(False)


  # Another animation, used in mode switches
  def flash(self, idx, times_all, times_one):
    for i in range(times_all):
      self.set_leds(True)
      snooze(80)
      self.set_leds(False)
      snooze(40)
    for i in range(times_one):
      self.led_on(idx)
      snooze(80)
      self.led_off(idx)
      snooze(40)


