#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Markus Hubig'
AUTHOR_EMAIL = u'mhubig@gmail.com'
SITENAME = u'admin punk and python junk ...'
SITEURL = u'http://mhubig.fritz.box:8000'

TIMEZONE = u'Europe/Paris'
DEFAULT_LANG = u'en'
DEFAULT_PAGINATION = 10

THEME = u"/Users/markus/Development/pelican-octopress-theme"

# GITHUB_USER = u'mhubig'
# GITHUB_REPO_COUNT = 5
# GITHUB_SKIP_FORK = True
# GITHUB_SHOW_USER_LINK = False

FEED_ALL_ATOM = u'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = u'feeds/%s.atom.xml'

TYPOGRIFY = True
DELETE_OUTPUT_DIRECTORY = True
RELATIVE_URLS = False

# Blogroll
LINKS =  (('IMKO GmbH', 'http://imko.de'),
          ('Python', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/mhubig'),
          ('bitbucket', 'http://bitbucket.org/mhubig'),
          ('github', 'http://github.com/mhubig'),)

# global metadata to all the contents
DEFAULT_METADATA = (('administration', 'linux'),
                    ('python',          'punk'),)

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }

# static paths will be copied without parsing their contents
STATIC_PATHS = ['extra/robots.txt',]

# Following items are often useful when publishing
GITHUB_URL = u"http://github.com/mhubig/"
TWITTER_USERNAME = u"mhubig"
DISQUS_SITENAME = u"mhubig"
GOOGLE_ANALYTICS = u"UA-38038655-1"
