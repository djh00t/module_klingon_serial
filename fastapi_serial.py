import os
import subprocess
import json
from fastapi import FastAPI
from klingon_serial.generate_serial import generate_serial

app = FastAPI()

@app.get("/")
def read_root():
    serial = generate_serial()
    return {"serial": serial.upper()}

@app.get("/test")
def run_tests():
    result = subprocess.run(["pytest","-v", "./tests/"], capture_output=True, text=True)
    return {"pytest_output": result.stdout}

if __name__ == "__main__":
    os.system("uvicorn fastapi_serial:app --reload")
