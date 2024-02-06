"""
Install script for crytic-exploit package
"""
from setuptools import setup, find_packages

setup(
    name="test_generator",
    description="A tool for automatically generating unit tests from Echidna and Medusa reproducers",
    url="https://github.com/crytic/test-generator",
    author="Trail of Bits",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    install_requires=[
        "colorama",
        "crytic_compile",
        "eth_utils",
        "slither_analyzer",
        "web3",
        "jinja2",
    ],
    entry_points={"console_scripts": ["test-generator = test_generator.main:main"]},
)
