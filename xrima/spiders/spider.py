from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.utils.python import unicode_to_str
from scrapy.item import Item
from scrapy.http import Request
import re
from xrima.items import XrimaItem, StockItem
import datetime, time
import json
import memcache
import urllib2
import sys

class Spider1(BaseSpider):
    name = "tkam"
    start_urls = [
        "http://www.naftemporiki.gr"
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@id="CPHome_divBasic"]/div[@class="Box"]/*[name()="h1" or name()="h2"]')
        for site in sites:
            title = site.select('a/text()').extract()[0]
            link = site.select('a/@href').extract()[0]
            desc = ""#site.select('p/text()').extract()[0]
            print site, "[",title, link, desc, "]"

class Spider2(BaseSpider):
    name = "deal"
    allowed_domains = ["dealnews.gr"]
    start_urls = [
        "http://www.dealnews.gr/oikonomia"
    ]

    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@id="itemListPrimary"]/div[contains(@class,"itemContainer")]')
        for site in sites:
            print site
            title = site.select('.//a/text()').extract()[0]
            link = site.select('.//a/@href').extract()[0]
            desc = site.select('.//div[@class="catItemIntroText"]/text()').extract()[0]
            print site, "[",title, link, desc, "]"

class Spider3(BaseSpider):
    name = "gmoney"
    allowed_domains = ["greekmoney.gr"]
    start_urls = [
        "http://www.greekmoney.gr/"
    ]


    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@id="rotating_headlines"]/div[@class="headline_article"]')
        for site in sites:
            print site
            image = site.select('.//div[@class="headline_image"]/a/img/@src').extract()[0]
            title = site.select('.//h6/a/text()').extract()[0]
            link = site.select('.//h6/a/@href').extract()[0]
            desc = site.select('.//div[@class="headline_body"]/text()').extract()[0]
            print site, "[",title, link, desc, "]"
        sites = hxs.select('//div[@id="vertical_container"]/div[@class="vertical_accordion_content"]')
        for site in sites:
            print site
            image = site.select('div[@class="vertical_accordion_content_holder"]/a/img/@src').extract()[0]
            title = ""#site.select('a/text()').extract()[0]
            link = site.select('div[@class="vertical_accordion_content_holder"]/a/@href').extract()[0]
            desc = site.select('div[@class="vertical_accordion_content_holder"]/text()').extract()[0]
            print site, "[",image, title, link, desc, "]"

class Spider4(BaseSpider):
    name = "euro2day"
    allowed_domains = ["euro2day.gr"]
    start_urls = [
        "http://www.euro2day.gr/"
    ]

    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        #sites = hxs.select('//div[@id="fp-b2"]/div[contains(@class,"holder")]/div[@class="col-l"]/div[contains(@class,"post-box-top")]')
        sites = hxs.select('//div[@id="fp-b2"]/div[contains(@class,"holder")]/div[@class="col-l"]')
        for site in sites:
            print site
            image = site.select('.//a/img/@src').extract()[0]
            try:
                title = site.select('.//h3/a/text()').extract()[0]
            except:
                try:
                    title = site.select('.//li/text()').extract()[0]
                except:
                    title = ""
            link = site.select('.//a/@href').extract()[0]
            try:
                desc = site.select('.//p/text()').extract()[0]
            except:
                desc = ""
            print site, "[",title, link, desc, "]"
        sites = hxs.select('//div[@id="fp-b2"]/div[contains(@class,"holder")]/div[contains(@class,"col-r")]')
        for site in sites:
            print site
            image = site.select('.//a/img/@src').extract()[0]
            title = site.select('.//h3/a/text()').extract()[0]
            link = site.select('.//a/@href').extract()[0]
            try:
                desc = site.select('.//p/text()').extract()[0]
            except:
                desc = ""
            print site, "[",title, link, desc, "]"


class Spider5(BaseSpider):
    name = "imerisia"
    allowed_domains = ["imerisia.gr"]
    start_urls = [
        "http://www.imerisia.gr/"
    ]

    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="content"]')
        for site in sites:
            print site
            image = site.select('.//div[@class="fsummary"]/a/img/@src').extract()[0]
            title = site.select('.//div[@class="fsummary"]/h3/a/text()').extract()[0]
            link = site.select('.//div[@class="fsummary"]/a/@href').extract()[0]
            try:
                desc = site.select('.//div[@class="fsummary"]/text()').extract()[0]
            except:
                desc = ""
            print site, "[",title, link, desc, "]"
        sites = hxs.select('//div[@class="restsummary"]')
        for site in sites:
            print site
            image = site.select('a/img/@src').extract()[0]
            title = site.select('h3/a/text()').extract()[0]
            link = site.select('a/@href').extract()[0]
            try:
                desc = site.select('text()').extract()[0]
            except:
                desc = ""
            print site, "[",title, link, desc, "]"

class Spider6(BaseSpider):
    name = "kerdos"
    allowed_domains = ["kerdos.gr"]
    start_urls = [
        "http://www.kerdos.gr/"
    ]

    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@id="games"]/a')
        for site in sites:
            print site
            image = site.select('img/@src').extract()[0]
            title = site.select('img/@title').extract()[0]
            link = site.select('@href').extract()[0]
            try:
                desc = site.select('span/text()').extract()[0]
            except:
                desc = ""
            print site, "[",title, link, desc, "]"

class Spider7(BaseSpider):
    name = "capital"
    allowed_domains = ["capital.gr"]
    start_urls = [
        "http://www.capital.gr/"
    ]

    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//td[@class="cdBCTCDivCellBlue"]/div[@id="divTabCtrl_1_2" or @id="divTabCtrl_1_3" or @id="divTabCtrl_1_4" or @id="divTabCtrl_1_6"]/ul/li')
        #
        for site in sites:
            #print site
            title = site.select('a/text()').extract()[0]
            link = site.select('a/@href').extract()[0]
            if link.startswith('/static'):
            	continue
            try:
                desc = site.select('a/text()').extract()[0]
            except:
                desc = ""
            print site, "[",title, link, desc, "]"

class Spider8(BaseSpider):
    name = "news"
    allowed_domains = ["news.gr"]
    start_urls = [
        "http://www.news.gr/oikonomia/9/news.html"
    ]

    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[contains(@class,"newsbox300") or contains(@class,"newsbox140")]')
        #
        for site in sites:
            image = site.select('.//a/img/@src').extract()[0]
            title = site.select('.//a/text()').extract()[0]
            link = site.select('.//a/@href').extract()[0]
            desc = ""#site.select('a/text()').extract()[0]
            print "[",image,title, link, desc, "]"

class Spider9(CrawlSpider):
    name = "kathimerini"
    allowed_domains = ["kathimerini.gr"]
    start_urls = [
        "http://www.kathimerini.gr/economy"
    ]
    rules = (Rule(SgmlLinkExtractor(allow=('w_articles', )), callback='parse_item'),)
    
    def parse_item(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//a/@href')
        regexp = re.compile(r'w_articles')
        for site in sites:
            link = site.extract()
            if regexp.search(str(link)) is not None:
		        item = XrimaItem()
		        item['title'] = hxs.select('//*[@class="articleTitlos"]/text()').extract()[0]
		        item['link'] = response.url
		        item['desc'] =  hxs.select('//td[contains(@class,"eelantext")][1]/text()[normalize-space()]').extract()[0]
		        item['date'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
		        try:
		            item['image'] = hxs.select('//td[contains(@class,"eelantext")][1]').select('.//img/@src').extract()[0]
		        except:
		            item['image'] = None
		        print item
		        print item['title'], "::", item['desc']
		        return item


class Spider10(BaseSpider):
    name = "kathtest"
    allowed_domains = ["kathimerini.gr"]
    start_urls = [
        "http://www.kathimerini.gr/4dcgi/_w_articles_kathremote_1_03/07/2013_507253"
    ]

    def parse(self, response):
        #print(response.body)
        hxs = HtmlXPathSelector(response)
        item = XrimaItem()
        item['title'] = hxs.select('//*[@class="articleTitlos"]/text()').extract()[0]
        item['link'] = response.url
        item['desc'] =  hxs.select('//td[contains(@class,"eelantext")][1]/text()[normalize-space()]').extract()[0]
        item['date'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        try:
            item['image'] = hxs.select('//td[contains(@class,"eelantext")][1]').select('.//img/@src').extract()[0]
        except:
            item['image'] = None
        print item['title'], "::", item['desc']
        return item

class Spider11(BaseSpider): 
    name = "pinakas"
    allowed_domains = ["naftemporiki.gr", "msn.com"]
    start_urls = [
        "http://www.naftemporiki.gr/finance/athexStream"
    ]

    stocks = []
    items = []  
    memc = memcache.Client(['127.0.0.1:11211'], debug=1);

    def parse(self, response):
    	#symbols = {"AAAK.ATH", "AAAP.ATH","AEGEK.ATH","AEGN.ATH","AIOLC.ATH","AKRIT.ATH","ALAPIS.ATH","ALCO.ATH","ALKA.ATH","ALMY.ATH","ALPHA.ATH","ALPHAR.ATH","ALTEC.ATH","ALTER.ATH","ALTI.ATH","ANEK.ATH","ARBA.ATH","ASCO.ATH","ASTIR.ATH","ATE.ATH","ATEK.ATH","ATHINA.ATH","ATLA.ATH","ATRUST.ATH","ATTICA.ATH","ATTIK.ATH","AVE.ATH","AVENIR.ATH","BALK.ATH","BELA.ATH","BIOKA.ATH","BIOSK.ATH","BIOX.ATH","BOC.ATH","BOX.ATH","BYTE.ATH","CENTR.ATH","CPBANK.ATH","CPI.ATH","CRETA.ATH","CYCL.ATH","DAIOS.ATH","DIFF.ATH","DION.ATH","DOCHO.ATH","DOL.ATH","DOMIK.ATH","DROME.ATH","EDRA.ATH","EDRIP.ATH","EEE.ATH","EEEK.ATH","ELATH.ATH","ELBA.ATH","ELBE.ATH","ELBI.ATH","ELFIS.ATH","ELGEK.ATH","ELIN.ATH","ELKA.ATH","ELLAKTOR.ATH","ELPE.ATH","ELSTR.ATH","ELTRK.ATH","ELYF.ATH","ENTER.ATH","EPIL.ATH","EPSIL.ATH","ETE.ATH","ETEM.ATH","EUBRK.ATH","EUPRO.ATH","EUROB.ATH","EUROM.ATH","EUROS.ATH","EVROF.ATH","EXAE.ATH","EX.ATH","EYAPS.ATH","EYDAP.ATH","FFGRP.ATH","FGE.ATH","FIDO.ATH","FLEXO.ATH","FOODL.ATH","FORTH.ATH","GEBKA.ATH","GEKTERNA.ATH","GMF.ATH","HATZK.ATH","HKRAN.ATH","HRAK.ATH","HSI.ATH","HTO.ATH","HYGEIA.ATH","IASO.ATH","ILYDA.ATH","INKAT.ATH","INLOT.ATH","INTEK.ATH","INTET.ATH","INTRK.ATH","IOKA.ATH","IPPOK.ATH","KAMP.ATH","KANAK.ATH","KARE.ATH","KARTZ.ATH","KATHI.ATH","KEKR.ATH","KERAL.ATH","KLEM.ATH","KLONK.ATH","KLONP.ATH","KMOL.ATH","KORDE.ATH","KORRES.ATH","KOUM.ATH","KREKA.ATH","KRI.ATH","KTILA.ATH","KYLO.ATH","KYRI.ATH","KYRM.ATH","KYSA.ATH","LAMDA.ATH","LANAC.ATH","LAVI.ATH","LEBEK.ATH","LEBEP.ATH","LOGISMOS.ATH","LYK.ATH","MAIK.ATH","MARAC.ATH","MATHIO.ATH","MEDIC.ATH","MERKO.ATH","METKK.ATH","MEVA.ATH","MHXAK.ATH","MHXAP.ATH","MIG.ATH","MIN.ATH","MINOA.ATH","MLS.ATH","MOCHL.ATH","MODA.ATH","MOTO.ATH","MPITR.ATH","MPK.ATH","MPP.ATH","MSHOP.ATH","MYTIL.ATH","NAFT.ATH","NAKAS.ATH","NAYP.ATH","NEWS.ATH","NIKAS.ATH","NIR.ATH","NUTRIART.ATH","OLKAT.ATH","OLTH.ATH","OLYMP.ATH","OPAP.ATH","OPTRON.ATH","ORAORA.ATH","OTOEL.ATH","PAIR.ATH","PAP.ATH","PARN.ATH","PEGAS.ATH","PERF.ATH","PERS.ATH","PETZK.ATH","PLAIS.ATH","PLAKR.ATH","PLAT.ATH","PPA.ATH","PPAK.ATH","PPC.ATH","PRD.ATH","PRESD.ATH","PROF.ATH","QUAL.ATH","QUEST.ATH","REVOIL.ATH","RIDE.ATH","RILK.ATH","SAR.ATH","SATOK.ATH","SELMK.ATH","SELO.ATH","SFA.ATH","SIDE.ATH","SPACE.ATH","SPID.ATH","SPIR.ATH","TATT.ATH","TBANK.ATH","TEGO.ATH","TELET.ATH","TELL.ATH","TENERGY.ATH","TEXT.ATH","TGEN.ATH","TITK.ATH","TITP.ATH","TPEIR.ATH","TRASTOR.ATH","TT.ATH","VARDA.ATH","VARG.ATH","VARNH.ATH","VIDAVO.ATH","VIS.ATH","VOSYS.ATH","VOVOS.ATH","XYLEP.ATH","YALCO.ATH"}
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//table[@class="dataBoard"][position()>4]').select('.//tr[contains(@class,"parentRow")]')
        url = "http://www.naftemporiki.gr/finance/UpdateStreamValues.ashx?market=ATH"
        #url2 = "http://capital.gr.msn.com/stockvalues/allstocks.txt"
        items = []
      	time.sleep(7)
        for site in sites:
        	dict = {}
        	symbolgr = site.select('.//a/text()').extract()[0]
        	name = site.select('.//a/@title').extract()[0] 
        	symbolen = site.select('.//a/@symbol').extract()[0]
        	#print symbolgr,":",name,":",symbolen
	        dict['symbolgr'] = symbolgr
	        dict['name'] = name    
	        dict['symbolen'] = symbolen
    		self.stocks.append(dict)

		headers = {
            'User-agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:20.0) Gecko/20100101 Firefox/20.0'
        }
        req = urllib2.Request(url=url, headers=headers)
        f = urllib2.urlopen(req)
        response = f.read()
        stocklist = self.parse2(response) 
        self.memc.set('stocks', stocklist)
#        print "<--------------------------------------------------------->"
#        print self.memc.get('stocks')

    def parse2(self, response):
    	print "PARSE 2 IS CALLED"
    	items = []
    	print response
    	for stock in str(response).split('|'):
    		item = {}
    		sarr = stock.split('~')   		
    		if (len(sarr)>3 and sarr[0] != "qSymbol"):
		    	# print "Parse2:", sarr[0], sarr[1], sarr[2] , sarr[3]
		    	if (sarr and sarr[0] != 'qSymbol' and self.searchlist(self.stocks, sarr[0])):
		    		item['ticker'] = self.searchlist(self.stocks, sarr[0])['symbolgr']
		    		item['name'] = self.searchlist(self.stocks, sarr[0])['name']
		    		item['value'] = sarr[1]
		    		item['change'] = sarr[2]
		    		item['volume'] = sarr[3]	
		    		items.append(item)
		    	else:
		    		print("<---Symbol not found: ",sarr[0],"--->")
		    		pass
	return items

    def searchlist(self, list, symbol):
    	for item in list:
    		if item['symbolen'] == symbol:
    			return item
    		else:
    			#print item['symbolen'], "!=", symbol
    			pass

    def parse3(self, response):
    	print("got in")
    	print(response.body)
    	for stock in json.loads(response.body):
   			print stock
   			print "Parse3:", stock["P"], stock["S"], stock["L"]



# class Spider12(CrawlSpider):
#     name = "1stock"
#     allowed_domains = ["capital.gr.msn.com"]
#     start_urls = [
#         "http://capital.gr.msn.com/stockInfo.aspx?s=%CE%95%CE%A5%CE%91%CE%A0%CE%A3"
#     ]
    
#     def parse(self, response):
#         #print(response.body)
#         hxs = HtmlXPathSelector(response)
#         print "TKAM: ", response.body
#         item = {}
#         item['price'] = hxs.select('//div[@class="valuesContainer"]/div[@class="valueBox"]/div[@class="value qlast"]/text()').extract()[0]
#         item['chang'] = hxs.select('//div[@class="valuesContainer"]/div[@class="valueBox"]/div[@class="value qchange"]/text()').extract()[0]
#         # item['date'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
#         # try:
#         #     item['image'] = hxs.select('//td[contains(@class,"eelantext")][1]').select('.//img/@src').extract()[0]
#         # except:
#         #     item['image'] = None
#         print item
#         print item['price'], "::", item['chang']
#         return item
