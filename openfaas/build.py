import requests
import os

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
    image_name = os.getenv('IMAGE_NAME', 'djh00t/klingon-serial')
    version_file = os.getenv('VERSION_FILE', 'VERSION')
    latest_tag = fetch_latest_tag(image_name)
    new_version = increment_version(latest_tag)
    print(f"New version: {new_version}")
    with open(version_file, 'w') as f:
        f.write(new_version)

if __name__ == "__main__":
    main()
