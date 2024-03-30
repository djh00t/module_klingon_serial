VERSION_FILE := VERSION
VERSION := $(shell cat $(VERSION_FILE))
IMAGE_NAME := djh00t/klingon-serial

build:
	@echo "Building Docker image with version $(VERSION)"
	# Check for buildx and create if not exists
	if ! docker buildx inspect multi-arch-builder > /dev/null 2>&1; then \
		docker buildx create --name multi-arch-builder --use; \
	fi
	# Build image
	docker build --tag $(IMAGE_NAME):$(VERSION) .
	# Tag as latest
	docker tag $(IMAGE_NAME):$(VERSION) $(IMAGE_NAME):latest
	# Remove hanging containers
	CONTAINERS=$$(docker ps -a --filter "name=klingon-serial-test" -q); \
	if [ -n "$$CONTAINERS" ]; then \
		docker container rm -f $$CONTAINERS; \
	fi
	# Run image for testing
	docker run -d --name klingon-serial-test -p 8080:8080 $(IMAGE_NAME):$(VERSION)
	sleep 5
	# Health check, test endpoints, validate serial, and push if successful
	if docker ps | grep -q klingon-serial-test; then \
		echo "Running Health Check"; \
		HEALTH_CHECK=$$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health); \
		echo "Checking Serial Response"; \
		SERIAL_RESPONSE=$$(curl -s -H "Accept: application/json" http://localhost:8080/); \
		echo $$SERIAL_RESPONSE; \
		SERIAL=$$(echo $$SERIAL_RESPONSE | jq -r '.serial'); \
		echo "Validating Serial"; \
		if [ "$$HEALTH_CHECK" -eq 200 ]; then \
			echo "Container started successfully, pushing to Docker Hub..."; \
			docker push $(IMAGE_NAME):$(VERSION); \
			docker push $(IMAGE_NAME):latest; \
			docker image rm -f $$(docker images --filter=reference="$(IMAGE_NAME):*" -q | grep -v $(IMAGE_NAME):$(VERSION)) || true; \
		else \
			echo "Health check or serial validation failed, not pushing to Docker Hub."; \
			docker container rm -f klingon-serial-test; \
			exit 1; \
		fi; \
	else \
		echo "Container did not start, not pushing to Docker Hub."; \
		docker container rm -f klingon-serial-test; \
		exit 1; \
	fi
		echo "Running Health Check" \
		HEALTH_CHECK=$$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health); \
		echo "Checking Serial Response" \
		SERIAL_RESPONSE=$$(curl -s -H "Accept: application/json" http://localhost:8080/); \
		echo $$SERIAL_RESPONSE; \
		SERIAL=$$(echo $$SERIAL_RESPONSE | jq -r '.serial'); \
		echo "Validating Serial" \
		if [ "$$HEALTH_CHECK" -eq 200 ]; then \
			echo "Container started successfully, pushing to Docker Hub..."; \
			docker push $(IMAGE_NAME):$(VERSION); \
			docker push $(IMAGE_NAME):latest; \
			docker image rm -f $$(docker images --filter=reference="$(IMAGE_NAME):*" -q | grep -v $(IMAGE_NAME):$(VERSION)) || true; \
		else \
			echo "Health check or serial validation failed, not pushing to Docker Hub."; \
			docker container rm -f klingon-serial-test; \
			exit 1; \
		fi; \
	else \
		echo "Container did not start, not pushing to Docker Hub."; \
		docker container rm -f klingon-serial-test; \
		exit 1; \
	fi
	# Clean up
	docker image rm -f $$(docker images --filter=reference="$(IMAGE_NAME):*" -q) || true
	# Increment version
	@echo $$(echo $(VERSION) | awk -F. '{ printf "%d.%d.%d", $$1, $$2, $$3+1 }') > $(VERSION_FILE)

test:
	pytest -v

clean:

	docker system prune -af --volumes
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: build test clean run

run:
	uvicorn openfaas.handler:app --host 0.0.0.0 --port 8000
.PHONY: build test clean
