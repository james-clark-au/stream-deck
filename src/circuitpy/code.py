import time
import microcontroller
import random
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from digitalio import DigitalInOut, Pull

from PushButton import PushButton, PushState
from LazySerial import LazySerial


time.sleep(1)

MODE_SINGLE = 0                # Single shot, fire once at rising edge.
MODE_TOGGLE = 1                # Single shot, but keeps state LEDs toggling.
MODE_TOGGLE_CONTINUOUS = 2     # Toggle to continuous mode or off.
MODE_MOMENTARY_CONTINUOUS = 3  # Fire continuously while button held.

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0, 0, 0)


modes = (
  {
    'name': 'SPLIT',
    'colour': PURPLE,
    'toggle_colour': RED,
    'mode': MODE_TOGGLE,
    'sequence': (
      {'keys': (Keycode.GUI, Keycode.S), 'delay': 0.1},  # Splits!
    ),
  },
  {
    'name': 'SPAM_LMB',
    'colour': GREEN,
    'pulse_colour': YELLOW,
    'mode': MODE_MOMENTARY_CONTINUOUS,
    'sequence': (
      # {'keys': Keycode.A, 'delay': 0.01},  # aaaaa
      {'mouse': Mouse.LEFT_BUTTON, 'delay': 0.1},
    ),
  },
  {
    'name': 'HOLD_RMB',
    'colour': CYAN,
    'toggle_colour': RED,
    'mode': MODE_TOGGLE,
    'sequence': (
      {'mousehold': Mouse.RIGHT_BUTTON, 'delay': 1},
    ),
  },
)
current_mode_index = 0;
current = modes[current_mode_index]



keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
mouse = Mouse(usb_hid.devices)


# create the switch, add a pullup, start it with not being pressed
touch1 = DigitalInOut(microcontroller.pin.GPIO11)
touch1.switch_to_input(pull=Pull.UP)
button = PushButton(touch1, False)


toggled_on = False

lazy = LazySerial()


def make_keystrokes(keys, delay):
  if isinstance(keys, str):  # If it's a string...
    keyboard_layout.write(keys)  # ...Print the string
  elif isinstance(keys, int):  # If its a single key
    keyboard.press(keys)  # "Press"...
    keyboard.release_all()  # ..."Release"!
  elif isinstance(keys, (list, tuple)):  # If its multiple keys
    keyboard.press(*keys)  # "Press"...
    keyboard.release_all()  # ..."Release"!
  time.sleep(delay)

def make_mousestrokes(buttons, delay):
  if isinstance(buttons, int):
    mouse.click(buttons)
  time.sleep(delay)

def make_mousehold(buttons, delay):
  if isinstance(buttons, int):
    mouse.press(buttons)
  time.sleep(delay)

def run_sequence(sequence):
  if isinstance(sequence, (list, tuple)) and isinstance(sequence[0], dict):
    for k in sequence:
      if 'keys' in k:
        make_keystrokes(k['keys'], k['delay'])
      elif 'mouse' in k:
        make_mousestrokes(k['mouse'], k['delay'])
      elif 'mousehold' in k:
        make_mousehold(k['mousehold'], k['delay'])

def change_mode():
  # Reset things
  global toggled_on
  global current_mode_index
  global current
  toggled_on = False
  keyboard.release_all()
  mouse.release_all()

  # New mode
  current_mode_index = (current_mode_index + 1) % len(modes)
  current = modes[current_mode_index]
  print("Selected mode: ", current['name'])


def process_buttons():
  # fuck python
  global toggled_on

  push_state = button.loop()

  if current['mode'] == MODE_SINGLE:
    # Just fire our sequence when pushed
    if push_state == PushState.PRESSED:
      print("MODE_SINGLE: Button Pressed!")
      run_sequence(current['sequence'])
  
  elif current['mode'] == MODE_TOGGLE:
    # fire our sequence each time, but toggle LED (for e.g. mute)
    if push_state == PushState.PRESSED:
      toggled_on = not toggled_on
      print("MODE_TOGGLE: Button Toggled! ", toggled_on)
      run_sequence(current['sequence'])
      if not toggled_on:
        # Release any held keys if thats what we were using for the toggle
        keyboard.release_all()
        mouse.release_all()
  
  elif current['mode'] == MODE_TOGGLE_CONTINUOUS:
    # our sequence fires all the time if we are toggled on
    if toggled_on:
      run_sequence(current['sequence'])
    if push_state == PushState.PRESSED:
      toggled_on = not toggled_on
      print("MODE_TOGGLE_CONTINUOUS: Button Toggled! ", toggled_on)
      if not toggled_on:
        # Release any held keys if thats what we were using for the toggle
        keyboard.release_all()
        mouse.release_all()
  
  elif current['mode'] == MODE_MOMENTARY_CONTINUOUS:
    # run sequence for as long as the button is held.
    if push_state == PushState.HELD:
      print("MODE_MOMENTARY_CONTINUOUS: Button Held!")
      run_sequence(current['sequence'])
    elif push_state == PushState.RELEASED:
      print("MODE_MOMENTARY_CONTINUOUS: Button Released!")
      # Release any held keys if thats what we were using for the toggle
      keyboard.release_all()
      mouse.release_all()
    

print("Starting main loop!")
lazy.init()
while True:
  process_buttons()
  lazy.loop()

