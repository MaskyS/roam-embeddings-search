Docker
Chroma Cloud

Chroma Cloud, our fully managed hosted service is here. Sign up for free.

Run Chroma in a Docker Container#
You can run a Chroma server in a Docker container, and access it using the HttpClient. We provide images on both docker.com and ghcr.io.

To start the server, run:


docker run -v ./chroma-data:/data -p 8000:8000 chromadb/chroma
This starts the server with the default configuration and stores data in ./chroma-data (in your current working directory).

The Chroma client can then be configured to connect to the server running in the Docker container.


import chromadb

chroma_client = chromadb.HttpClient(host='localhost', port=8000)
chroma_client.heartbeat()
Client-only package

If you're using Python, you may want to use the client-only package for a smaller install size.

Configuration#
Chroma is configured using a YAML file. Check out this config file detailing all available options.

To use a custom config file, mount it into the container at /config.yaml like so:


echo "allow_reset: true" > config.yaml # the server will now allow clients to reset its state
docker run -v ./chroma-data:/data -v ./config.yaml:/config.yaml -p 8000:8000 chromadb/chroma
Observability with Docker#
Chroma is instrumented with OpenTelemetry hooks for observability. OpenTelemetry traces allow you to understand how requests flow through the system and quickly identify bottlenecks. Check out the observability docs for a full explanation of the available parameters.

Here's an example of how to create an observability stack with Docker Compose. The stack is composed of

a Chroma server
OpenTelemetry Collector
Zipkin
First, paste the following into a new file called otel-collector-config.yaml:


receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

exporters:
  debug:
  zipkin:
    endpoint: "http://zipkin:9411/api/v2/spans"

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [zipkin, debug]
This is the configuration file for the OpenTelemetry Collector:

The receivers section specifies that the OpenTelemetry protocol (OTLP) will be used to receive data over GRPC and HTTP.
exporters defines that telemetry data is logged to the console (debug), and sent to a zipkin server (defined below in docker-compose.yml).
The service section ties everything together, defining a traces pipeline receiving data through our otlp receiver and exporting data to zipkin and via logging.
Next, paste the following into a new file called docker-compose.yml:


services:
  zipkin:
    image: openzipkin/zipkin
    ports:
      - "9411:9411"
    depends_on: [otel-collector]
    networks:
      - internal
  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.111.0
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ${PWD}/otel-collector-config.yaml:/etc/otel-collector-config.yaml
    networks:
      - internal
  server:
    image: chromadb/chroma
    volumes:
      - chroma_data:/data
    ports:
      - "8000:8000"
    networks:
      - internal
    environment:
      - CHROMA_OPEN_TELEMETRY__ENDPOINT=http://otel-collector:4317/
      - CHROMA_OPEN_TELEMETRY__SERVICE_NAME=chroma
    depends_on:
      - otel-collector
      - zipkin

networks:
  internal:

volumes:
  chroma_data:
To start the stack, run


docker compose up --build -d
Once the stack is running, you can access Zipkin at http://localhost:9411 when running locally to see your traces.

Zipkin will show an empty view initially as no traces are created during startup. You can call the heartbeat endpoint to quickly create a sample trace:


curl http://localhost:8000/api/v2/heartbeat
Then, click "Run Query" in Zipkin to see the trace.