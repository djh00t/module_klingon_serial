VERSION_FILE := VERSION
VERSION := $(shell cat $(VERSION_FILE))
IMAGE_NAME := djh00t/klingon-serial

build:
	@echo "Building Docker image with version $(VERSION)"
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest --push .
	@echo $$(($(VERSION)+0.0.1)) > $(VERSION_FILE)

test:
	pytest -v

clean:
	docker system prune -f
	docker image prune -af

.PHONY: build test clean
