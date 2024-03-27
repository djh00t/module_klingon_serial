from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r") as version_file:
    version = version_file.read().strip()

setup(
    name='klingon-serial',
    version=version,
    packages=find_packages(),
    author='David Hooton',
    author_email='klingon_serial+david@hooton.org',
    description='Get a globally unique serial',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/djh00t/module_klingon_serial',
    include_package_data=True,
    install_requires=[
        'psutil',
        'pytest>=6.0',  # Specify the minimum version required
        'str2bool',
    ],
    entry_points={
        'console_scripts': [
            'klingon_serial=klingon_serial:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',  # Add the license field
    python_requires='>=3.9',
)
