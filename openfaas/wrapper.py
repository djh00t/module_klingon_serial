from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from klingon_serial import generate_serial
from starlette.responses import Response
from typing import Optional
import uvicorn


class XMLResponse(Response):
    media_type = "application/xml"



app = FastAPI()


@app.get("/favicon.ico")
async def favicon():
    return Response(content="", media_type="image/x-icon", status_code=204)

@app.get("/")
async def root(accept: Optional[str] = Header(None)):
    unique_serial = generate_serial().upper()
    data = {"serial": unique_serial}
    if accept:
        if "text/plain" in accept:
            return PlainTextResponse(unique_serial)
        elif "application/xml" in accept or "text/xml" in accept or "application/xhtml+xml" in accept:
            xml_content = f'<root><serial>{unique_serial}</serial></root>'
            return XMLResponse(content=xml_content)
    # Default to JSON response
    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run("openfaas.wrapper:app", host="0.0.0.0", port=8000, reload=True)
