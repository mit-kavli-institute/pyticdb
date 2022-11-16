#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = []

setup(
    author="William Fong",
    author_email="willfong@mit.edu",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="A python wrapper for the TESS Input Catalog.",
    entry_points={
        "console_scripts": [
            "pyticdb=pyticdb.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="pyticdb",
    name="pyticdb",
    packages=find_packages(include=["pyticdb", "pyticdb.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://tessgit.mit.edu/wcfong/pyticdb",
    version="0.1.1a0",
    zip_safe=False,
)
