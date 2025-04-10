import time

def snooze(ms):
  time.sleep(ms / 1000)

def millis():
  return time.monotonic() * 1000

