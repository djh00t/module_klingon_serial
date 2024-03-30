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
	# Build and push multi-architecture images
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME):$(VERSION) --push .
	docker buildx build --platform linux/amd64,linux/arm64 -t $(IMAGE_NAME):latest --push .
	sleep 5
	# Health check, test endpoints, validate serial
	@if docker ps | grep -q klingon-serial-test; then \
		echo "Running Health Check"; \
		set -e; \
		HEALTH_CHECK=$$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health); \
		echo "Checking Serial Response"; \
		SERIAL_RESPONSE=$$(curl -s -H "Accept: application/json" http://localhost:8080/); \
		echo $$SERIAL_RESPONSE; \
		SERIAL=$$(echo $$SERIAL_RESPONSE | jq -r '.serial'); \
		echo "Validating Serial"; \
		if [ "$$HEALTH_CHECK" -eq 200 ]; then \
			echo "Container started successfully, pushing to Docker Hub..."; \
			docker push djh00t/klingon-serial:$(VERSION); \
			docker tag djh00t/klingon-serial:$(VERSION) djh00t/klingon-serial:latest; \
			docker push djh00t/klingon-serial:latest; \
		fi; \
		docker container rm -f klingon-serial-test; \
	else \
		echo "Container did not start successfully"; \
		exit 1; \
	fi


test:
	pytest -v

clean:
	docker system prune -af --volumes
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete

run:
	uvicorn openfaas.handler:app --host 0.0.0.0 --port 8000
