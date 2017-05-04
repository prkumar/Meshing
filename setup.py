# Standard library imports.
import os
from setuptools import setup, find_packages

about = dict()
with open(os.path.join("meshing", "__about__.py")) as fp:
    exec(fp.read(), about)

METADATA = {
    "name": "meshing",
    "version": about["__version__"],
    "author": about["__author__"],
    "author_email": about["__author_email__"],
    "install_requires": [],
    "description":  "Python package for geometric modeling and mesh "
                    "simplification",
    "classifiers": [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ],
    "keywords": "modeling",
    "packages": find_packages(exclude=("tests",))
}

if __name__ == "__main__":
    setup(**METADATA)
