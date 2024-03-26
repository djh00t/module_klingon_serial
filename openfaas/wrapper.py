from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse, PlainTextResponse, XMLResponse
from typing import Optional
import uvicorn

app = FastAPI()

@app.get("/")
async def root(accept: Optional[str] = Header(None)):
    data = {"message": "Hello, World"}
    if accept:
        if "text/plain" in accept:
            return PlainTextResponse(str(data))
        elif "application/xml" in accept or "text/xml" in accept:
            xml_content = f'<root><message>{data["message"]}</message></root>'
            return XMLResponse(content=xml_content)
    # Default to JSON response
    return JSONResponse(content=data)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
