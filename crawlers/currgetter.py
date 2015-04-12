import json
import feedparser
from datetime import datetime
from random import choice
from bs4 import BeautifulSoup

#import utils
import memcache
#import urllib.request
from StringIO import StringIO
import pycurl
import re

user_agents = [
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0'
]

class currGetter(object):
    def __init__(self):
        self.memc = memcache.Client(['127.0.0.1:11211'])

    def processcur(self, feed_link):
        feedparser.USER_AGENT = choice(user_agents)
        a_feed = feedparser.parse(feed_link)
        if a_feed['entries'] == []:
            return

        curr = {}
        for article in a_feed['entries']:
            
            try:
                post_date = datetime(*article.published_parsed[:6])
            except:
                post_date = datetime(*article.updated_parsed[:6])

            list = article.description.split(' ')
#            print(article.title_detail.value, " :: ",article.description,"::", post_date, "::",list[3])
            curr[article.title_detail.value] = list[3]
            self.memc.set("currencies",curr)
            #print(curr)

    def processcomm(self):
        url = 'query.import.io/store/connector/64ecbb87-dab9-4b78-a9be-7a12f274f436/_query'
        urll = 'https://api.import.io/auth/login?username=tkampour&password=github'
        data = '{"input": {"webpage/url":"http://money.cnn.com/data/commodities/"}}'
        datal = 'username=tkampour&password=github'
        try: 

            storage = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, urll)
            c.setopt(c.POSTFIELDS, datal)
            c.setopt(pycurl.POST, 1)
            #c.setopt(c.WRITEFUNCTION, storage.write)
            c.setopt(c.HEADERFUNCTION, storage.write)
            c.perform()
            match = re.search(r'AUTH=[\w\d]*',storage.getvalue())
            if match:
                pass
            else:
                print("Did not get auth token!!")
            storage.close() 
            c.close() # test if 

            storage = StringIO()
            c = pycurl.Curl() # test if
            c.setopt(c.URL, url)
            c.setopt(pycurl.POST, 1)

            c.setopt(c.POSTFIELDS, data)
            c.setopt(pycurl.COOKIE, match.group())
            c.setopt(c.WRITEFUNCTION, storage.write)

            c.perform()
            c.close()
            com =  json.loads(storage.getvalue())
            print
            print(str(datetime.now()), " : ", "Ended Currency and Commodity Getter")
            memc.set('commodities',com["results"])
            return com["results"]
        except Exception as e:  
            print("Error:", e)

    def processind(self, feed_link):
        headers = {
            'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0'
            }
        req = urllib.request.Request(url=feed_link, headers=headers)
        f = urllib.request.urlopen(req)
        print("--------------",)
        soup = BeautifulSoup(f.read(), "html.parser")
#        print(description.prettify())
        for tbody in soup.find_all("tr", "stripe"):
            print(tbody)

#        curr = {}
#
#            curr[article.title_detail.value] = list[3]
#            self.memc.set("currencies",curr)


if __name__ == "__main__":
    memc = memcache.Client(['127.0.0.1:11211'])
    # Point of entry in execution mode
    getter = currGetter()
    # Retrieve all feeds
    print(str(datetime.now()), " : ", "Running Currency and Commodity Getter")
    getter.processcur("http://themoneyconverter.com/rss-feed/EUR/rss.xml")
    getter.processcomm()
    
