from os import path
from codecs import open
from setuptools import setup, find_packages


NAME = 'photomatron'
VERSION = '0.0.143'
DESCRIPTION = 'Photobooth for Raspberry Pi 3'
AUTHOR = 'Frangitron'
AUTHOR_EMAIL = 'contact@frangitron.com'


_here = path.abspath(path.dirname(__file__))
_requirements_filepath = path.join(_here, 'requirements.txt')

if path.isfile(_requirements_filepath):
    with open(_requirements_filepath) as requirements_file:
        _requirements = requirements_file.readlines()
else:
    _requirements = list()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=find_packages(exclude=['tests']),
    install_requires=_requirements,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7"
    ],
    python_requires='>3.6, <3.8',
)
