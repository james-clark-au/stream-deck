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

  delay(1);
}
