# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from tvb.models import Forum81Item, ThreadItem

class Scrapy81Item(DjangoItem):
    django_model = Forum81Item

class ScrapyThreadItem(DjangoItem):
    django_model = ThreadItem
