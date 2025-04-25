# Makefile for klingon_serial Python package

# Variables
TWINE_USERNAME ?= __token__
TEST_TWINE_PASSWORD ?= $(TEST_PYPI_USER_AGENT)
PYPI_TWINE_PASSWORD ?= $(PYPI_USER_AGENT)
RM = rm -f
PYTEST = poetry run pytest
TWINE = poetry publish
APP = klingon_serial

# Clean up build files
clean:
	$(RM) -r build dist *.egg-info .mypy_cache .pytest_cache __pycache__ */__pycache__ *.zip *.gz *.whl */*.zip */*.gz */*.whl

## install: Install the package locally
install:
	poetry install

# Pre-push cleanup target
push-prep:

	@echo "Running poetry lock......................................................... 🔒"
	@poetry lock
	@echo "Removing temporary files.................................................... 🧹"
	@find . -type f -name '*.pyc' -delete
	@echo "Removed temporary files..................................................... ✅"

## uninstall: Uninstall the local package
uninstall:
	poetry remove $(APP)

# Run tests
test:
	@echo "Running unit tests..."
	$(PYTEST) -v tests

## sdist: Create a source distribution package
sdist: clean
	poetry build -f sdist

## build: Create a distribution package
build: clean
	poetry build

## upload-test: Run tests, if they pass, upload the distribution package to TestPyPI
upload-test: test build
	echo "Uploading to TestPyPI..."
	$(TWINE) --repository testpypi

## upload: Run tests, if they pass, upload the distribution package to PyPI
upload: test build
	echo "Uploading to PyPI..."
	$(TWINE)

## update-version: Increment the patch version number in pyproject.toml
update-version:
	echo "Updating version number..."
	NEW_VERSION=$$(awk -F. '{print $$1"."$$2"."$$3+1}' VERSION); \
	echo $$NEW_VERSION > VERSION; \
	sed -i'' -e "s/version = \"[0-9]*\.[0-9]*\.[0-9]*\"/version = \"$$NEW_VERSION\"/g" pyproject.toml; \
	echo "New version number is $$NEW_VERSION"

.DEFAULT_GOAL := test
.PHONY: clean install uninstall test build upload-test upload update-version push-prep
