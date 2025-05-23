# Here we define assorted classes to associate with each button, to declare how it should be actioned.
from PushButton import PushState
from BlinkyLed import BlinkyLed
from Behaviour import Behaviour
from Keeb import sendkeys, holdkeys, releasekeys
from Helpers import *


# Send key while pushed. (release key when button is)
# Light up while doing so (or, be on all the time)
class SimpleButton(Behaviour):
  def __init__(self, key=None, light_while_pressed=True):
    self.key = key
    self.light_while_pressed = light_while_pressed
  
  def on_attached(self):
    self.led.set_onoff(not self.light_while_pressed)
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      if self.light_while_pressed:
        self.led.on()
      self.emit("CLICKED")
      holdkeys(self.key)
    elif state == PushState.RELEASED:
      if self.light_while_pressed:
        self.led.off()
      releasekeys(self.key)


# *Tap* key when pushed. Taps the alternate key when pushed again.
# Starts with LED off (optionally, on), toggles LED state with each push.
class ToggleButton(Behaviour):
  def __init__(self, key_on=None, key_off=None, led_initial=False):
    self.key_on = key_on
    self.key_off = key_off
    self.led_initial = led_initial
    self.toggled = led_initial
  
  def on_attached(self):
    self.led.set_onoff(self.toggled)
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      self.toggled = self.led.toggle()
      if self.toggled:
        self.emit("TOGGLED ON")
        sendkeys(self.key_on)
      else:
        self.emit("TOGGLED OFF")
        sendkeys(self.key_off)


# *Tap* key_on when pressed down. Taps the alternate key when released.
# Starts with LED off (optionally, on), toggles LED state while held.
class MomentaryButton(Behaviour):
  def __init__(self, key_on=None, key_off=None, led_initial=False):
    self.key_on = key_on
    self.key_off = key_off
    self.led_initial = led_initial
  
  def on_attached(self):
    self.led.set_onoff(self.led_initial)
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      self.led.set_onoff(not self.led_initial)
      self.emit("PRESSED")
      sendkeys(self.key_on)
    elif state == PushState.RELEASED:
      self.led.set_onoff(self.led_initial)
      self.emit("RELEASED")
      sendkeys(self.key_off)


# Send key while pushed. (release key when button is)
# Light follows whichever button in the group was pushed last.
class RadioButton(Behaviour):
  def __init__(self, key=None, group=()):
    self.key = key
    self.group = group
    self.led_mode = BlinkyLed.OFF
  
  def on_attached(self):
    self.led.set_mode(self.led_mode)
  
  # If a mode switch happens, we need to remember our state.
  def on_detached(self):
    self.led_mode = self.led.mode
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      for i in self.group:
        self.deck.led_off(i)
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
    self.led_mode = BlinkyLed.OFF
  
  def on_attached(self):
    self.led.set_mode(self.led_mode)
  
  # If a mode switch happens, we need to remember our state.
  def on_detached(self):
    self.led_mode = self.led.mode
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      for i in self.group:
        self.deck.led_off(i)
      self.led.on()
    elif state == PushState.RELEASED:
      self.emit("CLICKED")
      sendkeys(self.key)
    elif state == PushState.HELD and self.button.last_hold_time > 1000:
      self.button.cancel()  # Don't also emit a 'released'
      self.led.off()
      self.emit("HELD")
      sendkeys(self.key_when_held)
      self.led.blink()


# Repeatedly tap key while pushed. (release key when button is)
# Light up while doing so (or, be on all the time)
class SpamButton(Behaviour):
  def __init__(self, key=None, light_while_pressed=True, delay_ms=20):
    self.key = key
    self.light_while_pressed = light_while_pressed
    self.delay_ms = delay_ms
    self.flipflop = False
    self.lastflip = 0
  
  def on_attached(self):
    self.led.set_onoff(not self.light_while_pressed)
  
  def on_detached(self):
    if self.flipflop:
      releasekeys(self.key)
      self.flipflop = False
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      if self.light_while_pressed:
        self.led.on()
      self.emit("SPAMMING START")
    elif state == PushState.RELEASED:
      self.led.set_onoff(not self.light_while_pressed)
      releasekeys(self.key)
      self.emit("SPAMMING OVER")
    elif state == PushState.HELD:
      # pew pew pew pew pew
      delta = millis() - self.lastflip
      if delta > self.delay_ms:
        self.lastflip = millis()
        self.flipflop = not self.flipflop
        self.led.set_onoff(self.flipflop)
        if self.flipflop:
          holdkeys(self.key)
        else:
          releasekeys(self.key)


# Does not send keypresses, just selects a new config mode (assuming there are multiple defined)
class ModeSwitch(Behaviour):
  def __init__(self, prev=False, light_while_pressed=True):
    self.prev = prev
    self.light_while_pressed = light_while_pressed
  
  def on_attached(self):
    self.led.set_onoff(not self.light_while_pressed)
  
  def push_state(self, state):
    if state == PushState.PRESSED:
      if self.light_while_pressed:
        self.led.on()
    elif state == PushState.RELEASED:
      if self.light_while_pressed:
        self.led.off()
      self.emit("CLICKED")
      if self.prev:
        self.deck.prev_mode()
      else:
        self.deck.next_mode()
  
