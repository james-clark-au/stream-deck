import microcontroller
from digitalio import DigitalInOut, Pull
import storage
import usb_cdc
import usb_midi

# Set to True to not load up the CIRCUITPY drive at boot.
# If you want to edit code again, you'll have to hold down Switch 0 as you plug it in.
HIDE_CIRCUITPY_DRIVE = False

# hackily check SW0 to see if it's being held down at boot.
sw0 = DigitalInOut(microcontroller.pin.GPIO3)
sw0.switch_to_input(pull=Pull.UP)


if HIDE_CIRCUITPY_DRIVE:
  # If button is held, value will be low
  if not switch.value:
    print("Button held, enabling USB drive!")
  else:
    print("Button not held, disabling USB drive!")
    storage.disable_usb_drive()


usb_cdc.enable(console=True, data=True)    # console is the Python REPL, data is our own custom serial device.


# We also really don't need the MIDI device that's enabled by default.
usb_midi.disable()
