#include "globals.h"
#include "commands.h"


void setup() {
  register_commands();
  Serial.begin(BAUD_RATE);

  Serial.println(F("\nOK STARTING"));
}


void loop() {
  lazy.loop();
  blinky.loop();
  for (int i = 0; i < NUM_LEDS; ++i) {
    leds[i].loop();
  }

  delay(1);
}
