import time
import microcontroller
import random
from digitalio import DigitalInOut, Pull
# adafruit_hid is a separate library you need to get from the circuitpy site and drop in lib/
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from BlinkyLed import BlinkyLed
from PushButton import PushButton, PushState
from LazySerial import LazySerial
from StrimDick import StrimDick
from Behaviours import *

# Here we define what we actually want each key to do
config = {
  0: RadioButton(key=(Keycode.GUI, Keycode.Q), group=(0, 1, 2)),
  1: RadioButton(key=(Keycode.GUI, Keycode.R), group=(0, 1, 2)),
  2: RadioButton(key=(Keycode.GUI, Keycode.S), group=(0, 1, 2)),
  3: SimpleButton(key=Keycode.RIGHT_SHIFT),
  4: RadioButtonWithHold(key=(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.ONE), key_when_held="Hello", group=(5, 6)),
  5: RadioButtonWithHold(key=(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.TWO), key_when_held="World", group=(5, 6)),
}

lazy = LazySerial()
blinky = BlinkyLed(microcontroller.pin.GPIO17, 500)
dick = StrimDick(lazy, config)


# Serial commands
def cmd_eyecatch(lazy, args):
  dick.eyecatch()
  lazy.say("OK EYECATCH")
lazy.register("EYECATCH", cmd_eyecatch)

def cmd_clear(lazy, args):
  dick.set_leds(False)
  lazy.say("OK CLEAR")
lazy.register("CLEAR", cmd_clear)


# Let's go!
print("Starting main loop!")
lazy.init()
dick.eyecatch()

while True:
  dick.loop()
  lazy.loop()
  blinky.loop()
