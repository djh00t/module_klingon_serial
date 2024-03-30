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
	@curl -s -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
	"https://registry.hub.docker.com/v2/repositories/$(IMAGE_NAME)/tags" | \
	jq -r '.results|.[]|.name' | \
	sort -V | \
	tail -n1 | \
	xargs -I {} echo "Highest version found: {}"



test:
	pytest -v

clean:
	docker system prune -af --volumes
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete

run:
	uvicorn openfaas.handler:app --host 0.0.0.0 --port 8000
