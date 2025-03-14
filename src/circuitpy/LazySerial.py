import usb_cdc

class LazySerial:
  def __init__(self, output=None):
    if output:
      self.output = output
    else:
      self.output = usb_cdc.data
    self.last_serial_state = False


  def init(self):
    self.say("OK STARTING")


  def loop(self):
    self.monitor_connection()
  
  
  def monitor_connection(self):
    if self.last_serial_state:
      if not self.output.connected:
        print("LazySerial: Disconnected!")
    else:
      if self.output.connected:
        print("LazySerial: Connected!")
        self.say("OK CONNECTION ESTABLISHED")
    self.last_serial_state = self.output.connected


  def write(self, what):
    if self.output:
      self.output.write(what)

  def say(self, what):
    self.write(what + "\r\n")
