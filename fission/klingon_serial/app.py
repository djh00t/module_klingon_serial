from klingon_serial import generate_serial

def main(context, event):
    # Generate a unique serial number
    unique_serial = generate_serial()
    print(unique_serial.upper())
    return {"status": 200, "message": "OK"}

if __name__ == "__main__":
    main(None, None)