#!/bin/bash
set -e # exit immediately if there is any error

if [[ "$1" = "serve" ]]; then
    # remove the first argument
    shift 1 
    
    # archieve all models in path
    PRETRAIN_DIR=/home/model-server/pretrain/
    MODEL_DIR=/home/model-server/models/
    HANDLER_FILE=/home/model-server/handler/base_model_handler.py

    pretrain_lists=$(ls $PRETRAIN_DIR)
    model_lists=( $(find $MODEL_DIR -maxdepth 1 -not -type d) )

    i=0
    for pretrain_file in $pretrain_lists
    do 
        IFS='.' read -ra ADDR <<< "$pretrain_file"
        for subpart in "${ADDR[@]}"; do
            if [ "$subpart" != "pt" ]; then
                echo $subpart
                echo "pretrain_file: $PRETRAIN_DIR$pretrain_file"
                echo "model_file: ${model_lists[$i]}"    
                torch-model-archiver --model-name $subpart --version 1.0 --model-file=${model_lists[$i]} --serialized-file $PRETRAIN_DIR$pretrain_file  --handler $HANDLER_FILE
                i=$((i+1))
            fi
        done
    done

    # move all .mar files into model store
    mv *.mar ./model_store/
    # start server
    torchserve --ncs --start --ts-config config.properties --model-store ./model_store --models all
else
    eval "$@"
fi

tail -f /dev/null