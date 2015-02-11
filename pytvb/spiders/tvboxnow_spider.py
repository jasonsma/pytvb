# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector

from pytvb.items import Scrapy81Item, ScrapyThreadItem

import re

URL_BASE = 'http://www.tvboxnow.com/'

class LoginSpider(BaseSpider):
    name = 'tvboxnow'
    allowed_domains = ['tvboxnow.com']
    start_urls = ['http://www.tvboxnow.com/logging.php?action=login']

    def parse(self, response):
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
        #xpath_row = "//table[@class='datatable']/tbody[@id]/tr"
        #xpath_title = "//table[@class='datatable']/tbody[@id]/tr/th[@class='subject hot']/span[@id]/a/text()"
        #xpath_author ="//table[@class='datatable']/tbody[@id]/tr/td[@class='author']/cite/a/text()"
        #xpath_date = "//table[@class='datatable']/tbody[@id]/tr/td[@class='author']/em"

        entries = response.xpath("//table[@class='datatable']/tbody[@id]/tr")
        threads = []
        for entry in entries:
            title_row = entry.xpath("th[@class='subject hot']/span[@id]/a/text()").extract()
            author = entry.xpath("td[@class='author']/cite/a/text()").extract()
            date = entry.xpath("td[@class='author']/em/text()").extract()
            link = entry.xpath("th[@class='subject hot']/span[@id]/a/@href").extract()
            if title_row and author and date:
                title_row[0].encode('utf-8')
                #print title_row[0], author[0], date[0], link[0]
                print self.extract_title_row(title_row[0])
                threads.append(Request(url = URL_BASE + link[0], callback = self.parseThreads))

        return threads[0]

    def extract_title_row(self, row):
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
        if m:
            title = m.group(2)
            first_episode = int(m.group(3))
            last_episode = int(m.group(4))
            return title, first_episode, last_episode

        m = whyhung2.search(row)
        if m:
            title = m.group(3)
            first_episode = int(m.group(4))
            last_episode = int(m.group(5))
            return title, first_episode, last_episode

        m = whyhung3.search(row)
        if m:
            title = m.group(3)
            first_episode = int(m.group(4))
            last_episode = int(m.group(5))
            return title, first_episode, last_episode

        m = jacky1.search(row)
        if m:
            title = m.group(3)
            first_episode = int(m.group(4))
            last_episode = int(m.group(5))
            return title, first_episode, last_episode

    def parseThreads(self, response):
        open('forumthread', 'wb').write(response.body)
        links = response.xpath("//span[@id]/a")
        #print "parsing %s\n" % response.url
        for link in links:
            title = link.xpath('strong/text()').extract()
            href = link.xpath('@href').extract()
            if title and href:
                title[0].encode('utf-8')
                #print title[0], href[0]
        return None
