from klingon_serial.generate_serial import generate_serial

def main(context=None, event=None):
    # Generate a unique serial number
    unique_serial = generate_serial()
    return {"status": 200, "message": "OK", "serial": unique_serial.upper()}

if __name__ == "__main__":
    main(None, None)
