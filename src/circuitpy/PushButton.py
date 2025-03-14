import time

DEBOUNCE_TIME_MS = 20

def millis():
  return time.monotonic() * 1000

# enum hack
class PushState:
  UNINITIALISED = 0
  NOT_HELD = 1
  PRESSED_AWAITING_CONFIRM = 2
  PRESSED = 3
  HELD = 4
  RELEASED_AWAITING_CONFIRM = 5
  RELEASED = 6
  CANCELLED = 7


class PushButton:
  # Parameters
  #source = Nil  # A digitalio or touchio source we can access .value on.
  #trigger_high = True  # Should we look for a high value or a low one?
  
  # Internal state
  latch = False
  rising_edge_started_at = 0   # 'rising' in this case means pushed, even if the logic level goes low from a button shorted to ground.
  falling_edge_started_at = 0
  pressed_at = 0
  last_hold_time = 0
  want_cancel = False
  
  def __init__(self, source, trigger_high):
    self.source = source
    self.trigger_high = trigger_high
  
  
  # Returns a PushState
  def loop(self):
    if not self.source:
      return PushState.UNINITIALISED
    
    if self.trigger_high:
      measurement = self.source.value
    else:
      measurement = not self.source.value
    current_time_ms = millis()
    
    if measurement:
      # Still pushed, still holding
      if self.latch:
        self.last_hold_time = current_time_ms
        if self.want_cancel:
          return PushState.CANCELLED
        return PushState.HELD
      
      # Debounce - rising edge
      if self.rising_edge_started_at == 0:
        # Start waiting
        self.rising_edge_started_at = current_time_ms
      elif current_time_ms - self.rising_edge_started_at < DEBOUNCE_TIME_MS:
        # Still waiting
        if self.want_cancel:
          return PushState.CANCELLED
        return PushState.PRESSED_AWAITING_CONFIRM
      else:
        # Able to proceed.
        self.latch = True
        self.rising_edge_started_at = 0
        self.falling_edge_started_at = 0
        self.pressed_at = current_time_ms
        if self.want_cancel:
          return PushState.CANCELLED
        return PushState.PRESSED
      
    else:
      # Still unpushed, still not holding
      if not self.latch:
        self.want_cancel = False  # uncancel, button is released
        return PushState.NOT_HELD
      
      # Debounce - falling edge
      if self.falling_edge_started_at == 0:
        # Start waiting
        self.falling_edge_started_at = current_time_ms
      elif current_time_ms - self.falling_edge_started_at < DEBOUNCE_TIME_MS:
        # Still waiting
        if self.want_cancel:
          return PushState.CANCELLED
        return PushState.RELEASED_AWAITING_CONFIRM
      else:
        # Able to proceed
        self.latch = False
        self.last_hold_time = self.falling_edge_started_at - self.pressed_at
        self.rising_edge_started_at = 0
        self.falling_edge_started_at = 0
        if self.want_cancel:
          return PushState.CANCELLED
        return PushState.RELEASED
    
    # End of loop()
    return PushState.NOT_HELD  # Should be unreachable.
  
  # Some sort of keypress, e.g. long hold, is now actioned, please don't emit any other PushStates for this push.
  def cancel(self):
    self.want_cancel = True

