import requests
import os
import argparse

def fetch_latest_tag(image_name):
    response = requests.get(f"https://registry.hub.docker.com/v2/repositories/{image_name}/tags")
    tags = response.json()['results']
    latest_tag = max((tag['name'] for tag in tags if tag['name'] != 'latest'), default=None, key=lambda t: list(map(int, t.split('.'))))
    return latest_tag

def increment_version(latest_tag):
    if latest_tag is None:
        return "0.0.1"
    major, minor, patch = map(int, latest_tag.split('.'))
    new_version = f"{major}.{minor}.{patch + 1}"
    return new_version

def main():
    image_name = os.getenv('IMAGE_NAME')
    version_file = os.getenv('VERSION_FILE')
    latest_tag = fetch_latest_tag(image_name)
    new_version = increment_version(latest_tag)
    print(f"New version: {new_version}")
    with open(version_file, 'w') as f:
        f.write(new_version)

if __name__ == "__main__":
    main()
import requests
import os
import argparse
import logging

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
    latest_tag = fetch_latest_tag(image_name)
    new_version = increment_version(latest_tag, version_type)
    logging.info(f"New version: {new_version}")
    with open(version_file, 'w') as f:
        f.write(new_version)
        logging.debug(f"Version {new_version} written to {version_file}")

if __name__ == "__main__":
    main()
