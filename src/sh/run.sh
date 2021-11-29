#!/bin/bash

# Start server
torchserve --start \
           --ncs \
           --ts-config config.properties \
           --model-store model-store \
           --models mnist=mnist.mar

# Do not close container
tail -f /dev/null