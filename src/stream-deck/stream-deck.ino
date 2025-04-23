#include "globals.h"
#include "commands.h"


char read_saved_script(size_t pos) {
  return saved.readChar(pos);
}


void setup() {
  register_commands();
  Serial.begin(BAUD_RATE);

  saved.init();
  lazy.run_script(&read_saved_script);
  cmd_eyecatch(nullptr);
  Serial.println(F("\nOK READY"));
}


void loop() {
  lazy.loop();
  blinky.loop();
  for (int i = 0; i < NUM_LEDS; ++i) {
    leds[i].loop();
  }
  for (int i = 0; i < NUM_KEYS; ++i) {
    PushButton::PressState pushed = keys[i].loop();
    if (pushed == PushButton::PRESSED) {
      led_only(i);
    } else if (pushed == PushButton::RELEASED) {
      Serial.print(F("INPUT KEY "));
      Serial.print(i);
      Serial.println(F(" CLICKED"));
    } else if (pushed == PushButton::HELD && keys[i].lastHoldTime() > 1000) {
      keys[i].cancel();
      Serial.print(F("INPUT KEY "));
      Serial.print(i);
      Serial.println(F(" HELD"));
      leds[i].blink(1000);
      leds[i].set(LOW);  // Make sure it starts off
    }
  }
  if (heart.enabled() && ! heart.beating()) {
    heart.setEnabled(false);
    cmd_clear(nullptr);
  }

  delay(1);
}
