#!/usr/bin/env python

"""The setup script."""

import codecs
import pathlib

from setuptools import find_packages, setup


# See https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path):
    here = pathlib.Path(__file__).resolve().parent()
    with codecs.open(here / rel_path) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


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
    version=get_version("pyticdb/__init__.py"),
    zip_safe=False,
)
