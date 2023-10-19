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
    lines = result.stdout.split('\n')
    test_results = {}
    for line in lines:
        if "PASSED" in line or "FAILED" in line:
            test_name, test_result = line.split("::")[-1].split()[0:2]
            test_results[test_name] = test_result
    return test_results

if __name__ == "__main__":
    os.system("uvicorn fastapi_serial:app --reload")
