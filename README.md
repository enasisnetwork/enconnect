# Enasis Network Remote Connect

> :children_crossing: This project has not released its first major version.

Functions and classes for connecting to remote services and whatnot.

[![](https://img.shields.io/github/actions/workflow/status/enasisnetwork/enconnect/build.yml?style=flat-square&label=GitHub%20actions)](https://github.com/enasisnetwork/enconnect/actions)<br>
[![codecov](https://img.shields.io/codecov/c/github/enasisnetwork/enconnect?token=7PGOXKJU0E&style=flat-square&logoColor=FFFFFF&label=Coverage)](https://codecov.io/gh/enasisnetwork/enconnect)<br>
[![](https://img.shields.io/readthedocs/enconnect?style=flat-square&label=Read%20the%20Docs)](https://enconnect.readthedocs.io)<br>
[![](https://img.shields.io/pypi/v/enconnect.svg?style=flat-square&label=PyPi%20version)](https://pypi.org/project/enconnect)<br>
[![](https://img.shields.io/pypi/dm/enconnect?style=flat-square&label=PyPi%20downloads)](https://pypi.org/project/enconnect)

## Documentation
Documentation is on [Read the Docs](https://enconnect.readthedocs.io).
Should you venture into the sections below you will be able to use the
`sphinx` recipe to build documention in the `docs/html` directory.

## Useful and related links
- https://developers.facebook.com/docs/instagram-basic-display-api/reference/media

## Installing the package
Installing stable from the PyPi repository
```
pip install enconnect
```
Installing latest from GitHub repository
```
pip install git+https://github.com/enasisnetwork/enconnect
```

## Quick start for local development
Start by cloning the repository to your local machine.
```
git clone https://github.com/enasisnetwork/enconnect.git
```
Set up the Python virtual environments expected by the Makefile.
```
make -s venv-create
```

### Execute the linters and tests
The comprehensive approach is to use the `check` recipe. This will stop on
any failure that is encountered.
```
make -s check
```
However you can run the linters in a non-blocking mode.
```
make -s linters-pass
```
And finally run the various tests to validate the code and produce coverage
information found in the `htmlcov` folder in the root of the project.
```
make -s pytest
```

## Build and upload to PyPi
Build the package.
```
make -s pypackage
```
Upload to the test PyPi.
```
make -s pypi-upload-test
```
Upload to the prod PyPi.
```
make -s pypi-upload-prod
```
