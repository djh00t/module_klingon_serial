"""
handler.py

This module defines the FastAPI application that serves as the OpenFaaS function for generating unique hexadecimal serial numbers.
It includes endpoints for generating serial numbers in various formats based on the Accept header of the request.

The module uses the `klingon_serial` Python module to generate the serial numbers and defines custom response classes to handle
different content types.

It can be run standalone using Uvicorn for local development and testing purposes.
"""

from fastapi import FastAPI, Header, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.responses import YAMLResponse as FastAPIYAMLResponse
from klingon_serial import generate_serial
from starlette.responses import Response as StarletteResponse
from typing import Optional
import uvicorn

import yaml

class XMLResponse(Response):
    media_type = "application/xml"

class YAMLResponse(Response):
    media_type = "application/yaml"

app = FastAPI()

response_types = {
    "application/json": {"description": "JSON response"},
    "text/plain": {"description": "Plain text response"},
    "text/html": {"description": "HTML response"},
    "application/xml": {"description": "XML response"},
    "application/xhtml+xml": {"description": "XHTML response"},
    "application/yaml": {"description": "YAML response"},
}

@app.get("/health")
async def health():
    ...

@app.get("/favicon.ico")
async def favicon():
    ...
    # Health check endpoint; returns a 200 OK response to indicate the service is up and running.
    return PlainTextResponse("OK", status_code=200)

@app.get("/favicon.ico")
async def favicon():
    # Endpoint to serve the favicon; returns a 204 No Content response as there is no favicon.
    return Response(content="", media_type="image/x-icon", status_code=204)


@app.get("/", responses=response_types)
async def root(accept: Optional[str] = Header(None, alias='Accept', include_in_schema=True)):
    ...
    # Root endpoint that generates and returns a unique serial number in the requested format.
    # The Accept header determines the response content type: JSON, plain text, HTML, XML, or XHTML.
    # If the Accept header is not supported, it returns a 406 Not Acceptable with an error message.
    unique_serial = generate_serial().upper()
    data = {"serial": unique_serial}
    # Check if 'Accept' is provided as a query parameter and override the header value
    if accept:
        if "application/json" in accept:
            return JSONResponse(content=data)
        elif "text/plain" in accept:
            return PlainTextResponse(unique_serial)
        elif "text/html" in accept:
            html_content = f'<html><body><p>{unique_serial}</p></body></html>'
            return HTMLResponse(content=html_content)
        elif "application/xml" in accept:
            xml_content = f'<root><serial>{unique_serial}</serial></root>'
            return XMLResponse(content=xml_content)
        elif "application/xhtml+xml" in accept:
            xhtml_content = f'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Serial Number</title></head><body><p>{unique_serial}</p></body></html>'
            return HTMLResponse(content=xhtml_content)
        elif "application/yaml" in accept:
            yaml_content = yaml.dump(data)
            return YAMLResponse(content=yaml_content)
    raise HTTPException(status_code=406, detail="Unsupported Accept header")

if __name__ == "__main__":
    import pytest
    # Run the pytest suite before starting the server
    test_exit_code = pytest.main(['-v'])
    if test_exit_code != 0:
        # If tests fail, exit with the test exit code
        import sys
        sys.exit(test_exit_code)
    # If run as the main module, start the Uvicorn server to serve the FastAPI application.
    uvicorn.run("openfaas.handler:app", host="0.0.0.0", port=8000, reload=True)
