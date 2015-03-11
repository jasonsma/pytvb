# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector

from pytvb.items import Scrapy81Item, ScrapyThreadItem
from tvb.models import Forum81Item
import django
from django.forms.models import model_to_dict

import re

URL_BASE = 'http://www.tvboxnow.com/'

class LoginSpider(BaseSpider):
    name = 'tvboxnow'
    allowed_domains = ['tvboxnow.com']
    start_urls = ['http://www.tvboxnow.com/logging.php?action=login']

    def parse(self, response):
        django.setup()
        return FormRequest.from_response(response,
                formdata={'username': 'tvbgetter', 'password': 'abc123'},
                callback=self.after_login)

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        self.log("Successful login. Time to crawl.")

        # continue scraping with authenticated session...
        return Request('http://www.tvboxnow.com/forum-8-1.html', callback=self.parse81)

    def parse81(self, response):
        open('forum-8-1', 'wb').write(response.body)

        entries = response.xpath("//table[@class='datatable']/tbody[@id]/tr")
        threads = []
        for entry in entries:
            item = Forum81Item()
            title_row = entry.xpath("th[@class='subject hot']/span[@id]/a/text()").extract()
            author = entry.xpath("td[@class='author']/cite/a/text()").extract()
            date = entry.xpath("td[@class='author']/em/text()").extract()
            link = entry.xpath("th[@class='subject hot']/span[@id]/a/@href").extract()
            if title_row and author and date:
                title_row[0].encode('utf-8')
               
                (item.title,\
                 item.first_episode,\
                 item.last_episode) = self.extract_title_row(title_row[0])
                item.datePosted = date[0]
                item.url = link[0]
                item.author = author[0]
                if item.title and item.author == 'whyhung':
                    try:
                        f81i = Forum81Item.objects.get(title=item.title,
                                                       author=item.author,
                                                       datePosted=item.datePosted)
                        Forum81Item.objects.filter(
                                title=item.title,
                                author=item.author,
                                datePosted=item.datePosted).update(
                                                    last_episode=item.last_episode)
                        print "Updated %s to episode %d" %\
                            (item.title.encode('utf-8'), item.last_episode)
                    except Forum81Item.DoesNotExist:
                        item.save()
                        print "New item"
                        print item
                    #threads.append(Request(url = URL_BASE + link[0],
                    #                   callback = self.parseThreads))

        return None

    def extract_title_row(self, row):
        """
            Return: title, first_episode, last_episode
        """
        # match:
        # [更新第2集] (高清翡翠台) 《倩女喜相逢》- 第1~2集 [HDTV-DIVX+HDTV-RMVB480P+HDTV-RMVB720P][粵語中字]
        whyhung1 = re.compile(r'\[更新第(\d+)集.*?\]\s*\(.+?\)\s*《(.+?)》\s*-\s*第(\d+)~(\d+)集')

        # [更新第30集(完)] (TVB) 大太監 第1~31集(完) [TV-RMVB+AVI+HDTV-RMVB720P][粵語中字]
        # [更新第30+31集(完)] (TVB) 大太監 第1~31集(完) [TV-RMVB+AVI+HDTV-RMVB720P][粵語中字]
        # group(2) would be None for the first case
        whyhung2 = re.compile(r'\[更新第(\d+)\+?(\d+)?集.*?\]\s*\(.+?\)\s*(.+?)\s+第(\d+)~(\d+)集')

        # [更新Ch41(完)] (煲劇2台)《宮鎖連城》 Ch01~44(完) [2015-02-02][TV-RMVB][粵語配音中字][720x408]
        # [更新Ch41~44(完)] (煲劇2台)《宮鎖連城》 Ch01~44(完) [2015-02-02][TV-RMVB][粵語配音中字][720x408]
        # [更新Ch700] (高清翡翠台) 愛．回家 Ch600~700 [高清->RMVB 版本][粵語中字][720x408]
        whyhung3 = re.compile(r'\[更新Ch(\d+)~?(\d+)?.*?\]\s*\(.+?\)\s*(?:《)?(.+?)(?:》)?\s*Ch(\d+)~(\d+)')

        # [更新Ch02](TVB) 倩女喜相逢 [Ch01 - Ch02] [TV-RMVB][粵語中字]
        jacky1 = re.compile(r'\[更新Ch(\d+)~?(\d+)?.*?\]\s*\(.+?\)\s*(?:《)?(.+?)(?:》)?\s*\[?Ch(\d+)\s*-\s*Ch(\d+)')

        row = row.encode('utf8')
        m = whyhung1.search(row)
        if m and 'ATV' not in row:
            title = m.group(2).decode('utf-8')
            first_episode = int(m.group(3))
            last_episode = int(m.group(4))
            return title, first_episode, last_episode

        m = whyhung2.search(row)
        if m and 'ATV' not in row:
            title = m.group(3).decode('utf-8')
            first_episode = int(m.group(4))
            last_episode = int(m.group(5))
            return title, first_episode, last_episode

        m = whyhung3.search(row)
        if m and 'ATV' not in row:
            title = m.group(3).decode('utf-8')
            first_episode = int(m.group(4))
            last_episode = int(m.group(5))
            return title, first_episode, last_episode

        m = jacky1.search(row)
        if m:
            title = m.group(3).decode('utf-8')
            first_episode = int(m.group(4))
            last_episode = int(m.group(5))
            return title, first_episode, last_episode

        return None, None, None

    def parseThreads(self, response):
        open('forumthread', 'wb').write(response.body)
        print "parsing %s\n" % response.url
        import pdb
        pdb.set_trace()

        lines = response.body.split('\n')
        for line in lines:
            if re.search('\.torrent', line):
                m = re.search('a href=\"(.*?)\"', line)
                if m:
                    attach = m.group(1)
                    break


        for link in links:
            title = link.xpath('strong/text()').extract()
            href = link.xpath('@href').extract()
            if title and href:
                title[0].encode('utf-8')
                print title[0], href[0]
        return None
