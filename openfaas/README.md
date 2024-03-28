# Klingon Serial Generator

## Overview

The `klingon-serial` function provides an API to generate unique hexadecimal serial numbers using the `klingon-serial` Python module. It is designed to be deployed as a serverless function.

 ## Components

 - `tests/*`: A directory containing unit tests for the function.
 - `Dockerfile`: The container specification for building the function.
 - `handler.py`: The FastAPI application that serves the function's endpoints.
 - `Makefile`: A set of directives for building and deploying the function.
 - `pytest.ini`: A configuration file for the pytest test runner.
 - `README.md`: The function's documentation.
 - `requirements.txt`: The Python dependencies required by the function.
 - `VERSION`: A file containing the function's version number.

 ## Usage

The `klingon-serial` function is accessible via HTTP and generates a unique
serial number upon each request. 

The serial number is a hexadecimal value composed of the machine's MAC address,
the process ID (PID), and the current time in milliseconds since the epoch.

This document details how to interact with the function's endpoints and how to run and deploy the function.

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


## Running Locally - Development

The function is usually deployed as a docker container on kubernetes or a
serverless hosting platform however when developing it is often faster to run the code
locally.

To run the code locally, run `make run` in the root of the application. This will start the FastAPI application on `http://localhost:8000`

## Build & Deployment
To build the Docker image for the function, run:

 ```bash
 make build
 ```

 After building the image, you can deploy it to Kubernetes or a OpenFaaS cluster using the OpenFaaS CLI.


## Testing
Unit tests are included in the `tests` directory. You can run the tests using the following command:

```bash
make test
```

The following commands demonstrate how to test the function's response in different formats using `curl`. This is useful for verifying that the function behaves as expected and returns the correct content type based on the `Accept` header.

 ```bash
 curl -s -X GET http://localhost:8000/ -H "Accept: application/json"
 ```
 To test plain text response:
 ```bash
 curl -s -X GET http://localhost:8000/ -H "Accept: text/plain"
 ```
 To test XML response:
 ```bash
 curl -s -X GET http://localhost:8000/ -H "Accept: application/xml"
  ```
  To test HTML response:
  ```bash
  curl -s -X GET http://localhost:8000/ -H "Accept: application/html"
  ```
  To test XHTML response:
  ```bash
  curl -s -X GET http://localhost:8000/ -H "Accept: application/xhtml+xml"
  ```
  To test YAML response:
  ```bash
  curl -s -X GET http://localhost:8000/ -H "Accept: application/yaml"
  ```

 ## Contributing

Contributions are welcome, simply submit a PR with your work and an explanation
of the change. Supporting documentation and unit tests must be provided for all PR's
