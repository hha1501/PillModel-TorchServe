  
FROM python:3.8.2

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Create filesystem structures
RUN mkdir /home/model-server
RUN mkdir /home/model-server/model_store

# Copy file
COPY requirements.txt /home/model-server/

# Install torch and torchserve
RUN pip install -r /home/model-server/requirements.txt
RUN mkdir /home/model-server/pretrain
RUN mkdir /home/model-server/handler
RUN mkdir /home/model-server/models 

COPY src/checkpoints/. /home/model-server/pretrain/
COPY src/handler/. /home/model-server/handler/
COPY src/models/*.py /home/model-server/models/
COPY src/config.properties /home/model-server/
COPY src/sh/run_server.sh /home/model-server/
COPY src/checkpoints/index_to_name.json /home/model-server/
 
# Prepare to start server
RUN chmod +x /home/model-server/run_server.sh

EXPOSE 8080 8081 8082

WORKDIR /home/model-server/

# Start server and insert model
ENTRYPOINT ["./run_server.sh"]
CMD [ "serve"]