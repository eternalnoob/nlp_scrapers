import os
from sqlalchemy import create_engine
import microdata
import urllib
from lxml import html
import itertools
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, JSON, Text, DECIMAL, Integer
from sqlalchemy.orm import sessionmaker
from decimal import Decimal

engine = create_engine(os.environ.get('ALEXA_DATABASE_URL'))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw = Column(JSON)
    name = Column(Text)
    description = Column(Text)
    brand = Column(Text)
    price = Column(DECIMAL)
    avgrating = Column(DECIMAL)
    model = Column(Integer)
    rating_count = Column(Integer)
    good_rating = Column(Text)
    bad_rating = Column(Text)

    def __init__(self, item):
        self.raw = item.json()
        self.description = item.description
        self.name = item.name
        self.model = int(item.productID)
        self.price = Decimal(item.offers.price) if item.offers.price else Decimal(0)
        self.bad_rating = next((x.description for x in
            item.get_all('reviews') if int(x.reviewRating.ratingValue) < 3),
            'No Negative Rating')
        self.good_rating = next((x.description for x in
            item.get_all('reviews') if int(x.reviewRating.ratingValue) > 3),
            'No Positive Rating')
        self.brand = item.brand.name
        self.rating_count = int(item.aggregateRating.reviewCount)
        self.avgrating = Decimal(item.aggregateRating.ratingValue)


def typematch(item, itemtype=''):
    return str(item.itemtype[0]) == itemtype

bestbuy = 'http://www.bestbuy.com/site/misc/new-technology/pcmcat234500050002.c?id=pcmcat234500050002'
found_schema_items = microdata.get_items(urllib.request.urlopen(bestbuy))
item_feed = html.fromstring(urllib.request.urlopen(bestbuy).read())

bestbuybaseurl = 'http://www.bestbuy.com'

# find all links to products
links = [bestbuybaseurl+x.get('href') for x in
        list(itertools.chain.from_iterable([x.getchildren() for x in
            item_feed.find_class('offer-link')]))]

#follow links and scrape the schema objects from them
top_products = list(filter(lambda item: typematch(item, itemtype =
    'http://schema.org/Product'),
    itertools.chain.from_iterable([microdata.get_items(urllib.request.urlopen(link))
        for link in links])))


#translate schema objects into database schema
top_products_models = [Product(x) for x in top_products]
for x in top_products_models:
    session.add(x)
session.commit()
