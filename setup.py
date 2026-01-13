#!/usr/bin/env python

import os
from setuptools import setup
from setuptools import find_packages
from pathlib import Path


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding="utf-8") as file:
        return file.read()


def version():
    """Get the local package version."""
    namespace = {}
    path = Path("taggit_ui", "__version__.py")
    exec(path.read_text(), namespace)
    return namespace["__version__"]


version = version()
if 'dev' in version:
    dev_status = 'Development Status :: 3 - Alpha'
elif 'beta' in version:
    dev_status = 'Development Status :: 4 - Beta'
else:
    dev_status = 'Development Status :: 5 - Production/Stable'


setup(
    name="django-admin-taggit-ui",
    version=version,
    description="Filter and action to work with tags in the django-admin-backend.",
    long_description=read("README.rst"),
    author="Thomas Leichtfuß",
    author_email="thomas.leichtfuss@posteo.de",
    license="BSD License",
    url="https://github.com/thomst/django-admin-taggit-ui",
    platforms=["OS Independent"],
    packages=find_packages(exclude=["tests"]),
    package_data={'taggit_ui': ['templates/admin/*']},
    include_package_data=True,
    install_requires=[
        "Django",
        "django-taggit",
        "djangorestframework",
        "django-taggit-api",
        "django-modeltree>=0.9",
    ],
    classifiers=[
        dev_status,
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Framework :: Django :: 6.0",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    zip_safe=True,
)
