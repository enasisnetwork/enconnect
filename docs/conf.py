"""
Functions and routines associated with Enasis Network Remote Connect.

This file is part of Enasis Network software eco-system. Distribution
is permitted, for more information consult the project license file.
"""
# pylint: disable=import-error



from os import path as os_path
from sys import path as sys_path

sys_path.insert(0, os_path.abspath('../'))

from enconnect import VERSION  # noqa: E402



project = 'enconnect'
copyright = '2024, Enasis Network'
author = 'Enasis Network'
nitpicky = True
version = VERSION

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.autodoc_pydantic']

html_theme = 'sphinx_rtd_theme'

always_document_param_types = True

intersphinx_mapping = {
    'encommon': ('https://encommon.readthedocs.io/en/stable', None),
    'pydantic': ('https://docs.pydantic.dev/latest', None),
    'pytest': ('https://docs.pytest.org/latest', None),
    'python': ('https://docs.python.org/3', None)}

nitpick_ignore = [

    # Seems to be an issue using Pydantic
    ('py:class', 'Field'),
    ('py:class', 'FieldInfo'),
    ('py:class', 'Ge'),
    ('py:class', 'Le'),
    ('py:class', 'MinLen'),
    ('py:class', 'NoneType'),

    # Not sure what causes these warnings
    ('py:class', 'httpx.AsyncClient'),
    ('py:class', 'httpx.AsyncByteStream'),
    ('py:class', 'httpx.Client'),
    ('py:class', 'httpx.Response'),
    ('py:class', 'httpx.SyncByteStream'),
    ('py:class', 'pytest_mock.plugin.MockerFixture'),
    ('py:class', 'requests.models.Response'),
    ('py:class', 'requests.sessions.Session'),
    ('py:class', 'respx.router.MockRouter'),
    ('py:class', 'types.Annotated')]
