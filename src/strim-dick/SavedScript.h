#pragma once
#include <EEPROM.h>


namespace SavedScript {
  const char lazy_magic_id[] = "LAZY";

  struct EepromHeader {
    char magic[4];
    uint8_t csum;
    uint32_t len;
  };

  class SavedScript {
  public:
    uint32_t d_writePos = 0;
    EepromHeader d_header;
    bool d_saved = false;

    explicit
    SavedScript() {

    }

    void
    init() {
      int length = EEPROM.length();
      EEPROM.get(0, d_header);

      Serial.print(F("EEPROM: "));
      Serial.print(length);
      Serial.println(F(" bytes total."));
      Serial.print(F("SavedScript: "));
      if (strncmp(d_header.magic, lazy_magic_id, 4) != 0) {
        Serial.println(F("Magic number does not match, uninitialised."));
        d_saved = false;
        return;
      }
      uint8_t csum = calcCsum();
      if (csum != d_header.csum) {
        Serial.print(F("Checksum mismatch, "));
        Serial.print(csum, HEX);
        Serial.print(F(" is not the declared "));
        Serial.print(d_header.csum, HEX);
        Serial.println();
        d_saved = false;
        return;
      }
      Serial.print(F("csum="));
      Serial.print(d_header.csum, HEX);
      Serial.print(F(" len="));
      Serial.println(d_header.len);
    }


    uint8_t
    calcCsum() {
      uint32_t pos = sizeof(EepromHeader);
      uint8_t csum = 0;
      for (uint32_t i = 0; i < d_header.len; ++i) {
        if (pos > EEPROM.length()) {
          break;
        }
        csum += EEPROM[pos++];
      }
      return csum;
    }


    void
    beginNewSave() {
      memcpy(d_header.magic, lazy_magic_id, 4);
      d_header.csum = 0;
      d_header.len = 0;
      d_writePos = sizeof(EepromHeader);
    }


    void
    write(char c) {
      EEPROM.update(d_writePos++, c);
      d_header.csum += c;
      d_header.len++;
    }


    void
    write(const char *str) {
      while (*str) {
        write(*str++);
      }
      write('\0');
    }


    void
    finishSave() {
      EEPROM.put(0, d_header);
    }


    uint32_t
    length() {
      return d_header.len;
    }
  
  };
} // namespace
