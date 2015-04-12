#! /usr/bin/env python
#-*- coding: utf-8 -*-

# pyAggr3g470r - A Web based news aggregator.
# Copyright (C) 2010-2013  Cédric Bonhomme - http://cedricbonhomme.org/
#
# For more information : http://bitbucket.org/cedricbonhomme/pyaggr3g470r/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 1.5 $"
__date__ = "$Date: 2010/09/02 $"
__revision__ = "$Date: 2013/04/02 $"
__copyright__ = "Copyright (c) Cedric Bonhomme"
__license__ = "GPLv3"

import hashlib, sys
import json
import threading
import feedparser
from bs4 import BeautifulSoup

from datetime import datetime
from dateutil import tz

from random import choice

import conf
import utils
import rawes
from elasticutils import get_es, S
from pyelasticsearch.exceptions import ElasticHttpNotFoundError
import memcache

list_of_threads = []
user_agents = [
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0'
]

class FeedGetter(object):
    """
    This class is in charge of retrieving feeds listed in ./var/feed.lst.
    This class uses feedparser module from Mark Pilgrim.
    For each feed a new thread is launched.
    """
    def __init__(self):
        """
        Initializes the database connection.
        """
        self.rawes = rawes.Elastic('http://localhost:9200/')
        self.memc = memcache.Client(['127.0.0.1:11211'], debug=1);
  
    def index_event(self, feed_id, e, description):
        es = get_es(urls='localhost:9200')
        
        id = hashlib.md5(e.link.encode('utf-8')).hexdigest()
        
        try:
            basic_s = S().indexes(feed_id).doctypes('article')
            s2 = basic_s.query(_id__match=id)
            if (s2.count() != 0):
                return
        except Exception:#ElasticHttpNotFoundError:
            pass


        """ Pass the event to ElasticSearch for indexing """
        #str(datetime(*e.published_parsed[:6]
        time = str(datetime(*e.published_parsed[:6], tzinfo=tz.gettz('Europe/Athens')))
        #print(time[:10]+'T'+time[12:], ": Indexing ", e.title)
        body = json.dumps({'title': e.title, 'updated': time[:10]+'T'+time[12:], 'summary': e.summary, 'link': e.link, 'type': 'feed'})
        try:
            self.rawes.put(feed_id+'/article/'+id, data=body)
        except Exception as E:
            print("Elastic Search Problem Needs to be addressed: ",E)
            sys.exit(0)
            

    def index_event2(self, feed_id, e, description):
        es = get_es(urls='localhost:9200')
        try:
            es.delete_index(str(feed_id))
        except ElasticHttpNotFoundError:
            pass
        """ Pass the event to ElasticSearch for indexing """
        id = hashlib.md5(e.link.encode('utf-8')).hexdigest()
        body = json.dumps({'title': e.title, 'updated': e.updated, 'summary': e.summary, 'link': e.link})
        try:
            #es.put_mapping(feed_id, 'article', {
            #    'id': {'type': 'integer'},
            #    'title': {'type': 'string'},
            #    'updated': {'type': 'string'},
            #    'summary': {'type': 'string'},
            #    'link': {'type': 'string'}
            #    })
            es.index(feed_id,'article', body, 1)
        except Exception as E:
            print("Elastic Search Problem Needs to be addressed: ",E)
            sys.exit(0)

    def retrieve_feed(self, feed_url=None, feed_original=None):
        """
        Parse the file 'feeds.lst' and launch a thread for each RSS feed.
        """
        if feed_url != None:
            self.process(feed_url, feed_original)
        else:
            with open(conf.FEED_LIST) as f:
                for a_feed in f:
                    # test if the URL is well formed
                    for url_regexp in utils.url_finders:
                        if url_regexp.match(a_feed) or True:
                            #the_good_url = url_regexp.match(a_feed).group(0).replace("\n", "")
                            the_good_url = a_feed
                            try:
                                # launch a new thread for the RSS feed
                                thread = threading.Thread(None, self.process, \
                                                    None, (the_good_url,))
                                thread.start()
                                list_of_threads.append(thread)
                            except:
                                pass
                            break
                        else: 
                            print ("Feed url not suitably formed: "+ a_feed)

            # wait for all threads are done
            for th in list_of_threads:
                th.join()
            es = get_es(urls='localhost:9200')
            basic_s = S()
            lnews = basic_s.order_by('-updated')[:10]
            self.memc.set('lnews',lnews)

    def process(self, the_good_url, feed_original=None):
        """Request the URL
        Executed in a thread.
        """
        #errors=utils.detect_url_errors([the_good_url]) 
        #if errors == []:
            # if ressource is available add the articles in the base.
        self.add_into_database(the_good_url, feed_original)
        #else:
        #    print("Url Errors detected: "+the_good_url)
        #    print(errors)

    def add_into_database(self, feed_link, feed_original=None):
        """
        Add the articles of the feed 'a_feed' in the SQLite base.
        """
        feedparser.USER_AGENT = choice(user_agents)
        a_feed = feedparser.parse(feed_link)
        if a_feed['entries'] == []:
            return
        try:
            feed_image = a_feed.feed.image.href
        except:
            feed_image = "/img/feed-icon-28x28.png"

        if feed_original != None:
            feed_link = feed_original

        sha1_hash = hashlib.sha1()
        sha1_hash.update(feed_link.encode('utf-8'))
        feed_id = sha1_hash.hexdigest()

        

        for article in a_feed['entries']:
            #print(article)
            description = ""
            article_title = ""
            try:
                # article content
                description = article.content[0].value
                print("+++++++++++++++++++++++++++++++")
                print(description)
            except AttributeError:
                try:
                    description = article.description
                except Exception:
                    description = ""
            try:
                description = BeautifulSoup(description, "html.parser").get_text()
                article_title = BeautifulSoup(article.title, "html.parser").decode()
            except Exception as E:
                print("Problem when sanitizing the content of the feed: " + feed_link)
                print(E)
                article_title = article.title

            try:
                post_date = datetime(*article.published_parsed[:6])
            except:
                post_date = datetime(*article.updated_parsed[:6])

            # print(article.updated)
            sha1_hash = hashlib.sha1()
            sha1_hash.update(article.link.encode('utf-8'))
            article_id = sha1_hash.hexdigest()
            self.index_event(feed_id, article, description) # put on elastic search


# import urllib.request
# def get_frontpage():
#     urls = ["http://www.naftemporiki.gr"]
#     for url in urls:
#         headers = {
#             'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0'
#             }
#         req = urllib.request.Request(url=url, headers=headers)
#         f = urllib.request.urlopen(req)
#         html = f.read()
#         soup = BeautifulSoup(html)

#         sha1_hash = hashlib.sha1()
#         sha1_hash.update(url.encode('utf-8'))
#         feed_id = sha1_hash.hexdigest()

#         print(soup.prettify())
#  #       self.index_event(feed_id, article, description) # put on elastic search


if __name__ == "__main__":
    feed_getter = FeedGetter()
    print(str(datetime.now()), " : ", "Running feedgetter")
    feed_getter.retrieve_feed()
    print(str(datetime.now()), " : ", "Ended feedgetter")
