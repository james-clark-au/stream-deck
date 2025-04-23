#pragma once

#define BAUD_RATE 9600
#define LAZY_ID "stream-deck 1.0"
#define NUM_LEDS 6
#define NUM_KEYS 6
#define DEFAULT_BLINK_MS 500

#ifdef ARDUINO_AVR_NANO
  // Arduino Nano, using an ATmega328P - tiny and cheap, but can't do native USB
  #define BOARD_NAME "arduino nano"
  #define USB_HID 0
  #define STATUS_LED 13

#else
  #ifdef ARDUINO_AVR_PROMICRO
    // SparkFun Pro Micro, using an ATmega32u4. Commonly used in the keyboard community, this can do USB HID.
    // See https://learn.sparkfun.com/tutorials/pro-micro--fio-v3-hookup-guide/all#windows_boardaddon for setup in the Arduino IDE.
    #define BOARD_NAME "sparkfun pro micro"
    #define USB_HID 1
    #define STATUS_LED 17

  #else
    #error Please edit globals.h to include the correct settings for your board.
  #endif
#endif


#include "BlinkyLed.h"
#include "PushButton.h"
#include "SavedScript.h"
#include "Heartbeat.h"


BlinkyLed::BlinkyLed blinky(STATUS_LED, 500);
BlinkyLed::BlinkyLed leds[NUM_LEDS];

PushButton::PushButton keys[NUM_KEYS];

SavedScript::SavedScript saved;

Heartbeat::Heartbeat heart(10000);  // 10s


