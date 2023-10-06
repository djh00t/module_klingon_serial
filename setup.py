from setuptools import setup, find_packages

setup(
    name='klingon-kafka',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'uuid',
        'datetime'
        'unittest2==1.1.0'
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        'console_scripts': [
            'klingon_serial=klingon_serial:main',
        ],
    },
)
