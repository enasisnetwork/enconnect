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
- [Instagram API](https://developers.facebook.com/docs/instagram-basic-display-api/reference/media)
- [YouTube API](https://developers.google.com/youtube/v3/docs)

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

## Version management
:warning: Ensure that no changes are pending.

1. Rebuild the environment.
   ```
   make -s check-revenv
   ```

1. Update the [version.txt](enconnect/version.txt) file.

1. Push to the `main` branch.

1. Create [repository](https://github.com/enasisnetwork/enconnect) release.

1. Build the Python package.<br>
   ```
   make -s pypackage
   ```

1. Upload Python package to PyPi test.
   ```
   make -s pypi-upload-test
   ```

1. Upload Python package to PyPi prod.
   ```
   make -s pypi-upload-prod
   ```

1. Update [Read the Docs](https://enconnect.readthedocs.io) documentation.
