from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, MetaData, Index, BigInteger, Integer, String, ForeignKey, DateTime, Boolean, Text, Float, UniqueConstraint
from sqlalchemy.orm import backref, mapper, relation, sessionmaker

Base = declarative_base()

class Stocks(Base):
    __tablename__ = 'Stocks'

    symbol = Column(String(10), primary_key=True)
    date  = Column(String(12), primary_key=True)
    open  = Column(Float)
    close = Column(Float)
    high  = Column(Float)
    low   = Column(Float)
    volume = Column(Integer)
    volprice = Column(Float)

class StocksY(Base):
    __tablename__ = 'StocksY'

    symbol = Column(String(12), primary_key=True)
    date  = Column(String(12), primary_key=True)
    open  = Column(Float)
    close = Column(Float)
    high  = Column(Float)
    low   = Column(Float)
    volume = Column(Integer)




Index('mystock', Stocks.symbol)

# create a connection to a sqlite database
# turn echo on to see the auto-generated SQL
engine = create_engine('mysql://tkampour:github@localhost:3306/Stocker')
 
# create the table and tell it to create it in the 
# database engine that is passed
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
#Session.add(User(...))
#Session.add_all([User(..),User])
#Session.commit()
