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

# Following items are often useful when publishing
GITHUB_URL = u"http://github.com/mhubig/"
TWITTER_USERNAME = u"mhubig"
DISQUS_SITENAME = u"mhubig"
GOOGLE_ANALYTICS = u"UA-38038655-1"
