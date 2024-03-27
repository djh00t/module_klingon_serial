"""
handler.py

This module defines the FastAPI application that serves as the OpenFaaS function for generating unique hexadecimal serial numbers.
It includes endpoints for generating serial numbers in various formats based on the Accept header of the request.

The module uses the `klingon_serial` Python module to generate the serial numbers and defines custom response classes to handle
different content types.

It can be run standalone using Uvicorn for local development and testing purposes.
"""

from fastapi import FastAPI, Header
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from klingon_serial import generate_serial
from starlette.responses import Response
from typing import Optional
import uvicorn


class XMLResponse(Response):
    media_type = "application/xml"

app = FastAPI()

@app.get("/favicon.ico")
async def favicon():
    # Endpoint to serve the favicon; returns a 204 No Content response as there is no favicon.
    return Response(content="", media_type="image/x-icon", status_code=204)


@app.get("/")
async def root(accept: Optional[str] = Header(None)):
    # Root endpoint that generates and returns a unique serial number in the requested format.
    # The Accept header determines the response content type: JSON, plain text, HTML, XML, or XHTML.
    # If the Accept header is not supported, it returns a 406 Not Acceptable with an error message.
    unique_serial = generate_serial().upper()
    data = {"serial": unique_serial}
    if accept:
        if "application/json" in accept:
            return JSONResponse(content=data)
        elif "text/plain" in accept:
            return PlainTextResponse(unique_serial)
        elif "text/html" in accept:
            html_content = f'<html><body><p>{unique_serial}</p></body></html>'
            return HTMLResponse(content=html_content)
        elif "application/xml" in accept or "text/xml" in accept:
            xml_content = f'<root><serial>{unique_serial}</serial></root>'
            return XMLResponse(content=xml_content)
        elif "application/xhtml+xml" in accept:
            xhtml_content = f'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Serial Number</title></head><body><p>{unique_serial}</p></body></html>'
            return HTMLResponse(content=xhtml_content)
        else:
            accepted_formats = "application/json, text/plain, text/html, application/xml, text/xml, application/xhtml+xml"
            error_data = {
                "error": "Unsupported Accept header",
                "accepted_formats": [
                    "application/json",
                    "text/plain",
                    "text/html",
                    "application/xml",
                    "text/xml",
                    "application/xhtml+xml"
                ]
            }
            return JSONResponse(content=error_data, status_code=406)
    # Default to JSON response
    return JSONResponse(content=data)

if __name__ == "__main__":
    # If run as the main module, start the Uvicorn server to serve the FastAPI application.
    uvicorn.run("openfaas.handler:app", host="0.0.0.0", port=8000, reload=True)

