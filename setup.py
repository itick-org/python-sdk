from setuptools import setup, find_packages

setup(
    name="itick-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "websocket-client"
    ],
    description="iTick SDK for forex, stock, and crypto APIs",
    long_description=open("README.md").read() if open("README.md").readable() else "",
    long_description_content_type="text/markdown",
    author="iTick",
    author_email="support@itick.org",
    url="https://github.com/itick-org/python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
