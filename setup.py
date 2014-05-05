#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='djangorest-alchemy',
    version='0.1.0',
    description='Django REST Framework and SQLAlchemy integration',
    long_description=readme + '\n\n' + history,
    author='Ashish Gore',
    author_email='ashish.gore@dealertrack.com',
    url='https://github.com/iagore/djangorest-alchemy',
    packages=[
        'djangorest-alchemy',
    ],
    package_dir={'djangorest-alchemy':
                 'djangorest-alchemy'},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='djangorest-alchemy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)