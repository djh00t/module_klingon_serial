 # OpenFaaS Function: Klingon Serial Generator

## Overview

This OpenFaaS function provides an API to generate unique hexadecimal serial numbers using the `klingon_serial` Python module. It is designed to be deployed as a serverless function within the OpenFaaS framework.

 ## Components

 - `wrapper.py`: The FastAPI application that serves the function's endpoints.
 - `handler.py`: The handler that generates the serial number.
 - `Dockerfile`: The container specification for building the function.
 - `requirements.txt`: The Python dependencies required by the function.

 ## Usage

The function is accessible via HTTP and generates a unique serial number upon each request. The serial number is composed of the machine's MAC address, the process ID (PID), and the current time in milliseconds since the epoch. This document details how to interact with the function's endpoints and how to run and deploy the function.

 The function exposes an HTTP endpoint that returns a unique serial number when accessed. The serial number is a concatenation of the machine's MAC address, the process ID (PID), and the current time in epoch format with millisecond precision.

 ## Endpoints

 - `/`: The root endpoint that returns the serial number in whatever format you
   request using the `Accept` header.
   Available formats are:
    - `application/json`
    - `text/plain`
    - `application/xml`
    - `application/html`
    - `application/xhtml+xml`
    - `application/yaml`
 - `/docs`: The Swagger UI documentation for the function.
 - `/favicon.ico`: An endpoint to serve the favicon.
 - `/health`: A health check endpoint that returns a 200 OK status code if the
   function is running.
 - `docs`: The Swagger UI documentation for the function.

 ## Running Locally

To facilitate local development and testing, instructions are provided for running the function using `uvicorn`, a lightning-fast ASGI server. This allows developers to test changes before deploying them to a live OpenFaaS environment.

 To run the function locally, you can use `make run`:

 ```bash
 make run
 ```

 ## Deployment


Deployment instructions guide you through building the Docker container image for the function and deploying it to an OpenFaaS cluster using the OpenFaaS CLI. This ensures that the function is properly containerized and managed within the serverless framework.


To deploy the function to an OpenFaaS cluster, you can use the provided `Dockerfile` to build the container image and then use the OpenFaaS CLI to deploy it.

 ## Testing

 You can test the function by sending HTTP requests to the deployed function's endpoint. For example, using `curl`:

To test JSON response (default):

 The following commands demonstrate how to test the function's response in different formats using `curl`. This is useful for verifying that the function behaves as expected and returns the correct content type based on the `Accept` header.


 ```bash
 curl http://<openfaas-gateway-url>/function/klingon-serial
 ```
 To test plain text response:
 ```bash
 curl -H "Accept: text/plain" http://<openfaas-gateway-url>/function/klingon-serial
 ```
 To test XML response:
 ```bash
 curl -H "Accept: application/xml" http://<openfaas-gateway-url>/function/klingon-serial
 ```

 ## Contributing

Contributions are encouraged, and this section outlines the expectations for contributing to the function's codebase. It emphasizes the importance of maintaining documentation and tests alongside code changes.

## Contributing

 Contributions to the function are welcome. Please ensure that any changes are accompanied by corresponding updates to the documentation and tests.
