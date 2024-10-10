# Klingon Serial Python Module
[![klingon-serial unit tests](https://github.com/djh00t/module_klingon_serial/actions/workflows/klingon-serial-unit-tests.yaml/badge.svg)](https://github.com/djh00t/module_klingon_serial/actions/workflows/klingon-serial-unit-tests.yaml)
[![Pre-PR Merge CI](https://github.com/djh00t/module_klingon_serial/actions/workflows/pre-pr-merge.yaml/badge.svg)](https://github.com/djh00t/module_klingon_serial/actions/workflows/pre-pr-merge.yaml) [![.github/workflows/post-pr-merge.yaml](https://github.com/djh00t/module_klingon_serial/actions/workflows/post-pr-merge.yaml/badge.svg)](https://github.com/djh00t/module_klingon_serial/actions/workflows/post-pr-merge.yaml)

## Overview

The `klingon_serial` Python module is designed to generate a unique hexadecimal
serial number, avoiding serial conflicts in a distributed environment. The
serial number is a concatenation of the machine's MAC address, the process ID
(PID), and the current time in epoch format with millisecond precision. The
module aims to offer a robust method for generating serials that are virtually collision-free.

## Installation

To install the module, you can use `poetry`:

```bash
poetry add klingon-serial
```

## Serial Components

1. **MAC Address**: A unique identifier assigned to network interfaces for communications. 12 characters in hexadecimal.
2. **Process ID (PID)**: Unique ID for each running process. 5 characters in hexadecimal.
3. **Timestamp**: Millisecond-precision epoch time. 11 characters in hexadecimal.

These components are concatenated to form a unique serial number.

## Usage

Here is how you can use the `klingon_serial` module:

```python
from klingon_serial import generate_serial

# Generate a unique serial number
unique_serial = generate_serial()
print(f"Generated Serial: {unique_serial}")
```

## Serial Number Structure

The generated serial number has the following structure:

```
[ 12 characters MAC ][ 5 characters PID ][ 11 characters Timestamp ]
```

### Example

An example serial number might look like this:

```
02C3F642A1EC3A4B9B0985F53E
```

## Additional Features

- **Debug Mode**: Set the `DEBUG` environment variable to enable debug output.
- **Serial Validation**: Use `validate_serial()` function to check if a serial number is valid.
- **MAC Address Retrieval**: The module can retrieve the MAC address and network interface of the local machine.

## Testing

To run the test suite, you can use:

```bash
pytest -v tests
```

## Contributing

Feel free to fork this repository and submit pull requests for improvements or additional features.

## Development

For development, you can use Poetry:

- `poetry install`: Install dependencies
- `poetry run pytest`: Run tests
- `poetry build`: Create a distribution package
- `poetry publish`: Upload the package to PyPI

Make sure to update the version in `pyproject.toml` before creating a new release.
