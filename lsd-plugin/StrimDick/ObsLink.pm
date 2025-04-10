package LazyCat::LazySerial::Handler::StrimDick::ObsLink;
use Mojo::Base 'Mojo::EventEmitter', -signatures;

use Mojo::WebSocket 'WS_PING';
use Mojo::AsyncAwait;
use Mojo::Promise;
use Mojo::UserAgent;
use Mojo::JSON qw/decode_json encode_json/;
use Term::ANSIColor;
use List::MoreUtils qw/firstidx/;
use Carp;
use Digest::SHA 'sha256_base64';


has secret => "Oh-BS!";
has url => "ws://localhost:4455";
has debug => 1;
has ua => sub { Mojo::UserAgent->new };
has tx => undef;  # Mojo::Transaction::Websocket
has attempt => 0;
has keepalive_tid => undef;
has log_to_stderr => 1;


# Synced from OBS
has scenes => sub { [] };

# Hash of id => Promise
has pending_requests => sub { {} };


my @OPCODES = qw/Hello Identify Identified Reidentify 4 Event Request RequestResponse RequestBatch RequestBatchResponse/;
sub opcode_by_name($name) {
  my $opcode = firstidx { lc $_ eq lc $name } @OPCODES;
  croak "Attempt to reference unknown opcode by name '$name'!" if $opcode == -1;
  return $opcode;
}

my @EVENTSUBS = qw/General Config Scenes Inputs Transitions Filters Outputs SceneItems MediaInputs Vendors Ui 11 12 13 14 15 InputVolumeMeters InputActiveStateChanged InputShowStateChanged/;
sub eventsub_by_name($name) {
  my $eventsub_idx = firstidx { lc $_ eq lc $name } @EVENTSUBS;
  croak "Attempt to reference unknown eventsub ID by name '$name'!" if $eventsub_idx == -1;
  return 1 << $eventsub_idx;
}
sub eventsubs_mask(@events) {
  my $mask = 0;
  foreach my $event (@events) {
    $mask |= eventsub_by_name($event);
  }
  return $mask;
}


sub next_id() {
  state $id = 1;
  return $id++;
}


sub log($self, @what) {
  $self->emit(log => join(' ', @what));
  say STDERR colored("[OBS]", 'bold bright_green') . " " . colored(join(' ', @what), 'green') if $self->log_to_stderr;
}


sub connect ($self) {
  my $tx = $self->ua->build_websocket_tx($self->url);
  $tx->req->headers->header('Sec-WebSocket-Extensions' => 'permessage-deflate');
  $tx->req->headers->header('Sec-WebSocket-Protocol' => 'obswebsocket.json');

  $self->ua->start($tx, sub ($ua, $tx) {
    if (my $err = $tx->req->error || $tx->res->error || $tx->error) {
      if ($err->{message} =~ /Connection refused/i && $self->attempt > 0) {
        # Suppress log to avoid spam
      } else {
        $self->log("Websocket error: " . ($err->{code} // '') . " " . $err->{message} );
      }
      $self->reconnect();
      return;
    }
    unless ($tx && $tx->is_websocket) {
      $self->log("Websocket handshake to " . $self->url . " failed!");
      $self->reconnect();
      return;
    }

    # $tx is now assuredly an active Mojo::Transaction::WebSocket rather than a Mojo::Transaction::HTTP.
    $self->tx($tx);

    # Set up callbacks
    $tx->on(finish => sub ($tx, $code, $reason) {
      $reason //= 'unknown';
      $self->log("Websocket closed with status $code: $reason.");
      $self->emit('disconnected', $code, $reason);
      $self->tx(undef);
      $self->reconnect();
    });
    $tx->on(message => sub ($tx, $rawmsg) {
      $self->handle_message($rawmsg);
    });

    # Keep the connection alive
    my $tid = Mojo::IOLoop->recurring(2, sub ($loop) {
      $self->ping();
    });
    $self->keepalive_tid($tid);
    $self->ping();

  });
};


sub ping($self) {
  return unless $self->tx;
  $self->tx->send([1, 0, 0, 0, WS_PING, 'PING']);
}


sub reconnect($self) {
  my $seconds = ($self->attempt + 1) ** 2;
  $seconds = 10 if $seconds > 10;
  $self->log("Reconnecting in ${seconds}s...") unless $self->attempt > 5;
  Mojo::IOLoop->timer($seconds => sub ($loop) {
    $self->attempt($self->attempt + 1);
    $self->attempt(10) if $self->attempt > 10;
    $self->connect();
  });
}


sub handle_message($self, $rawmsg) {
  my $msg = decode_json $rawmsg;
  if ( ! defined $msg->{op}) {
    $self->log("received message without an opcode: $rawmsg");
    return;
  }
  my $opcode = $msg->{op};
  my $opname = $OPCODES[$opcode] // "UNKNOWN";
  $self->log("==> [$opcode $opname] $rawmsg");
  return $self->handle_hello($msg->{d}) if $opname eq 'Hello';
  return $self->handle_identified($msg->{d}) if $opname eq 'Identified';
  return $self->handle_event($msg->{d}) if $opname eq 'Event';
  return $self->handle_request_response($msg->{d}) if $opname eq 'RequestResponse';
}


sub handle_hello($self, $data) {
  $self->log("Connecting with OBS websocket version " . $data->{obsWebSocketVersion});
  my $authentication;
  if ($data->{authentication}) {
    $authentication = $self->challenge_response_b64(
      $data->{authentication}->{challenge},
      $data->{authentication}->{salt},
    );
  } else {
    $self->log("No authentication required? okay?");
  }
  my $mask = eventsubs_mask(qw/General Config Scenes Outputs/);
  $self->send_identify($authentication, $mask);
}


sub handle_identified($self, $data) {
  $self->log("Identified!");
  $self->emit("ready");
  $self->attempt(0);
}


sub handle_event($self, $data) {
  my $event = $data->{eventType};
  my $event_data = $data->{eventData};
  $self->log("Event: $event " . encode_json($event_data));
  $self->emit(event => $event, $event_data);
}


sub handle_request_response($self, $data) {
  my $request = $data->{requestType};
  my $id = $data->{requestId};
  my $status = $data->{requestStatus};
  my $rdata = $data->{responseData};
  my $promise = $self->pending_requests->{$id};
  delete $self->pending_requests->{$id};

  if ( ! $status->{result}) {
    my $reason = "Code: " . $status->{code};
    $reason .= " (" . $status->{comment} . ")" if $status->{comment};
    $self->log("Request #$id $request failed, $reason");
    $promise->reject($reason) if $promise;
    return;
  }
  $promise->resolve($rdata) if $promise;
  return $rdata;
}


sub challenge_response_b64($self, $challenge_b64, $salt_b64) {
  my $shasum_b64 = sha256_base64($self->secret, $salt_b64);
  $shasum_b64 .= "=" while length($shasum_b64) % 4;  # See perldoc Digest::SHA
  my $response_b64 = sha256_base64($shasum_b64, $challenge_b64);
  $response_b64 .= "=" while length($response_b64) % 4;
  return $response_b64;
}


sub send_identify($self, $authentication, $subscriptions) {
  croak "Can't send Identify, not connected!" unless $self->tx;
  my $opcode = opcode_by_name('Identify');
  my $msg = {
    op => $opcode,
    d => {
      rpcVersion => 1,
      eventSubscriptions => $subscriptions,
    },
  };
  $msg->{d}->{authentication} = $authentication if $authentication;
  my $json = encode_json $msg;
  $self->log("<== [$opcode Identify] $json");
  $self->tx->send($json);
}


async send_request_p => sub ($self, $request, $data) {
  croak "Can't send Request $request, not connected!" unless $self->tx;
  my $opcode = opcode_by_name('Request');
  my $id = next_id();
  my $msg = {
    op => $opcode,
    d => {
      requestType => $request,
      requestId => $id,
      requestData => $data,
    },
  };
  my $json = encode_json $msg;
  $self->log("<== [$opcode Request] $json");
  $self->pending_requests->{$id} = Mojo::Promise->timeout(10 => "OBS Request $id $request timed out.");
  $self->tx->send($json);
  return $self->pending_requests->{$id};
};


sub send_request($self, $request, $data) {
  # Fire and forget
  $self->send_request_p($request, $data)->catch(sub ($err) {
    $self->log("[ERR] send_request($request) failed with no error handler set: $err");
  });
}


async sync_p => sub ($self) {
  #my $res = await $self->obs->
};

1;
