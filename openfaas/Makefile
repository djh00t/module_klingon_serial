VERSION_FILE := VERSION
VERSION := $(shell cat $(VERSION_FILE))
IMAGE_NAME := djh00t/klingon-serial

build:
	@echo "Building Docker image with version $(VERSION)"
	# Build multi-platform images faster with Docker Build Cloud: https://docs.docker.com/go/docker-build-cloud
	docker buildx build --platform linux/amd64,linux/arm64 --builder default -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest --push .
	@echo $$(echo $(VERSION) | awk -F. '{ printf "%d.%d.%d", $$1, $$2, $$3+1 }') > $(VERSION_FILE)

test:
	pytest -v

clean:
	docker system prune -f
	docker image prune -af
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: build test clean
