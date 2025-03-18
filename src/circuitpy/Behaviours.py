# Here we define assorted classes to associate with each button, to declare how it should be actioned.
from PushButton import PushState
from Behaviour import Behaviour

class SimpleButton(Behaviour):
  def __init__(self, light_while_pressed=True):
    self.light_while_pressed = light_while_pressed
  
  def on_attached(self):
    self.led.value = not self.light_while_pressed
  
  def push_state(self, state):
    if self.light_while_pressed:
      if state == PushState.PRESSED:
        self.led.value = True
      elif state == PushState.RELEASED:
        self.led.value = False


class RadioButton(Behaviour):
  def __init__(self, group=()):
    self.group = group
  
  def on_attached(self):
    self.led.value = False
  
  def push_state(self, state):
    if self.light_while_pressed:
      if state == PushState.PRESSED:
        for i in self.group:
          self.dick.leds[i].value = False
        self.led.value = True

