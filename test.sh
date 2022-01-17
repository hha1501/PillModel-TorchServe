PRETRAIN_DIR=../models/pt_files/
MODEL_DIR=../base-model-updater/models/EncoderDecoder/
HANDLER_FILE=./src/handler/base_model_handler.py

pretrain_lists=$(ls $PRETRAIN_DIR)
model_lists=($(ls $MODEL_DIR))

i=0
for pretrain_file in $pretrain_lists
do 
    IFS='.' read -ra ADDR <<< "$pretrain_file"
    for subpart in "${ADDR[@]}"; do
        if [ "$subpart" != "pt" ]; then
            echo $subpart
            echo "pretrain_file: $PRETRAIN_DIR$pretrain_file"
            echo "model_file: ${model_lists[$i]}"    
            # torch-model-archiver --model-name $subpart --version 1.0 --model-file=${model_lists[$i]} --serialized-file $PRETRAIN_DIR$pretrain_file  --handler $HANDLER_FILE
            i=$((i+1))
        fi
    done
done

# mv *.mar ./model_store/

# torchserve --ncs --start --ts-config config.properties --model-store ./model_store --models daily_predict=daily_predict.mar
