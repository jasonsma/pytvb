# -*- coding: utf-8 -*-

# Scrapy settings for pytvb project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'pytvb'

SPIDER_MODULES = ['pytvb.spiders']
NEWSPIDER_MODULE = 'pytvb.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pytvb (+http://www.yourdomain.com)'

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")
path = os.path.join(os.path.dirname(__file__), '../frontend')
sys.path.append(os.path.abspath(path))
from django.conf import settings

