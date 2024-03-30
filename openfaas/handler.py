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
from klingon_serial.generate import generate_serial
from klingon_serial.generate import is_valid_serial
from starlette.responses import Response as StarletteResponse
from typing import Optional
import uvicorn

import yaml

class XMLResponse(Response):
    media_type = "application/xml"

class YAMLResponse(Response):
    media_type = "application/yaml"

app = FastAPI()

response_types = {  # Define the possible response types and their descriptions
    "application/json": {"description": "JSON response"},
    "text/plain": {"description": "Plain text response"},
    "text/html": {"description": "HTML response"},
    "application/xml": {"description": "XML response"},
    "application/xhtml+xml": {"description": "XHTML response"},
    "application/yaml": {"description": "YAML response"},
}

@app.get("/health")
async def health():
    """
    This endpoint does two things:
    - Ensures that the klingon-serial library is working and can generate a valid serial
    number using the is_valid_serial function. This step is a functional test of
    the library itself.
    - Ensures that the / http endpoint is working and returns a 200 status code with
    a valid serial number in the response body. This step should be considered
    as an end to end test of the library and the fastAPI server, as it will
    actually make an API call to the / endpoint and check the response.

    In the event that anything doesn't work, the exception should be caught and
    dumped to the result as a string and a 500 error should be returned.
    """
    try:
        client = TestClient(app)
        response = client.get("/", headers={"Accept": "application/json"})
        if response.status_code == 200 and "serial" in response.json():
            return {"status": "ok"}
        else:
            raise Exception("The / endpoint did not return a valid response.")
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/favicon.ico")
async def favicon():
    # Endpoint to serve the favicon; returns a 204 No Content response as there is no favicon.
    return Response(content="", media_type="image/x-icon", status_code=204)


@app.get("/", responses={  # Update the responses parameter to use proper status codes
    "200": {
        "description": "Successful Response",
        "content": {
            "application/json": {"example": {"serial": "123ABC"}},
            "text/plain": {"example": "123ABC"},
            "text/html": {"example": "<p>123ABC</p>"},
            "application/xml": {"example": "<serial>123ABC</serial>"},
            "application/xhtml+xml": {"example": "<p>123ABC</p>"},
            "application/yaml": {"example": "serial: 123ABC"},
        },
    },
    "406": {
        "description": "Not Acceptable",
        "content": {
            "application/json": {"example": {"error": "Unsupported Accept header"}},
        },
    },
})
async def root(accept: Optional[str] = Header(None)):
    # Root endpoint that generates and returns a unique serial number in the requested format.
    # The Accept header determines the response content type: JSON, plain text, HTML, XML, or XHTML.
    # If the Accept header is not supported, it returns a 406 Not Acceptable with an error message.
    unique_serial = generate_serial().upper()
    data = {"serial": unique_serial}
    # Check if 'Accept' is provided as a query parameter and override the header value
    accept_header = accept or ""
    if accept_header:
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
