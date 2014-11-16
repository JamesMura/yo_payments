
import sys
import os


cwd = os.getcwd()
project_root = os.path.dirname(cwd)

sys.path.insert(0, project_root)

import yo_payments


extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']

templates_path = ['_templates']

source_suffix = '.rst'


master_doc = 'index'

project = u'Yo Payments'
copyright = u'2013, James Muranga'

version = yo_payments.__version__
release = yo_payments.__version__


exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme = 'default'

html_static_path = ['_static']

htmlhelp_basename = 'yo_paymentsdoc'

latex_elements = {
}

latex_documents = [
    ('index', 'yo_payments.tex', u'Yo Payments Documentation',
     u'James Muranga', 'manual'),
]

man_pages = [
    ('index', 'yo_payments', u'Yo Payments Documentation',
     [u'James Muranga'], 1)
]


texinfo_documents = [
    ('index', 'yo_payments', u'Yo Payments Documentation',
     u'James Muranga', 'yo_payments', 'One line description of project.',
     'Miscellaneous'),
]
