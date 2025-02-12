#include "globals.h"
#include "commands.h"


void setup() {
  register_commands();
}


void loop() {
  lazy.loop();
  blinky.loop();

  delay(1);
}
