package LazyCat::LazySerial::Handler::StrimDick::Protocol;
use Mojo::Base -base, -signatures;

use Carp;
use Cwd;

use List::MoreUtils qw/firstidx/;


# Message Types or 'opcodes'
# https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#message-types-opcodes
my @OPCODES = qw/Hello Identify Identified Reidentify UNK_OP_4 Event Request RequestResponse RequestBatch RequestBatchResponse/;
sub opcode_id_by_name($self, $name) {
  my $opcode = firstidx { lc $_ eq lc $name } @OPCODES;
  croak "Attempt to reference unknown opcode by name '$name'!" if $opcode == -1;
  return $opcode;
}
sub opcode_name_by_id($self, $id) {
  my $name = $OPCODES[$id];
  croak "Attempt to reference unknown opcode by id '$id'!" unless defined $name;
  return $name;
}


# EventSubscription types
# https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#eventsubscription
my @EVENTSUBS = qw/
  General Config Scenes Inputs Transitions Filters Outputs SceneItems MediaInputs Vendors
  Ui UNK_ES_11 UNK_ES_12 UNK_ES_13 UNK_ES_14 UNK_ES_15 InputVolumeMeters InputActiveStateChanged InputShowStateChanged
  /;
sub eventsub_id_by_name($self, $name) {
  my $eventsub_idx = firstidx { lc $_ eq lc $name } @EVENTSUBS;
  croak "Attempt to reference unknown eventsub ID by name '$name'!" if $eventsub_idx == -1;
  return 1 << $eventsub_idx;
}

# Construct EventSubscription bitmask from a list of named events to track.
sub eventsubs_mask($self, @events) {
  my $mask = 0;
  foreach my $event (@events) {
    $mask |= $self->eventsub_id_by_name($event);
  }
  return $mask;
}


1;
