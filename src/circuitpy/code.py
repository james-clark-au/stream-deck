import microcontroller
# adafruit_hid is a separate library you need to get from the circuitpy site and drop in lib/
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

from BlinkyLed import BlinkyLed
from PushButton import PushButton, PushState
from Heartbeat import Heartbeat
from LazySerial import LazySerial
from StreamDeck import StreamDeck
from Behaviours import *
from Keeb import MouseLeft, MouseRight, MouseMiddle


############################################ CONFIG ################################################
# Here we define what we actually want each key to do. Associate keys 0-5 with a Behaviour,
# various types defined in Behaviours.py. Values for 'key' parameters can be a Keycode value,
# from https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode
# or a Tuple of several Keycode values for a chorded sequence, or a string literal for some text
# to type. None should also work, if you just want a key to send a serial console message.
####################################################################################################
config_mode0 = {
  0: RadioButton(key=(Keycode.GUI, Keycode.Q), group=(0, 1, 2)),
  1: RadioButton(key=(Keycode.GUI, Keycode.R), group=(0, 1, 2)),
  2: RadioButton(key=(Keycode.GUI, Keycode.S), group=(0, 1, 2)),
  3: SimpleButton(key=Keycode.RIGHT_SHIFT),
  4: SpamButton(key=MouseLeft(), delay_ms=30),
  5: ModeSwitch(),
}
config_mode1 = {
  0: RadioButtonWithHold(key=(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.ONE), key_when_held="Hello", group=(0, 1)),
  1: RadioButtonWithHold(key=(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.TWO), key_when_held="World", group=(0, 1)),
  2: MomentaryButton(key_on=(Keycode.GUI, Keycode.V), key_off=(Keycode.GUI, Keycode.V), led_initial=False),
  3: ToggleButton(key_on=(Keycode.GUI, Keycode.V), key_off=(Keycode.GUI, Keycode.V), led_initial=True),
  4: ToggleButton(key_on="Bed goes up", key_off="Bed goes down"),
  5: ModeSwitch(),
}

############################################ GLOBALS ###############################################
lazy = LazySerial()
blinky = BlinkyLed(microcontroller.pin.GPIO17, 500)
blinky.blink()
heart = Heartbeat(10000)
deck = StreamDeck(lazy, [config_mode0, config_mode1])


######################################### SERIAL COMMANDS ##########################################
# These are commands you can use on the serial interface (e.g. /dev/ttyACM1) to receive key input
# and control LEDs yourself via a program on the host, if you choose.
# Not to be confused with the CircuitPython REPL that also exists (on e.g. /dev/ttyACM0)
####################################################################################################
def cmd_ohai(lazy, args):
  lazy.say("OHAI circuitpy-stream-deck 1.0")
lazy.register("OHAI", cmd_ohai)

def cmd_eyecatch(lazy, args):
  deck.eyecatch()
  lazy.say("OK EYECATCH")
lazy.register("EYECATCH", cmd_eyecatch)

def cmd_clear(lazy, args):
  deck.set_leds(False)
  lazy.say("OK CLEAR")
lazy.register("CLEAR", cmd_clear)

def usage_led(lazy):
  lazy.say("ERR Usage: LED <num> (ON|OFF|ONLY|BLINK)")
  
def cmd_led(lazy, args):
  if len(args) == 0:
    return usage_led(lazy)
  num = 0
  try:
    num = int(args.pop(0))
  except ValueError:
    return usage_led(lazy)
  if num < 0 or num >= len(deck.leds):
    lazy.say("ERR num must be 0..^{}".format(len(deck.leds)))
    return
  if len(args) == 0:
    return usage_led(lazy)
  
  verb = args.pop(0).upper()
  if verb == "OFF":
    deck.leds[num].off()
    lazy.say("OK LED {} {}".format(num, verb))
  elif verb == "ON":
    deck.leds[num].on()
    lazy.say("OK LED {} {}".format(num, verb))
  elif verb == "ONLY":
    deck.set_only_led(num)
    lazy.say("OK LED {} {}".format(num, verb))
  elif verb == "BLINK":
    deck.leds[num].blink()
    lazy.say("OK LED {} {}".format(num, verb))
  else:
    return usage_led(lazy)
lazy.register("LED", cmd_led)

def cmd_heartbeat(lazy, args):
  if len(args) == 0:
    heart.beat()
    lazy.say("OK HEARTBEAT")
    return
  verb = args.pop(0).upper()
  if verb == "ON":
    heart.set_enabled(True)
    lazy.say("OK HEARTBEAT ON")
  elif verb == "OFF":
    heart.set_enabled(False)
    lazy.say("OK HEARTBEAT OFF")
  else:
    heart.beat()
    lazy.say("OK HEARTBEAT")
lazy.register("HEARTBEAT", cmd_heartbeat)

def usage_mode():
  lazy.say("ERR Usage: MODE <num>")
def cmd_mode(lazy, args):
  if len(args) == 0:
    return usage_led(lazy)
  num = 0
  try:
    num = int(args.pop(0))
  except ValueError:
    return usage_led(lazy)
  if num < 0 or num >= len(deck.modes):
    lazy.say("ERR num must be 0..^{}".format(len(deck.modes)))
    return
  lazy.say("OK MODE {}".format(num))
  deck.set_mode(num)
lazy.register("MODE", cmd_mode)


############################################# MAIN LOOP ############################################
print("Starting main loop!")
lazy.init()
deck.eyecatch()

while True:
  deck.loop()
  lazy.loop()
  blinky.loop()
  if heart.enabled() and not heart.beating():
    print("Heartbeat stopped, clearing LEDs!")
    heart.set_enabled(False)
    deck.set_leds(False)

