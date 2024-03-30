VERSION_FILE := VERSION
VERSION := $(shell cat $(VERSION_FILE))
IMAGE_NAME := djh00t/klingon-serial
TEST_CONTAINER := klingon-serial-test
DOCKER_BUILDX_BUILDER := multi-arch-builder

.PHONY: build test clean run check-buildx

# Check for buildx and create if not exists
check-buildx:
	@if ! docker buildx inspect $(DOCKER_BUILDX_BUILDER) > /dev/null 2>&1; then \
		docker buildx create --name $(DOCKER_BUILDX_BUILDER) --use; \
	fi

build:
	@echo "Fetching all tags for $(IMAGE_NAME)..."
	@LATEST_TAG=$$(curl -s "https://registry.hub.docker.com/v2/repositories/$(IMAGE_NAME)/tags" | jq -r '.results|.[]?.name' | grep -v latest | sort -V | tail -1); \
	if [ -z "$$LATEST_TAG" ]; then \
		echo "No tags found for $(IMAGE_NAME)"; \
	else \
		echo "Latest tag found: $$LATEST_TAG"; \
	fi
	# Version numbering is MAJOR.MINOR.PATCH. This script should increment the
	# PATCH number by 1 and tag the image with the new version number. If PATCH is 9,
	# it should roll over to 10 and so on.
	@echo "Calculating new version number..."
	@MAJOR=$$(echo $$LATEST_TAG | cut -d. -f1); \
	MINOR=$$(echo $$LATEST_TAG | cut -d. -f2); \
	PATCH=$$(echo $$LATEST_TAG | cut -d. -f3); \
	NEW_PATCH=$$((PATCH+1)); \
	NEW_VERSION=$$MAJOR.$$MINOR.$$NEW_PATCH; \
	echo "New version: $$NEW_VERSION"; \
	echo $$NEW_VERSION > $(VERSION_FILE)



test:
	pytest -v

clean:
	docker system prune -af --volumes
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete

run:
	uvicorn openfaas.handler:app --host 0.0.0.0 --port 8000
