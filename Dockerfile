  
FROM python:3.8.2

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Create filesystem structures
RUN mkdir /home/model-server
RUN mkdir /home/model-server/model_store

# Copy file
COPY ./requirements.txt /home/model-server/

# Install torch and torchserve
RUN pip install -r /home/model-server/requirements.txt

COPY ./src/mnist.py /home/model-server/
COPY ./src/mnist_handler.py /home/model-server/
COPY ./src/mnist_cnn.pt /home/model-server
COPY ./src/config.properties /home/model-server/
COPY ./src/sh/init_server.sh /home/model-server/
COPY ./src/sh/create_and_add_model.sh /home/model-server/
COPY ./src/sh/run.sh /home/model-server/
COPY ./src/test_data /home/model-server/

# Prepare to start server
RUN chmod +x /home/model-server/run.sh
RUN chmod +x /home/model-server/init_server.sh
RUN chmod +x /home/model-server/create_and_add_model.sh

EXPOSE 8080 8081 8082

WORKDIR /home/model-server/

# Start server and insert model
ENTRYPOINT ["./init_server.sh"]
CMD [ "serve"]