#!/bin/bash
set -e

if [[ "$1" = "serve" ]]; then
    shift 1
    torch-model-archiver --model-name mnist --version 1.0 --model-file mnist.py --serialized-file mnist_cnn.pt --handler mnist_handler.py
    mv mnist.mar ./model_store/
    torchserve --start --ncs --ts-config config.properties --model-store model_store --models mnist=mnist.mar    
else
    eval "$@"
fi

tail -f /dev/null