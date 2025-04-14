# James Neko's Strim Dick

I made my own 6-key macropad for streaming out of an old mechanical key 'switch tester' I had! In doing so, I designed and had my very first PCB manufactured!

There's code here for both Arduino C++ _(Using a Nano, and relying on a Perl [lazy-serial-daemon](https://bitbucket.org/jamesneko/lazy-serial-daemon) plugin to respond to the keys)_ and CircuitPython for a TENSTAR RP2040 board that uses the Pro Micro form factor.

There's also some 3D printing files - one for the partial enclosure I adapted my switch tester with, one for a full housing for it.

I made a [video](https://www.youtube.com/watch?v=3drgDwhuff8) about it on my channel.

## Configuration

Presuming you're using the RP2040 / CircuitPython version, you might want some help on configuring it.

### Getting the CIRCUITPY drive to show up

Because it's a bit annoying to see the virtual USB drive show up all the time, I configure mine to hide it by default. This is done by editing `boot.py` and changing the line `HIDE_CIRCUITPY_DRIVE = False` to `True`. When this is set to `True`, the device will only show up as two USB Serial ports and one USB HID (Keyboard/Mouse) device.

To get it to show up as a USB Mass Storage device again, so you can edit the onboard files, hold down Key 0 - the one closest to the cable - as you plug it in. You can let go once the drive shows up.

On the CIRCUITPY drive, the two files you want to edit are `boot.py` for the setting above, and `code.py` to change your keys' behaviours. If you're on a Microsoft system you _might_ need a text editor smarter than NOTEPAD.EXE.

### Editing the key mapping

At the top of `code.py` you should see the current behaviours assigned to each key. The example configuration defines two modes that can be switched between:-

```python
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
```

Slightly below that, those 'modes' are loaded with the line:-
```
dick = StrimDick(lazy, [config_mode0, config_mode1])
```

You'll only need to modify that if you want to play with lots of different modes; if you just want the same behaviour for each key all the time, edit `config_mode0` and don't worry about anything else.

You'll see that after each key number 0..5 is the name of a Python class and some parameters in parentheses. Don't forget the comma at the end. The parameters change depending on which class you use, but most take a `key=` parameter, or two `key_on=` and `key_off=` parameters. The key can be defined in a few different ways, but more on that later.

Here are the different behaviours you can use (defined in `Behaviours.py`):-

#### SimpleButton(key=, light_while_pressed=True)

The most basic. Sends the key down event for your `key` when you press the button, sends the key up event when you release it.

`light_while_pressed` controls what the LED should do - turn on as you press the button (True), or be on all the time (False).

#### ToggleButton(key_on=, key_off=, led_initial=False)

This button remembers whether it's 'on' or 'off', and starts 'off' (`led_initial`).

It does a quick tap of `key_on` when you turn it on, and a quick tap of `key_off` (which can be the same as `key_on`) when you push the button and turn the LED off.

You could use this for e.g. a 'mute mic' button, so the LED indicates whether you've muted or unmuted it -- assuming it starts in the right state. If you want it to accurately reflect your mute state, you'd need to write extra code for your computer.

#### MomentaryButton(key_on=, key_off=, led_initial=False)

This button defaults to being 'on' or 'off' (depending on how you set `led_initial`), and becomes 'off' or 'on' only while held down.

Like the ToggleButton, it does a quick tap of `key_on` when you turn it on, and a quick tap of `key_off` (which can be the same as `key_on`) when you push the button and turn the LED off.

You could use this for e.g. a 'push to talk' button, or a 'push to mute' button, so that it sends the keyboard shortcut to mute/unmute when you start holding it, and does the same thing when you release it.

#### RadioButton(key=, group=())

This button works a little like the SimpleButton, sending a key down event when you push it and sending the key release event when you let go. What changes here is the LED - it starts off, and when it is pushed it switches itself on - and all the other RadioButtons in the same group off.

You could use this for switching scenes in OBS - set the `key=` for each button to some complicated shortcut key you set in OBS, and now as you switch between them, the relevant light will stay on! Be sure to set the `group=` parameter to the numbers of each other RadioButton - e.g. the whole deck would be `group=(0,1,2,3,4,5)`.

You _can_ make the LEDs update if you switch scenes from clicking around in OBS, but that will require a program running on your computer to connect to OBS and the USB Serial Port the Deck exposes.

#### RadioButtonWithHold(key=, key_when_held=, group=())

Exactly the same as RadioButton, but:-

- It only taps the `key` when released, if you tap the button.
- If you hold the button down longer than a second, it instead taps the `key_when_held`, and begins flashing its LED instead of the LED being on continuously.

This way you get an extra second layer of possible radio buttons!

#### SpamButton(key=, light_while_pressed=True, delay_ms=20)

This button repeatedly taps the `key` for as long as you hold it.

#### ModeSwitch(prev=False, light_while_pressed=True)

This button switches to the next mode defined in the config, or if `prev=True`, the previous mode. The lights will briefly flash to indicate you've changed modes.

### Key definitions

There are multiple ways to specify what kind of key you want to simulate on a button push. Most of these reference `Keycode` definitions that come from the [adafruit_hid library](https://docs.circuitpython.org/projects/hid/en/latest/api.html#adafruit_hid.keycode.Keycode)

The simplest and most straightforward is a single key on your keyboard, such as `Keycode.RIGHT_SHIFT`, `Keycode.Q`, or `Keycode.F1`.

Most keyboard shortcuts you might want to use though, are going to be complex ctrl-alt-shift-super kind of chords that you wouldn't normally type - because you want to use some global shortcut that doesn't conflict with any application shortcuts. To do these, put a list of Keycode values in parentheses, modifiers first, then the key you want to trigger last. For example, `(Keycode.CONTROL, Keycode.ALT, Keycode.SHIFT, Keycode.ONE)`. The library refers to your Super or Command or MICROSOFT WINDOWS™ LOGO® key as `Keycode.GUI`.

If you want to get silly, you can also put a plain-text string for your `key=` value, such as `"Let's circle back and align our goals on this later."`. The code will type out the message.

Finally, it's possible to 'press' mouse buttons in place of keys. `MouseLeft()`, `MouseRight()` and `MouseMiddle()` are set up if you need to do this for some strange reason. Try it with `SpamButton`!

## Errata

When laying out the PCB, I decided to grab the closer A6 and A7 inputs for switches 4 and 5, but I forgot that the Arduino Nano _doesn't let you do digital input on those pins_. I ended up using bodge wires from A0 and A1 to A6 and A7 to let me still easily read the switch status.

