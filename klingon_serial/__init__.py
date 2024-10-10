import logging

from .utils import validate_serial
from .generate import (
    generate_serial,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """Main function to run when the module is executed as a script."""
    serial = generate_serial()
    print(serial)
    logging.debug(f"Generated Serial: {serial}")
    logging.debug(f"Serial Valid: {validate_serial(serial)}")


if __name__ == "__main__":
    main()
