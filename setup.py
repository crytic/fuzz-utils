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
    python_requires=">=3.10",
    install_requires=[
        "colorama>=0.4.0",
        "slither_analyzer>=0.10.0",
        "jinja2>=3.1.0",
    ],
    extras_require={
        "lint": [
            "black==22.3.0",
            "pylint==2.13.4",
        ],
        "test": [
            "pytest",
        ],
        "dev": [
            "slither-analyzer[lint,test]",
        ],
    },
    entry_points={"console_scripts": ["test-generator = test_generator.main:main"]},
)
