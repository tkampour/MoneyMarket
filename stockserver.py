import os.path
import sys
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import memcache
import torndb
import simplejson
import json
from tornado.options import define, options
from tornado.httpclient import HTTPRequest, HTTPError 
from elasticutils import get_es, S
import pycurl
from StringIO import StringIO
import re
from datetime import datetime

define("port", default=8888, help="App Server running on the given port", type=int)

symbols = {"AAAK.AT", "AAAP.AT","AEGEK.AT","AEGN.AT","AIOLC.AT","AKRIT.AT","ALAPIS.AT","ALCO.AT","ALKA.AT","ALMY.AT","ALPHA.AT","ALPHAR.AT","ALTEC.AT","ALTER.AT","ALTI.AT","ANEK.AT","ARBA.AT","ASCO.AT","ASTIR.AT","ATE.AT","ATEK.AT","ATHINA.AT","ATLA.AT","ATRUST.AT","ATTICA.AT","ATTIK.AT","AVE.AT","AVENIR.AT","BALK.AT","BELA.AT","BIOKA.AT","BIOSK.AT","BIOX.AT","BOC.AT","BOX.AT","BYTE.AT","CENTR.AT","CPBANK.AT","CPI.AT","CRETA.AT","CYCL.AT","DAIOS.AT","DIFF.AT","DION.AT","DOCHO.AT","DOL.AT","DOMIK.AT","DROME.AT","EDRA.AT","EDRIP.AT","EEE.AT","EEEK.AT","ELATH.AT","ELBA.AT","ELBE.AT","ELBI.AT","ELFIS.AT","ELGEK.AT","ELIN.AT","ELKA.AT","ELLAKTOR.AT","ELPE.AT","ELSTR.AT","ELTRK.AT","ELYF.AT","ENTER.AT","EPIL.AT","EPSIL.AT","ETE.AT","ETEM.AT","EUBRK.AT","EUPRO.AT","EUROB.AT","EUROM.AT","EUROS.AT","EVROF.AT","EXAE.AT","EX.AT","EYAPS.AT","EYDAP.AT","FFGRP.AT","FGE.AT","FIDO.AT","FLEXO.AT","FOODL.AT","FORTH.AT","GEBKA.AT","GEKTERNA.AT","GMF.AT","HATZK.AT","HKRAN.AT","HRAK.AT","HSI.AT","HTO.AT","HYGEIA.AT","IASO.AT","ILYDA.AT","INKAT.AT","INLOT.AT","INTEK.AT","INTET.AT","INTRK.AT","IOKA.AT","IPPOK.AT","KAMP.AT","KANAK.AT","KARE.AT","KARTZ.AT","KATHI.AT","KEKR.AT","KERAL.AT","KLEM.AT","KLONK.AT","KLONP.AT","KMOL.AT","KORDE.AT","KORRES.AT","KOUM.AT","KREKA.AT","KRI.AT","KTILA.AT","KYLO.AT","KYRI.AT","KYRM.AT","KYSA.AT","LAMDA.AT","LANAC.AT","LAVI.AT","LEBEK.AT","LEBEP.AT","LOGISMOS.AT","LYK.AT","MAIK.AT","MARAC.AT","MATHIO.AT","MEDIC.AT","MERKO.AT","METKK.AT","MEVA.AT","MHXAK.AT","MHXAP.AT","MIG.AT","MIN.AT","MINOA.AT","MLS.AT","MOCHL.AT","MODA.AT","MOTO.AT","MPITR.AT","MPK.AT","MPP.AT","MSHOP.AT","MYTIL.AT","NAFT.AT","NAKAS.AT","NAYP.AT","NEWS.AT","NIKAS.AT","NIR.AT","NUTRIART.AT","OLKAT.AT","OLTH.AT","OLYMP.AT","OPAP.AT","OPTRON.AT","ORAORA.AT","OTOEL.AT","PAIR.AT","PAP.AT","PARN.AT","PEGAS.AT","PERF.AT","PERS.AT","PETZK.AT","PLAIS.AT","PLAKR.AT","PLAT.AT","PPA.AT","PPAK.AT","PPC.AT","PRD.AT","PRESD.AT","PROF.AT","QUAL.AT","QUEST.AT","REVOIL.AT","RIDE.AT","RILK.AT","SAR.AT","SATOK.AT","SELMK.AT","SELO.AT","SFA.AT","SIDE.AT","SPACE.AT","SPID.AT","SPIR.AT","TATT.AT","TBANK.AT","TEGO.AT","TELET.AT","TELL.AT","TENERGY.AT","TEXT.AT","TGEN.AT","TITK.AT","TITP.AT","TPEIR.AT","TRASTOR.AT","TT.AT","VARDA.AT","VARG.AT","VARNH.AT","VIDAVO.AT","VIS.AT","VOSYS.AT","VOVOS.AT","XYLEP.AT","YALCO.AT"}

nsymbols = [{'value': 'MYTIL.AT', 'label':'Mytilineos'},{'value':'AEGEK.AT', 'label':'test2'},{'value':'ETE.AT', 'label':'Ethniki'},{'value':'NEWS.AT', 'label':'test4'},{'value':'MOTO.AT', 'label':'MOTODYNAMICS'}]

#get names of stocks with importio

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/search", SearchHandler),
            (r"/stock/(\w+.AT)", AjaxStock),
            (r"/stock/(.*)", AjaxStock),
            (r"/stock2/(.*)", Stock),
            (r"/about/?", AboutHandler),
            (r"/table", TableHandler),
            (r"/table2", TableHandler2),
            (r"/stockList", StockListHandler),
            (r"/arthro/(.*)", ArticleHandler),
            (".*", DefaultHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            debug=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):

    def return_json(self, data_dict):
        """
        acessory method to return json objects
        """
        self.set_header('Content-Type', 'application/json')
        json_ = tornado.escape.json_encode(data_dict)
        self.write(json_)
        self.finish()

    def write_error(self, status_code, **kwargs):
        self.write("Wow, that was unexpected! You caused a %d error." % status_code)

    def get_latest(self):
        lnews = memc.get('lnews')
        if not lnews:
            print "Error: Not Found in MemCache: latest news"
            es = get_es(urls='localhost:9200')
            basic_s = S()
            lnews = basic_s.order_by('-updated')[:10]
            memc.set('lnews',lnews)
        for result in lnews:
            print result.updated, ": ", result.title

class MainHandler(BaseHandler):
   def get(self):
        currencies = memc.get('currencies') # Refreshed every 2 hours
        com = memc.get('commodities') # Refreshed every 2 hours
        stocks = memc.get('stocks')
        self.get_latest()
        #print com
        #print currencies
        #print stocks
        if not currencies:
            print "Error: Not Found in MemCache: currencies"
        if not com:
            print "Error: Not Found in MemCache: commodities"
        self.render("index.html", curr=currencies, stocks=stocks, comm=com, symbol=None, news=None)

class ArticleHandler(BaseHandler):
    def get(self, article=5):
        try:
            print "Website: ",article
            self.render("article.html", article=article)
        except Exception, e:
            print "Unhandled Exception: ",e

class AjaxStock(BaseHandler):
    def handle_search(self, response):
        if response.error:
            print "Error", response.error
        else:
            body = json.loads(response.body)
            print body

    def get(self, symbol=5):
        try:
            print symbol
            if not symbol or symbol not in symbols:
                print "<--------Error: Stock not Found-------------->"

            else:
                print '<---------------Stock Found!!--------------------------->'
                db = torndb.Connection(
                    host="localhost", database="Stocker",
                    user="tkampour", password="github")
                rows = db.query("select * from StocksY where symbol = '"+symbol+"' order by date desc LIMIT 500")
                db.close()
                priceData =[]
                volumeData =[]
                summaryData =[]
                rows.reverse()
                rows2 = tornado.escape.json_encode(rows)
                
                for i in range(0,len(rows)):
                    priceData.append([i,rows[i].close])
                    volumeData.append([i,int(rows[i].volume)])
                    if (i % 14)==0:
                        summaryData.append([i,rows[i].close])

                self.render("index.html",curr=None, stocks=None, news=None,comm=None, symbol=symbol,jsonData=rows2, priceData=priceData, volumeData=volumeData, summaryData=summaryData)
        except Exception, e:
            print "Unhandled Exception: ",e

class Stock(BaseHandler):
    def get(self, symbol=5):
        try:
            print symbol
            if not symbol or symbol not in symbols:
                print "<--------Error: Stock not Found-------------->"

            else:
                print '<---------------Stock Found!!--------------------------->'
                db = torndb.Connection(
                    host="localhost", database="Stocker",
                    user="tkampour", password="github")
                rows = db.query("select * from StocksY where symbol = '"+symbol+"' order by date desc LIMIT 500")
                db.close()
                priceData =[]
                volumeData =[]
                summaryData =[]
                rows.reverse()
                rows2 = tornado.escape.json_encode(rows)
                
                for i in range(0,len(rows)):
                    priceData.append([i,rows[i].close])
                    volumeData.append([i,int(rows[i].volume)])
                    if (i % 14)==0:
                        summaryData.append([i,rows[i].close])

                self.render("stock.html",curr=None, stocks=None, news=None,comm=None, symbol=symbol,jsonData=rows2, priceData=priceData, volumeData=volumeData, summaryData=summaryData)
        except Exception, e:
            print "Unhandled Exception: ",e


class SearchHandler(BaseHandler):

    def searchel(self, query):
        es = get_es(urls='localhost:9200')
        # basic_s = S().indexes('bb141b308807935da14b57b7d531a36c32fddf77').doctypes('article').values_dict()
        basic_s = S()
        s = basic_s.query(summary__match=query)
        print basic_s.count(), s.count(), len(s)
        return s
        
    @tornado.web.asynchronous
    def get(self):
        self.render("search.html")

    @tornado.web.asynchronous
    def post(self):
        searchterm = self.get_argument("search")
        print "<-------------------------------Searched for:", searchterm
        if searchterm not in symbols:
            news = []
            news = self.searchel(searchterm)
            self.render("index.html",curr=None,stocks=None, comm=None, news=news, symbol=None)
        else:
            self.redirect("/stock/"+searchterm)

class StockListHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.return_json(nsymbols)

class AboutHandler(BaseHandler):
    @tornado.web.removeslash
    def get(self):
        self.render("about.html")

class TableHandler(BaseHandler):
    def get(self):
        self.render("table.html")

class TableHandler2(BaseHandler):
    def get(self):
        self.render("table.html.bak")
           
class DefaultHandler(BaseHandler):
    def get(self):
        self.render("50x.html")

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

def get_commodities():
    com = memc.get('commodities')
    if not com:
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
            c.setopt(c.HEADERFUNCTION, storage.write)
            c.perform()
            match = re.search(r'AUTH=[\w\d]*',storage.getvalue())
            if match:
                pass
            else:
                print "Did not get auth token!!"
            storage.close()
            c.close()

            storage = StringIO()
            c = pycurl.Curl()
            c.setopt(c.URL, url)
            c.setopt(pycurl.POST, 1)
            c.setopt(c.POSTFIELDS, data)
            c.setopt(pycurl.COOKIE, match.group())
            c.setopt(c.WRITEFUNCTION, storage.write)
            c.perform()
            c.close()
            com =  json.loads(storage.getvalue())
            print "Commodities Loaded from Webpage", com["results"]
            memc.set('commodities',com["results"])
            return com["results"]
        except Exception as e:
            print "Error:", e
    else:
        print "Commodities Loaded from MemCache"
        return com

if __name__ == "__main__":
    memc = memcache.Client(['127.0.0.1:11211'], debug=1);
    try:
#        get_commodities()
        main()
    except Exception, e:
        print "Unexpected Error", e
