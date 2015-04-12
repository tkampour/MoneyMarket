import json
from pprint import pprint
import urllib2
import linecache
import MySQLdb
import memcache
from time import gmtime, strftime
import sys
import csv
import torndb

symbols =["AAAK.AT", "AAAP.AT","AEGEK.AT","AEGN.AT","AIOLC.AT","AKRIT.AT","ALAPIS.AT","ALCO.AT","ALKA.AT","ALMY.AT","ALPHA.AT","ALPHAR.AT","ALTEC.AT","ALTER.AT","ALTI.AT","ANEK.AT","ARBA.AT","ASCO.AT","ASTIR.AT","ATE.AT","ATEK.AT","ATHINA.AT","ATLA.AT","ATRUST.AT","ATTICA.AT","ATTIK.AT","AVE.AT","AVENIR.AT","BALK.AT","BELA.AT","BIOKA.AT","BIOSK.AT","BIOX.AT","BOC.AT","BOX.AT","BYTE.AT","CENTR.AT","CPBANK.AT","CPI.AT","CRETA.AT","CYCL.AT","DAIOS.AT","DIFF.AT","DION.AT","DOCHO.AT","DOL.AT","DOMIK.AT","DROME.AT","EDRA.AT","EDRIP.AT","EEE.AT","EEEK.AT","ELATH.AT","ELBA.AT","ELBE.AT","ELBI.AT","ELFIS.AT","ELGEK.AT","ELIN.AT","ELKA.AT","ELLAKTOR.AT","ELPE.AT","ELSTR.AT","ELTRK.AT","ELYF.AT","ENTER.AT","EPIL.AT","EPSIL.AT","ETE.AT","ETEM.AT","EUBRK.AT","EUPRO.AT","EUROB.AT","EUROM.AT","EUROS.AT","EVROF.AT","EXAE.AT","EX.AT","EYAPS.AT","EYDAP.AT","FFGRP.AT","FGE.AT","FIDO.AT","FLEXO.AT","FOODL.AT","FORTH.AT","GEBKA.AT","GEKTERNA.AT","GMF.AT","HATZK.AT","HKRAN.AT","HRAK.AT","HSI.AT","HTO.AT","HYGEIA.AT","IASO.AT","ILYDA.AT","INKAT.AT","INLOT.AT","INTEK.AT","INTET.AT","INTRK.AT","IOKA.AT","IPPOK.AT","KAMP.AT","KANAK.AT","KARE.AT","KARTZ.AT","KATHI.AT","KEKR.AT","KERAL.AT","KLEM.AT","KLONK.AT","KLONP.AT","KMOL.AT","KORDE.AT","KORRES.AT","KOUM.AT","KREKA.AT","KRI.AT","KTILA.AT","KYLO.AT","KYRI.AT","KYRM.AT","KYSA.AT","LAMDA.AT","LANAC.AT","LAVI.AT","LEBEK.AT","LEBEP.AT","LOGISMOS.AT","LYK.AT","MAIK.AT","MARAC.AT","MATHIO.AT","MEDIC.AT","MERKO.AT","METKK.AT","MEVA.AT","MHXAK.AT","MHXAP.AT","MIG.AT","MIN.AT","MINOA.AT","MLS.AT","MOCHL.AT","MODA.AT","MOTO.AT","MPITR.AT","MPK.AT","MPP.AT","MSHOP.AT","MYTIL.AT","NAFT.AT","NAKAS.AT","NAYP.AT","NEWS.AT","NIKAS.AT","NIR.AT","NUTRIART.AT","OLKAT.AT","OLTH.AT","OLYMP.AT","OPAP.AT","OPTRON.AT","ORAORA.AT","OTOEL.AT","PAIR.AT","PAP.AT","PARN.AT","PEGAS.AT","PERF.AT","PERS.AT","PETZK.AT","PLAIS.AT","PLAKR.AT","PLAT.AT","PPA.AT","PPAK.AT","PPC.AT","PRD.AT","PRESD.AT","PROF.AT","QUAL.AT","QUEST.AT","REVOIL.AT","RIDE.AT","RILK.AT","SAR.AT","SATOK.AT","SELMK.AT","SELO.AT","SFA.AT","SIDE.AT","SPACE.AT","SPID.AT","SPIR.AT","TATT.AT","TBANK.AT","TEGO.AT","TELET.AT","TELL.AT","TENERGY.AT","TEXT.AT","TGEN.AT","TITK.AT","TITP.AT","TPEIR.AT","TRASTOR.AT","TT.AT","VARDA.AT","VARG.AT","VARNH.AT","VIDAVO.AT","VIS.AT","VOSYS.AT","VOVOS.AT","XYLEP.AT","YALCO.AT"]

def readmoney():
    cr = csv.reader(open("data/historical_values_MYTIL_10_05_11_to_10_05_13.csv","rb"))

    columns = "(symbol, date, open, close, high, low, volume, volprice)"
    count = 0
    symbol = "MYTIL"

    for row in cr:
        print row
        if count>3:
            if not row[0]:
                break;
            values = ["'"+symbol+"'", "'"+row[0]+"'", row[7], row[1], row[8], row[9], row[6], row[5]]
            valueList = "%s" % (", ".join(values))
            insertSTMT = """INSERT INTO %s %s VALUES (%s)""" % ("Stocks", columns, valueList)
            print count, insertSTMT
            db.execute(insertSTMT);
        count += 1

def readyahoo():
    for symbol in symbols:
        try:
            cr = csv.reader(open("data/yahoo/table.csv?s="+symbol+"&d=4&e=24&f=2013&g=d&a=0&b=3&c=2000&ignore=.csv","rb"))

        except Exception, e:
            print "File for Stock Symbol not found: "+symbol
            continue

        columns = "(symbol, date, open, close, high, low, volume)"
        count = 0
        lastrow = 0

        lines = []
        for row in cr:
            lines.append(row)
            if not row[0]:
                break;
            else:
                lastrow +=1

        print "lastRow:", lastrow       
        for row in reversed(range(lastrow)):
            if row == 0 :
                break;
            line = lines[row]
            values = ["'"+symbol+"'", "'"+line[0]+"'", line[1], line[4], line[2], line[3], line[5]]
            valueList = "%s" % (", ".join(values))
            insertSTMT = """INSERT INTO %s %s VALUES (%s)""" % ("StocksY", columns, valueList)
#            print count, ":", insertSTMT
            db.execute(insertSTMT);
            count += 1

try:
    db = torndb.Connection(host= "localhost", database="Stocker",
                           user="tkampour", password="github")

#    readmoney()
    readyahoo()

except Exception , e:
    print "Unhandled Exception: " , e
    db.close()
    sys.exit()

memc = memcache.Client(['127.0.0.1:11211'])

db.close()
