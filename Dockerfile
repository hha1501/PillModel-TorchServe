  
FROM python:3.8.2

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Create filesystem structures
RUN mkdir /home/model-server
RUN mkdir /home/model-server/model_store

# Copy file
COPY ./fimi-torch-serve/requirements.txt /home/model-server/

# Install torch and torchserve
RUN pip install -r /home/model-server/requirements.txt
RUN mkdir /home/model-server/pretrain
RUN mkdir /home/model-server/handler
RUN mkdir /home/model-server/models 


COPY ./models/pt_files/. /home/model-server/pretrain/
COPY ./fimi-torch-serve/src/handler/. /home/model-server/handler/
COPY ./base-model-updater/models/EncoderDecoder/. /home/model-server/models/
COPY ./fimi-torch-serve/src/config.properties /home/model-server/
COPY ./fimi-torch-serve/src/sh/init_server.sh /home/model-server/
 
# Prepare to start server
RUN chmod +x /home/model-server/init_server.sh

EXPOSE 8080 8081 8082

WORKDIR /home/model-server/

# Start server and insert model
ENTRYPOINT ["./init_server.sh"]
CMD [ "serve"]