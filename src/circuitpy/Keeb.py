# All the stuff we use to send keyboard and mouse events
import usb_hid
# adafruit_hid is a separate library you need to get from the circuitpy site and drop in lib/
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)


class MouseButton:
  def __init__(self, btn):
    self.btn = btn

class MouseLeft(MouseButton):
  def __init__(self):
    self.btn = Mouse.LEFT_BUTTON

class MouseRight(MouseButton):
  def __init__(self):
    self.btn = Mouse.RIGHT_BUTTON

class MouseMiddle(MouseButton):
  def __init__(self):
    self.btn = Mouse.MIDDLE_BUTTON

# Call with a string to type that string,
# Call with a single keycode to tap that keycode, e.g. Keycode.F1  (See https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode for full list)
# Call with a list of keycodes to tap a chorded sequence, e.g. (Keycode.GUI, Keycode.S)
def sendkeys(keys):
  if isinstance(keys, str):
    keyboard_layout.write(keys)
  elif isinstance(keys, int):
    keyboard.press(keys)
    keyboard.release(keys)
  elif isinstance(keys, (list, tuple)):
    keyboard.press(*keys)
    keyboard.release(*keys)
  elif isinstance(keys, MouseButton):
    mouse.press(keys.btn)
    mouse.release(keys.btn)

def holdkeys(keys):
  if isinstance(keys, str):  # What are you doing?
    keyboard_layout.write(keys)
  elif isinstance(keys, int):
    keyboard.press(keys)
  elif isinstance(keys, (list, tuple)):
    keyboard.press(*keys)
  elif isinstance(keys, MouseButton):
    mouse.press(keys.btn)

def releasekeys(keys):
  if isinstance(keys, str):  # WHAT are you doing?
    pass
  elif isinstance(keys, int):
    keyboard.release(keys)
  elif isinstance(keys, (list, tuple)):
    keyboard.release(*keys)
  elif isinstance(keys, MouseButton):
    mouse.release(keys.btn)


