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

# Here we define what we actually want each key to do
config = {}

lazy = LazySerial()
blinky = BlinkyLed(microcontroller.pin.GPIO17, 500)
dick = StrimDick(lazy, config)


print("Starting main loop!")
lazy.init()
dick.eyecatch()

while True:
  dick.loop()
  lazy.loop()
  blinky.loop()
