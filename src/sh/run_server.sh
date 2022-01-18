#!/bin/bash
set -e # exit immediately if there is any error

if [[ "$1" = "serve" ]]; then
    # remove the first argument
    shift 1 
    torch-model-archiver --model-name pill_model --version 1.0 --model-file=/home/model-server/models/KGbased_model.py --serialized-file /home/model-server/pretrain/kg_w_best.pt  --handler /home/model-server/handler/pill_model_handler.py
    # move all .mar files into model store
    mv *.mar ./model_store/
    # start server
    torchserve --ncs --start --ts-config config.properties --model-store ./model_store --models all
else
    eval "$@"
fi

tail -f /dev/null