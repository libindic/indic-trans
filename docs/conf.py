# -*- coding: utf-8 -*-
#
# indic-trans documentation build configuration file, created by
# sphinx-quickstart on Thu Jul 14 18:45:00 2016.

import sys
import os

project = u'indic-trans'
copyright = u'2016, Irshad Ahmad Bhat (AGPLv3+ License)'
author = u'Irshad Ahmad Bhat'


# -- Configuration of documentation -------------------------------------------

sys.path.append(os.path.dirname(os.path.dirname(__file__)).encode('utf-8'))

import indictrans
version = indictrans.__version__
release = indictrans.__version__

extensions = ['sphinx.ext.autosummary',
              'sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'numpydoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

pygments_style = 'sphinx'
todo_include_todos = False


# -- Overrides for modules ----------------------------------------------------

from mock import Mock

MOCK_MODULES = ['numpy', 'scipy']

for mod_name in MOCK_MODULES:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = Mock()


# -- Options for HTML output --------------------------------------------------

html_theme = 'sphinx_rtd_theme'

html_title = 'indic-trans documentation'
# html_logo = 'img/logo.png'
# html_favicon = 'img/favicon.ico'

html_static_path = ['_static']
htmlhelp_basename = 'indictransdoc'
