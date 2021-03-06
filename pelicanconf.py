#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Markus Hubig'
AUTHOR_EMAIL = u'mhubig@gmail.com'
SITENAME = u'admin punk and python junk ...'
SITEURL = u'http://localhost:8000'

TIMEZONE = u'Europe/Paris'
DEFAULT_LANG = u'en'
DEFAULT_PAGINATION = 10
THEME = u"/Users/markus/Development/pelican-octopress-theme"

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'extra/CNAME',
    'extra/keybase.txt',
    'extra/.nojekyll',
    'extra/favicon.ico',
    'extra/favicon.png',
]

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/CNAME':       {'path': 'CNAME'},
    'extra/keybase.txt': {'path': 'keybase.txt'},
    'extra/.nojekyll':   {'path': '.nojekyll'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/favicon.png': {'path': 'favicon.png'},
    }

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TYPOGRIFY = True
DELETE_OUTPUT_DIRECTORY = True
RELATIVE_URLS = True

# Blogroll
LINKS =  (('IMKO GmbH', 'http://imko.de'),
          ('Python', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/mhubig'),
          ('bitbucket', 'http://bitbucket.org/mhubig'),
          ('github', 'http://github.com/mhubig'),)
