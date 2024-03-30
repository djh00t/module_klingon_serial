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
	# Ensure the container is removed even if it doesn't exist
	-docker container rm -f $(TEST_CONTAINER) 2> /dev/null
	# Fetch the latest version tag from Docker Hub using the official Docker Hub API
	LATEST_VERSION=$$(curl -s "https://hub.docker.com/v2/repositories/$(IMAGE_NAME)/tags/?page_size=100&page=1&ordering=last_updated" | jq -r '.results[] | select(.name | test("^[0-9]+\\.[0-9]+\\.[0-9]+$")) | .name' | head -n 1)
	LATEST_VERSION=$$(curl -s "https://hub.docker.com/v2/repositories/$(IMAGE_NAME)/tags/?page_size=100&page=1&ordering=last_updated" | jq -r '.results[] | select(.name | test("^[0-9]+\\.[0-9]+\\.[0-9]+$")) | .name' | head -n 1)
	# Increment the latest version by one
	NEW_VERSION=$$(echo $$LATEST_VERSION | awk -F. '{$$NF = $$NF + 1;} 1' | sed 's/ /./g')
	# Update the VERSION file with the new version
	echo $$NEW_VERSION > $(VERSION_FILE)
	# Check if NEW_VERSION is not empty, then proceed
	if [ -z "$$NEW_VERSION" ]; then \
		echo "Error: Unable to get the latest version tag from Docker Hub."; \
		exit 1; \
	fi
	# Run image for testing with platform specification
	if [ -n "$$NEW_VERSION" ]; then \
		docker run -d --name $(TEST_CONTAINER) --platform linux/amd64 -p 8080:8080 $(IMAGE_NAME):$$NEW_VERSION; \
	else \
		echo "Error: Unable to get the latest version tag from Docker Hub."; \
		exit 1; \
	fi
	sleep 5
	# Health check, test endpoints, validate serial
	@if docker ps | grep -q $(TEST_CONTAINER); then \
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
			docker push $(IMAGE_NAME):$(VERSION); \
			docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest; \
			docker push $(IMAGE_NAME):latest; \
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
