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
master_doc = 'index'
nitpicky = True
version = VERSION

extensions = [
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinxcontrib.autodoc_pydantic']

html_theme = 'sphinx_rtd_theme'

always_document_param_types = True

intersphinx_mapping = {
    'encommon': ('https://encommon.readthedocs.io/en/stable', None),
    'pathlib': ('https://docs.python.org/3', None),
    'pytest': ('https://docs.pytest.org/latest', None),
    'python': ('https://docs.python.org/3', None)}

nitpick_ignore = [
    ('py:class', 'httpx.AsyncClient'),
    ('py:class', 'httpx.Client'),
    ('py:class', 'httpx.Response'),
    ('py:class', 'pydantic.main.BaseModel'),
    ('py:class', 'requests.models.Response'),
    ('py:class', 'requests.sessions.Session')]
