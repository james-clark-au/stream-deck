package LazyCat::LazySerial::Handler::StrimDick;
use Mojo::Base 'LazyCat::LazySerial::Handler', -signatures;

use LazyCat::LazySerial::Heartbeat;


has debug => 0;
has heartbeat => sub { LazyCat::LazySerial::Heartbeat->new(rate_s => 60) };

my %HARDCODED_CONFIG = (
  "5-CLICKED" => "Card: Just Chatting",
  "5-HELD"    => "Card: Starting Soon",
  "4-CLICKED" => "Card: Just Catting",
  "3-CLICKED" => "Game: Ultima 9",
  "3-HELD"    => "Game: Serpent Isle",
  "2-CLICKED" => "Game: Generic Fullscreen",
  "1-CLICKED" => "Card: BRB",
  "1-HELD"    => "Card: Technical Difficulties",
  "0-CLICKED" => "Card: Stream Ended",
);


sub init($self) {
  $self->log("init()");
  return 1;
}


sub matches_usb_ids($self, $device) {
  return 1 if $device->usb_id eq '0403:6001' && $device->driver eq 'ftdi_sio';
  return 1 if $device->usb_id eq '1a86:7523' && $device->driver eq 'ch341';
  return 0;
}


sub matches_lazy_id($self, $device) {
  return 1 if $device->lazy_id eq 'strim-dick';
  return 0;
}


sub matches_lazy_version($self, $device) {
  return 1 if $device->lazy_version >= 1.0 && $device->lazy_version < 2.0;
  return 0;
}


# input from the LazySerial device
sub handle_input($self, $line) {
  if ($line =~ /^INPUT KEY (\d+) (\w+)$/) {
    my $key = $1;  # 0..5
    my $act = $2;  # CLICKED or HELD
    if ($HARDCODED_CONFIG{"$key-$act"}) {
      my $scene = $HARDCODED_CONFIG{"$key-$act"};
      $self->log("$line - scene $scene");
    } else {
      $self->log("$line - no binding");
    }

  } elsif ($line =~ /^OK/) {
    # No need to log
  } else {
    $self->log("unknown input: $line");
  }
}


sub connected($self) {
  $self->log("connected()") if $self->debug;
  $self->device->send("EYECATCH");

#  $self->heartbeat->handler($self);
#  $self->heartbeat->resume_fn(sub { $self->device->send("EYECATCH"); $self->set_light(); });
#  $self->heartbeat->enable();
#  $self->heartbeat->beat();
}



sub disconnected($self) {
  $self->log("disconnected()") if $self->debug;
  $self->heartbeat->stop();
}


# ----

# Set light according to OBS scene
sub set_light($self) {
}


1;
