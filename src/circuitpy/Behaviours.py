# Here we define assorted classes to associate with each button, to declare how it should be actioned.
from PushButton import PushState
from Behaviour import Behaviour
from Keeb import sendkeys, holdkeys, releasekeys


# Send key while pushed. (release key when button is)
# Light up while doing so (or, be on all the time)
class SimpleButton(Behaviour):
  def __init__(self, key=None, light_while_pressed=True):
    self.key = key
    self.light_while_pressed = light_while_pressed
  
  def on_attached(self):
    self.led.set_onoff(not self.light_while_pressed)
  
  def push_state(self, state):
    if self.light_while_pressed:
      if state == PushState.PRESSED:
        self.led.on()
        self.emit("CLICKED")
        holdkeys(self.key)
      elif state == PushState.RELEASED:
        self.led.off()
        releasekeys(self.key)


# *Tap* key when pushed. Taps the alternate key when pushed again.
# Starts with LED off (optionally, on), toggles LED state with each push.
class ToggleButton(Behaviour):
  def __init__(self, key_on=None, key_off=None, led_initial=False):
    self.key_on = key_on
    self.key_off = key_off
    self.led_initial = led_initial
  
  def on_attached(self):
    self.led.set_onoff(self.led_initial)
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      self.led.toggle()
      if self.led.mode == BlinkyLed.ON:
        self.emit("TOGGLED ON")
        sendkeys(self.key_on)
      else:
        self.emit("TOGGLED OFF")
        sendkeys(self.key_off)


# Send key while pushed. (release key when button is)
# Light follows whichever button in the group was pushed last.
class RadioButton(Behaviour):
  def __init__(self, key=None, group=()):
    self.key = key
    self.group = group
  
  def on_attached(self):
    self.led.off()
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      for i in self.group:
        self.dick.leds[i].value = False
      self.led.on()
      self.emit("CLICKED")
      holdkeys(self.key)
    elif state == PushState.RELEASED:
      releasekeys(self.key)


# *Tap* key after button is released.
# Holding the button for longer than a second will tap an alternative key.
# Light follows last button pushed.
class RadioButtonWithHold(Behaviour):
  def __init__(self, key, key_when_held, group=()):
    self.key = key
    self.key_when_held = key_when_held
    self.group = group
  
  def on_attached(self):
    self.led.off()
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      for i in self.group:
        self.dick.leds[i].value = False
      self.led.on()
    elif state == PushState.RELEASED:
      self.emit("CLICKED")
      sendkeys(self.key)
    elif state == PushState.HELD and self.button.last_hold_time > 1000:
      self.button.cancel()  # Don't also emit a 'released'
      self.emit("HELD")
      sendkeys(self.key_when_held)
      self.led.blink()
        

