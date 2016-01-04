#!/bin/bash

ENV=${1:-$(hostname)}
SERVER=${2:-fs18}
HOSTNAME=$ENV-$SERVER.dev.coredial.com
CMD='tail -n 1 /var/log/asterisk/full | cut -d "[" -f 3 | cut -d "]" -f 1' 
ssh -q $HOSTNAME $CMD 2> /dev/null