#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Rob Osterburg"
SITENAME = "Data and Code"
SITEURL = ""

PATH = "content"
STATIC_PATHS = ["images"]

TIMEZONE = "America/Denver"

DEFAULT_LANG = "en"

MARKUP = "md"
PLUGIN_PATHS = ["../etc/pelican-plugins/"]
PLUGINS = ["i18n_subsites"]

# Theme
THEME = "../etc/pelican-themes/pelican-bootstrap3"
JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.i18n"]}
SHOW_ARTICLE_AUTHOR = True
BOOTSTRAP_THEME = "flatly"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Chris Albon - Data Science & Artificial Intelligence", "https://chrisalbon.com/"),
    ("Practical Business Python", "https://www.pbpython.com/"),
    ("Animated Math", "https://www.3blue1brown.com/"),
    ("Flowing Data", "https://flowingdata.com/"),
    ("Talk Python To Me", "https://talkpython.fm/"),
    ("Alberto Cairo", "http://albertocairo.com/"),
    ("Data PlayGround", "https://harangdev.github.io/"),
    ("Matthew Devaney's Blog", "https://matthewdevaney.com/"),
)

# Social widget
# SOCIAL = (("You can add links in your config file", "#"), ("Another social link", "#"))

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# measure traffic
GOOGLE_ANALYTICS = "UA-142581046-2"
