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


void cmd_blink(char *args) {
  char *pos = firsttok(args);
  if ( ! pos) {
    Serial.println(F("ERR Usage: BLINK <pin> (<interval ms>)"));
    return;
  }
  uint8_t pinNum = constrain(atoi(pos), 0, 64);
  blinky.changePin(pinNum);
  
  Serial.print(F("OK BLINK "));
  Serial.print(pinNum);

  pos = nexttok(args);
  if (pos) {
    uint32_t interval_ms = constrain(atoi(pos), 0, 3600000);
    blinky.changeInterval(interval_ms);
    Serial.print(" ");
    Serial.print(interval_ms);
  }
  Serial.println();
}


void usage_led() {
  Serial.println(F("ERR Usage: LED <num> (ON|OFF|BLINK <ms>|PIN <pin>)"));
}
void cmd_led(char *args) {
  char *pos = firsttok(args);
  if ( ! pos) {
    usage_led();
    return;
  }
  uint8_t ledNum = constrain(atoi(pos), 0, 64);
  if (ledNum > NUM_LEDS) {
    Serial.print(F("ERR led num must be 0.."));
    Serial.println(NUM_LEDS);
  }

  pos = nexttok(args);
  if ( ! pos) {
    usage_led();
    return;
  }
  if (strcasecmp(pos, "OFF") == 0) {
    leds[ledNum].off();
    Serial.print(F("OK LED "));
    Serial.print(ledNum);
    Serial.println(F(" OFF"));

  } else if (strcasecmp(pos, "ON") == 0) {
    leds[ledNum].on();
    Serial.print(F("OK LED "));
    Serial.print(ledNum);
    Serial.println(F(" ON"));

  } else if (strcasecmp(pos, "BLINK") == 0) {
    uint32_t interval_ms = DEFAULT_BLINK_MS;
    pos = nexttok(args);
    if (pos) {
      interval_ms = constrain(atoi(pos), 0, 3600000);
    }
    leds[ledNum].blink(interval_ms);
    Serial.print(F("OK LED "));
    Serial.print(ledNum);
    Serial.println(F(" BLINK"));

  } else if (strcasecmp(pos, "PIN") == 0) {
    pos = nexttok(args);
    if ( ! pos) {
      usage_led();
      return;
    }
    uint8_t pinNum = constrain(atoi(pos), 0, 64);
    leds[ledNum].changePin(pinNum);
    Serial.print(F("OK LED "));
    Serial.print(ledNum);
    Serial.print(F(" PIN "));
    Serial.println(pinNum);
  }
}


void register_commands() {
  lazy.register_callback("OHAI", &cmd_ohai);
  lazy.register_callback("PINOUT", &cmd_pinout);
  lazy.register_callback("BLINK", &cmd_blink);
  lazy.register_callback("LED", &cmd_led);
}


