# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from xrima.items import XrimaItem
import rawes
import hashlib
import json
import memcache
import string, sys

class XrimaPipeline(object):
	# put all words in lowercase
    words_to_filter = ['politics', 'religion']
    es = rawes.Elastic('http://localhost:9200/')
    memc = memcache.Client(['127.0.0.1:11211'], debug=1);

    def process_item(self, item, spider):
        if spider.name == "pinakas":
            self.memc.set('stocks', item)
            print "Pipeline: ",item
        else:
            print spider
            try:
        		self.index_event(spider.start_urls[0], item)
            except Exception as e:
        		raise DropItem("Exception",e)

    def index_event(self, feed_link, item):
        sha1_hash = hashlib.sha1()
        sha1_hash.update(feed_link.encode('utf-8'))
        feed_id = sha1_hash.hexdigest()

        """ Pass the event to ElasticSearch for indexing """
        id = hashlib.md5(item['link'].encode('utf-8')).hexdigest()
        body = json.dumps({'titlegr': item['title'], 'titlegl': self.el2gr(item['title']), 'updated': item['date'], 'summary': item['desc'], 'link': item['link'], 'img': item['image']})
        self.es.put(feed_id+'/article/'+id, data=body)

    def el2gr(self, line):
        poolGR =  u"αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩςάέήίϊΐόύϋΰώΆΈΉΊΪΌΎΫΏ "
        poolGL  =  "abgdezh8iklmn3oprstufx4wABGDEZH8IKLMN3OPRSTYFX4WsaehiiiouuuwAEHIIOYYW-"
        pool = dict(zip(poolGR, poolGL))# -*- coding: utf-8 -*-
        #try:
            #print "UTF:",line
            #line = line.decode("utf-8")
        #except UnicodeDecodeError:
            #print "ISO:",line
            #line = line.decode("iso8859-7")

        output_line = []
        for character in line:
            if pool.has_key(character):
                output_line.append(pool[character])
            else:
                output_line.append(character)
        return("".join(output_line))


