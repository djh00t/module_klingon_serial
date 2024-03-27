VERSION_FILE := VERSION
VERSION := $(shell cat $(VERSION_FILE))
IMAGE_NAME := djh00t/klingon-serial

build:
	@echo "Building Docker image with version $(VERSION)"
	# Build the Docker image locally first
	@if ! docker buildx inspect multi-arch-builder > /dev/null 2>&1; then \
		docker buildx create --name multi-arch-builder --use; \
	fi
	docker build --tag $(IMAGE_NAME):$(VERSION) .
	# Remove any hanging containers that might have been left from previous tests
	CONTAINERS=$$(docker ps -a --filter "name=klingon-serial-test" -q); \
	if [ -n "$$CONTAINERS" ]; then \
		docker container rm -f $$CONTAINERS; \
	fi
	# Run the Docker image to ensure it starts correctly
	docker run -d --name klingon-serial-test -p 8080:8080 $(IMAGE_NAME):$(VERSION)
	# Wait for a few seconds to give the container time to start
	sleep 5
	# Check if the container is running and the application responds
	if docker ps | grep -q klingon-serial-test; then \
		if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health | grep -q 200; then \
			echo "Container started successfully, pushing to Docker Hub..."; \
			docker push $(IMAGE_NAME):$(VERSION); \
			docker push $(IMAGE_NAME):latest; \
			# Remove any previous versions of the image
			docker image rm -f $$(docker images --filter=reference="$(IMAGE_NAME):*" -q | grep -v $(docker images --filter=reference="$(IMAGE_NAME):$(VERSION)" -q)) || true; \
			IMAGES=$$(docker images --filter=reference="$(IMAGE_NAME):*" -q | grep -v $(docker images --filter=reference="$(IMAGE_NAME):$(VERSION)" -q)); \
			if [ -n "$$IMAGES" ]; then \
				docker image rm -f $$IMAGES; \
			fi; \
		else \
			echo "Health check failed, not pushing to Docker Hub."; \
			exit 1; \
		fi; \
	else \
		echo "Container did not start, not pushing to Docker Hub."; \
		exit 1; \
	fi
	# Clean up the test container
	docker stop klingon-serial-test
	docker rm klingon-serial-test
	@echo $$(echo $(VERSION) | awk -F. '{ printf "%d.%d.%d", $$1, $$2, $$3+1 }') > $(VERSION_FILE)

test:
	pytest -v

clean:
	docker system prune -f
	docker image prune -af
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

.PHONY: build test clean run

run:
	uvicorn openfaas.handler:app --host 0.0.0.0 --port 8000
.PHONY: build test clean
