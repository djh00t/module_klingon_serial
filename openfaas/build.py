import requests
import os
import argparse
import logging
import subprocess
import json
import time
import platform

def run_command(command, capture_output=True, text=True, check=True):
    try:
        result = subprocess.run(command, capture_output=capture_output, text=text, shell=True, check=check)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
        if e.stdout:
            logging.error(f"Command output: {e.stdout}")
        if e.stderr:
            logging.error(f"Command error output: {e.stderr}")
        raise
    return result

def fetch_latest_tag(image_name):
    logging.debug(f"Fetching the latest tag for image: {image_name}")
    response = requests.get(f"https://registry.hub.docker.com/v2/repositories/{image_name}/tags")
    json_response = response.json()
    if 'results' not in json_response:
        logging.error("Unable to fetch tags, 'results' key not found in the response.")
        exit(1)
    tags = json_response['results']
    latest_tag = max((tag['name'] for tag in tags if tag['name'] != 'latest'), default=None, key=lambda t: list(map(int, t.split('.'))))
    logging.info(f"Latest tag fetched: {latest_tag}")
    return latest_tag

def increment_version(latest_tag, version_type):
    major, minor, patch = (0, 0, 0) if latest_tag is None else map(int, latest_tag.split('.'))
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    else:  # patch is the default
        patch += 1
    return f"{major}.{minor}.{patch}"


def build_image_with_buildx(image_name, new_version):
    platforms = "linux/amd64,linux/arm64"
    logging.info(f"Building Docker image for platforms {platforms}")
    builder_name = "klingon-builder"
    existing_builders = run_command("docker buildx ls", capture_output=True, text=True).stdout
    if builder_name not in existing_builders:
        logging.info(f"Creating a new builder named {builder_name} that supports multi-platform builds")
        run_command(f"docker buildx create --name {builder_name} --use --driver docker-container --platform linux/amd64,linux/arm64", capture_output=True, text=True)
    else:
        logging.info(f"Using existing builder named {builder_name}")
        run_command(f"docker buildx use {builder_name}")

    # Check if Dockerfile exists in the current directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    dockerfile_path = os.path.join(script_dir, 'Dockerfile')
    if not os.path.isfile(dockerfile_path):
        logging.error("Dockerfile does not exist in the current directory.")
        exit(1)

    command = f"docker buildx build --platform {platforms} -t {image_name}:{new_version} --push --progress plain ."
    run_command(command)


def test_image(image_name, new_version):
    logging.info(f"Testing Docker image {image_name}:{new_version}")
    # Replace slashes in the image name with underscores for a valid container name
    valid_container_name = image_name.replace('/', '_')
    # Ensure any existing test container is removed
    run_command(f"docker rm -f {valid_container_name}-test", check=False)
    command = f"docker run --rm --name {valid_container_name}-test -d -p 8080:8080 {image_name}:{new_version}"
    run_command(command)
    time.sleep(5)  # Wait for the container to start
    try:
        response = run_command(f"curl -s -o /dev/null -w '%{{http_code}}' http://localhost:8080/health", check=False)
        if response.stdout.strip() == "200":
            logging.info("Health check passed.")
            return True
        else:
            logging.error(f"Health check failed with status code: {response.stdout.strip()}")
            return False
    finally:
        run_command(f"docker stop {valid_container_name}-test", check=False)
        run_command(f"docker rm -f {valid_container_name}-test", check=False)

def tag_and_push_image(image_name, new_version):
    logging.info(f"Tagging and pushing Docker image {image_name}:{new_version}")
    run_command(f"docker tag {image_name}:{new_version} {image_name}:latest")
    run_command(f"docker push {image_name}:latest")
    run_command(f"docker push {image_name}:{new_version}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    parser = argparse.ArgumentParser(description='Increment version number for a Docker image.')
    parser.add_argument('--image', required=True, help='Name of the Docker image to fetch tags for and increment version.')
    parser.add_argument('--quiet', action='store_true', help='Suppress INFO level logging.')
    parser.add_argument('--debug', action='store_true', help='Enable DEBUG level logging.')
    parser.add_argument('--major', action='store_true', help='Increment the major version number.')
    parser.add_argument('--minor', action='store_true', help='Increment the minor version number.')
    parser.add_argument('--patch', action='store_true', help='Increment the patch version number.')
    args = parser.parse_args()

    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    version_type = 'patch'
    if args.major:
        version_type = 'major'
    elif args.minor:
        version_type = 'minor'

    image_name = args.image
    version_file = 'VERSION'
    logging.debug(f"Image name: {image_name}")
    logging.debug(f"Version file: {version_file}")
    # Pre-testing cleanup: remove any existing containers that may interfere with the test
    valid_container_name = image_name.replace('/', '_')
    logging.info(f"Performing pre-testing cleanup for any existing containers named {valid_container_name}-test")
    run_command(f"docker rm -f {valid_container_name}-test", check=False)
    latest_tag = fetch_latest_tag(image_name)
    new_version = increment_version(latest_tag, version_type)
    logging.info(f"New version: {new_version}")
    with open(version_file, 'w') as f:
        f.write(new_version)
        logging.debug(f"Version {new_version} written to {version_file}")

    build_image_with_buildx(image_name, new_version)
    if test_image(image_name, new_version):
        tag_and_push_image(image_name, new_version)
    else:
        logging.error("Image failed the health check, not pushing to Docker Hub.")
        exit(1)

if __name__ == "__main__":
    main()
