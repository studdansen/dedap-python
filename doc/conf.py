'''
Configuration file for documentation of ``dedap``.
'''

from datetime import datetime
import os
from pathlib import Path
import sys

SRC_DPATH = Path(__file__).parent.parent / 'dedap'
sys.path.insert(0, str(SRC_DPATH.resolve()))

project = 'dedap'
copyright = f'{datetime.today().year}, Dan Lynn'
author = 'Dan Lynn'
release = '1.0'

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.graphviz',
	'sphinx.ext.todo',
	'sphinxcontrib.bibtex',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

todo_include_todos = True

bibtex_bibfiles = ['refs.bib']
