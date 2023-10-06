# Run tests
test:
	pytest tests/

# Package the project for pypi
package:
	python setup.py sdist bdist_wheel

# Upload to PyPI
upload:
	twine upload dist/*

# Clean up build files
clean:
	rm -rf build dist klingon_serial.egg-info .mypy_cache .pytest_cache klingon/__pycache__ tests/__pycache__

.PHONY: test package upload clean