# -*- coding: utf-8 -*-
from setuptools import setup
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


# read package description
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# read package requirements
with open(path.join(here, 'requirements.txt')) as f:
    package_requirements = f.read().splitlines()

# read tests requirements
with open(path.join(here, 'tests/requirements.txt')) as f:
    tests_requirements = f.read().splitlines()

setup(
    name='shield',
    version='0.1.0',
    description='Django application for authorizing access to files and links',
    long_description=long_description,
    url='http://github.com/sebastianlach/shield',
    author='Sebastian Łach',
    author_email='root@slach.eu',
    license='GNU',
    packages=['shield'],
    install_requires=package_requirements,
    test_suite='nose.collector',
    tests_require=tests_requirements,
    zip_safe=False,
    include_package_data=True,
)
