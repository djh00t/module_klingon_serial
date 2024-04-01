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
	@echo "Delegating build versioning to build.py..."
	@make clean
	@python3 build.py --image djh00t/klingon-serial --patch

build-minor:
	@echo "Delegating build versioning to build.py..."
	@make clean
	@python3 build.py --image djh00t/klingon-serial --minor

build-major:
	@echo "Delegating build versioning to build.py..."
	@make clean
	@python3 build.py --image djh00t/klingon-serial --major

test:
	export PYTHONPATH=./:$PYTHONPATH
	pytest -v

install:
	pip install -r requirements.txt

clean:
	docker system prune -af --volumes
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	rm -rf .pytest_cache

run:
	uvicorn openfaas.handler:app --host 0.0.0.0 --port 8000
