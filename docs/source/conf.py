
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
import namdtools

# Project information
project = 'namdtools'
copyright = '2020, Lockhart Lab'
author = 'C. Lockhart'

# The full version, including alpha/beta/rc tags
release = namdtools.__version__

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx.ext.viewcode',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# Autosummary parameters
autosummary_generate = True

# Intersphinx parameters
intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'python': ('https://docs.python.org/3', None),
    'scipy': ('http://docs.scipy.org/doc/scipy/reference', None),
    'sklearn': ('http://scikit-learn.org/stable', (None, './_intersphinx/sklearn-objects.inv'))
}

# Viewcode parameters
viewcode_follow_imported_members = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'nature'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
