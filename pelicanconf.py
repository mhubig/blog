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
FILES_TO_COPY = (
        ('extra/CNAME', 'CNAME'),
        ('extra/.nojekyll', '.nojekyll'),
        ('extra/favicon.ico', 'favicon.ico'),
        ('extra/favicon.png', 'favicon.png'))

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

