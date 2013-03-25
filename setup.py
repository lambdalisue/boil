#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = "0.1.0"

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()
setup(
    name="boil",
    version=version,
    description = "Jinja2 compile tools for building static web site",
    long_description=read('README.md'),
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "Jinja2, static, web",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/boil",
    download_url = r"https://github.com/lambdalisue/boil/tarball/master",
    license = 'MIT',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    entry_points = {
        'console_scripts': [
            "boil = boil.main:main",
        ]
    },
    include_package_data = True,
    zip_safe = True,
    install_requires=[
        'setuptools',
        'jinja2',
        'watchdog'
        'PyYaml',
    ],
)
