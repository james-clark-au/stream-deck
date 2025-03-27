# superclass for Behaviours.

class Behaviour:
  # Constructor arguments depend on the actual desired Behaviour subclass.
  def __init__(self):
    pass

  # more easily overridden hook to do any init once we are attached
  def on_attached(self):
    pass

  # more easily overridden hook to save any state as we are detached
  def on_detached(self):
    pass
  
  # push_state() is a hook to check each tick for button status.
  # `state` value is a PushButton::PushState.
  def push_state(self, state):
    pass
  
  # attached() is called by StrimDick as it pulls the config in.
  def attached(self, dick, idx):
    self.dick = dick
    self.idx = idx
    self.button = dick.buttons[idx]
    self.led = dick.leds[idx]
    self.on_attached()
  
  # detached() is called by StrimDick if a mode switch removes a Behaviour from a key.
  def detached(self):
    self.on_detached()
  
  # for you to call in your handler, if you want serial events for keypresses
  # e.g. action might be CLICKED or HELD or whatever you need.
  def emit(self, action):
    self.dick.lazy.say("INPUT KEY {} {}".format(self.idx, action))

