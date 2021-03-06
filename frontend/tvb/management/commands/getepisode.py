# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from tvb.models import Forum81Item

import requests
import re
from datetime import date

class Command(BaseCommand):
    args = '<thread> <episode>'
    help = 'Download an <episode> from the thread.'

    def handle(self, *args, **options):
        if len(args) != 2:
            self.stdout.write("Specify 2 arguments: <thread> <episode>")
            quit()

        thread = args[0]
        episode = int(args[1])

        originalUrl = 'http://www.tvboxnow.com/%s' % thread
        loginUrl = 'http://www.tvboxnow.com/logging.php?action=login&loginsubmit=yes'

        session = requests.Session()
        postdata = {'password':'abc123', 'username':'lordgul'}
        res = session.post(loginUrl, data=postdata, headers={'referer':originalUrl})
        res = session.get(originalUrl, headers={'referer':loginUrl})
        res.encoding = 'utf-8'
        #print >>open(newsThread+'.debug', 'w'), res.text.encode('utf-8')
        lines = res.text.encode('utf-8').split('\n')
        for line in lines:
            #if today in line:
            if re.search('%d\.torrent' % episode, line):
                if re.search('DIVX', line):
                    continue
                m = re.search('a href=\"(.*?)\"', line)
                if m:
                    attach = m.group(1)
                    break

    #attach = "attachment.php?aid=3044607&amp;k=7110c105d6f63d6fde2249ce295d0234&amp;t=1424300372&amp;fid=497&amp;sid=e986eAA1gE2VIt23Bf3grtN%2BzV1QW6PpNUT0AN9WWcgzXxk"

        res = session.get('http://www.tvboxnow.com/%s' % attach,
                      headers={'referer':originalUrl})
        res.encoding = 'utf-8'
        #print >>open('attach.debug', 'w'), res.text.encode('utf-8')
        lines = res.text.encode('utf-8').split('\n')
        for line in lines:
            if 'window.location.href' in line:
                m = re.search('window.location.href =\'(.*?)\'', line)
                if m:
                    attach2 = m.group(1)
                    break

    #attach2 = "attachment.php?aid=3044607&k=6d08894a1401dbcaed228810df69b923&t=1424300529&ck=75275fec&sid=eb69a4mAPMfsfN7MXQKrYCzaoNwJX4IE%2BiONdlm98dg3%2F%2BU"


        misc = res.url
        res = session.get('http://www.tvboxnow.com/%s' % attach2,
                            headers={'referer':misc}, stream=True)
        with open("%s-%d.torrent" % (thread, episode), "wb") as f:
           for chunk in res.iter_content():
             f.write(chunk)

