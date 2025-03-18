# LazySerial command console.
# You need to connect to /dev/ttyACM1, 9600 baud, line endings CR/LF or just LF, and pull DTR high.
import usb_cdc

def cmd_help(lazy, args):
  lazy.say("ERR Available commands: " + " ".join(lazy.commands.keys()))

class LazySerial:
  def __init__(self, serial=None):
    if serial:
      self.serial = serial
    else:
      self.serial = usb_cdc.data
    self.last_serial_state = False
    self.commands = {
      'HELP': cmd_help,
    }
    self.buf = ""
    

  def init(self):
    if self.serial:
      self.serial.timeout = 0.01
      self.serial.write_timeout = 0.01
    else:
      print("LazySerial: Warning, no serial defined!\n");
    self.say("OK STARTING")


  def register(self, cmdname, callback):
    self.commands[cmdname.upper()] = callback


  def loop(self):
    self.monitor_connection()
    self.read_buf()
    
  
  def monitor_connection(self):
    if self.last_serial_state:
      if not self.serial.connected:
        print("LazySerial: Disconnected!\n")
    else:
      if self.serial.connected:
        print("LazySerial: Connected!\n")
        self.say("OK CONNECTION ESTABLISHED")
    self.last_serial_state = self.serial.connected


  def read_buf(self):
    read_bytes = self.serial.read()
    for ch in read_bytes.decode():
      if ch == "\n":
        cmdstring = self.buf
        self.buf = ""
        self.dispatch_command(cmdstring)
      elif ch == "\r":
        pass  # do nothing, bloody python
      else:
        self.buf = self.buf + ch
  
  
  def dispatch_command(self, cmdstring):
    args = cmdstring.split()
    cmdname = args.pop(0) if len(args) else ''  # this is 'shift' in normal languages, with a pythony-ternary to protect against IndexError
    if cmdname.upper() in self.commands:  # motherfucking python
      self.commands[cmdname.upper()](self, args)
    else:
      cmd_help(self, args)
      

  def write(self, what):
    if self.serial:
      self.serial.write(what)

  def say(self, what):
    self.write(what + "\r\n")
