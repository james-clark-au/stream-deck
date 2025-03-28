# James Neko's Strim Dick

I made my own 6-key macropad for streaming out of an old mechanical key 'switch tester' I had! In doing so, I designed and had my very first PCB manufactured!

There's code here for both Arduino C++ _(Using a Nano, and relying on a Perl [lazy-serial-daemon](https://bitbucket.org/jamesneko/lazy-serial-daemon) plugin to respond to the keys)_ and CircuitPython for a TENSTAR RP2040 board that uses the Pro Micro form factor.

There's also some 3D printing files - one for the partial enclosure I adapted my switch tester with, one for a full housing for it.

I made a [video](https://www.youtube.com/watch?v=3drgDwhuff8) about it on my channel.

## Errata

When laying out the PCB, I decided to grab the closer A6 and A7 inputs for switches 4 and 5, but I forgot that the Arduino Nano _doesn't let you do digital input on those pins_. I ended up using bodge wires from A0 and A1 to A6 and A7 to let me still easily read the switch status.

