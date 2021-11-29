# torch-serve-demo
    Demo for torch serve with docker-compose
    Based on project of torch/serve:
        https://github.com/pytorch/serve

### Download default pretrained model at:
    https://github.com/pytorch/serve/blob/master/examples/image_classifier/mnist/mnist_cnn.pt

## Directory 
    - Dockerfile: run config 
    - config.properties: Default configuration for torch serve
    - handler: Contain preprocessor, postprocessor for each model
    - models: nn.Module layer for models
    - pretrain: Pretrain folder 
    - sh: Bash file on running dockerfile 
    - logs: Logging of model
## Installation 
docker build -t torch_serve:latest .

docker-compose -f torchserve.compose.yml up -d

## Todo 
    - Create directory of pretrained
    - Load and create model for each pretrained 

## How to add new model
- Add new model into src/models
- Add new pretrain model into src/pretrain
- Add new handler for new model in src/handler
- Add new model archiver into src/sh/init_server.py

    E.g: 
    - torch-model-archiver --model-name mnist --version 1.0 --model-file new_model_1.py --serialized-file new_model_1.pt --handler new_model_1_handler.py
    - torch-model-archiver --model-name mnist --version 1.0 --model-file new_model_2.py --serialized-file new_model_2.pt --handler new_model_2_handler.py

- Add newly created model into torchserve --start

    E.g: 
    -   torchserve --start --ncs --ts-config config.properties --model-store model_store --models mnist=mnist.mar new_model_1=new_model_1.mar new_model_2=new_model_2.mar   