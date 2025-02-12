#pragma once
#include <LazySerial.h>

#include "helpers.h"
#include "globals.h"

LazySerial::LazySerial lazy(Serial);



void cmd_ohai(char *args) {
  Serial.println(F("OHAI " LAZY_ID " " __TIMESTAMP__  KEYVAL(BOARD_NAME) KEYVAL(USB_HID)  ));
}


void cmd_pinout(char *args) {
  Serial.print(F("OK PINOUT"  KEYVAL(STATUS_LED)  ));
  // dynamically stored pins here?
  Serial.println("");
}



void register_commands() {
  lazy.register_callback("OHAI", &cmd_ohai);
  lazy.register_callback("PINOUT", &cmd_pinout);
}


