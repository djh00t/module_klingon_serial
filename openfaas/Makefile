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
	@LATEST_TAG=$$(curl -s "https://registry.hub.docker.com/v2/repositories/$(IMAGE_NAME)/tags" | jq -r '.results|.[]?.name' | grep -v latest | head -1); \
	if [ -z "$$LATEST_TAG" ]; then \
		echo "No tags found for $(IMAGE_NAME)"; \
	else \
		echo "Latest tag found: $$LATEST_TAG"; \
	fi
	@echo "Incrementing version number by 0.0.1"
	@echo $$(echo $(VERSION) | awk -F. '{$$NF = $$NF + 1;} 1' | sed 's/ /./g') > $(VERSION_FILE)
	@echo "Building image $(IMAGE_NAME):$(VERSION)"


test:
	pytest -v

clean:
	docker system prune -af --volumes
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete

run:
	uvicorn openfaas.handler:app --host 0.0.0.0 --port 8000
