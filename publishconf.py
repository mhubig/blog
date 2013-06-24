#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://mhubig.de'


FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

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
DEFAULT_METADATA = ({'administration': 'linux'},
                    {'python':          'punk'},)

# path-specific metadata
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    }

# static paths will be copied without parsing their contents
STATIC_PATHS = [
    'extra/robots.txt',
    ]

# Following items are often useful when publishing
GITHUB_URL = "http://github.com/mhubig/"
DISQUS_SITENAME = "mhubig"
GOOGLE_ANALYTICS = "UA-38038655-1"
