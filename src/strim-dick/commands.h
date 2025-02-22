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


void led_only(uint8_t ledNum) {
  for (uint8_t i = 0; i < NUM_LEDS; ++i) {
    if (i == ledNum) {
      leds[i].on();
    } else {
      leds[i].off();
    }
  }
}


void led_clear() {
  for (uint8_t i = 0; i < NUM_LEDS; ++i) {
    leds[i].off();
  }
}


void usage_led() {
  Serial.println(F("ERR Usage: LED <num> (ON|OFF|ONLY|BLINK <ms>|PIN <pin>)"));
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

  } else if (strcasecmp(pos, "ONLY") == 0) {
    led_only(ledNum);
    Serial.print(F("OK LED "));
    Serial.print(ledNum);
    Serial.println(F(" ONLY"));

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


void cmd_clear(char *args) {
  led_clear();
  Serial.println(F("OK CLEAR"));
}


void usage_key() {
  Serial.println(F("ERR Usage: KEY <num> PIN <pin>"));
}
void cmd_key(char *args) {
  char *pos = firsttok(args);
  if ( ! pos) {
    usage_key();
    return;
  }
  uint8_t keyNum = constrain(atoi(pos), 0, 64);
  if (keyNum > NUM_KEYS) {
    Serial.print(F("ERR key num must be 0.."));
    Serial.println(NUM_KEYS);
  }

  pos = nexttok(args);
  if ( ! pos) {
    usage_key();
    return;
  }
  if (strcasecmp(pos, "PIN") == 0) {
    pos = nexttok(args);
    if ( ! pos) {
      usage_key();
      return;
    }
    uint8_t pinNum = constrain(atoi(pos), 0, 64);
    keys[keyNum].changePin(pinNum);
    Serial.print(F("OK KEY "));
    Serial.print(keyNum);
    Serial.print(F(" PIN "));
    Serial.println(pinNum);
  }
}


void cmd_save(char *args) {
  saved.beginNewSave();
  for (uint8_t i = 0; i < NUM_LEDS; ++i) {
    if (leds[i]) {
      String cmd;
      cmd.reserve(14);
      cmd += "LED ";
      cmd += String(i);
      cmd += " PIN ";
      cmd += String(leds[i].pin());
      cmd += "\n";
      saved.write(cmd.c_str());
    }
  }
  for (uint8_t i = 0; i < NUM_KEYS; ++i) {
    if (keys[i]) {
      String cmd;
      cmd.reserve(14);
      cmd += "KEY ";
      cmd += String(i);
      cmd += " PIN ";
      cmd += String(keys[i].pin());
      cmd += "\n";
      saved.write(cmd.c_str());
    }
  }
  saved.finishSave();
  Serial.print(F("OK SAVE script len="));
  Serial.println(saved.length());
}


void cmd_eyecatch(char *args) {
  int which = args ? atoi(args) : 0;
  if (which == 1) {
    for (int i = 0; i < NUM_LEDS; ++i) {
      led_only(i);
      delay(20);
    }
    led_only(-1);
  } else {
    for (int i = NUM_LEDS - 1; i >= 0; --i) {
      led_only(i);
      delay(20);
    }
    led_clear();
  }
  Serial.println(F("OK EYECATCH"));
}


void cmd_heartbeat(char *args) {
  if (strcasecmp(args, "ON") == 0) {
    heart.setEnabled(true);
    Serial.println(F("OK HEARTBEAT ON"));

  } else if (strcasecmp(args, "OFF") == 0) {
    heart.setEnabled(false);
    Serial.println(F("OK HEARTBEAT OFF"));

  } else {
    heart.beat();
    if (args) {
      Serial.println(F("OK HEARTBEAT"));
    }
  }
}



void register_commands() {
  lazy.register_callback("OHAI", &cmd_ohai);
  lazy.register_callback("PINOUT", &cmd_pinout);
  lazy.register_callback("BLINK", &cmd_blink);
  lazy.register_callback("LED", &cmd_led);
  lazy.register_callback("CLEAR", &cmd_clear);
  lazy.register_callback("KEY", &cmd_key);
  lazy.register_callback("SAVE", &cmd_save);
  lazy.register_callback("EYECATCH", &cmd_eyecatch);
  lazy.register_callback("HEARTBEAT", &cmd_heartbeat);
}


