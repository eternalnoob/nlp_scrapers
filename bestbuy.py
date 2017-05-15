import microdata
import urllib
import lxml
from lxml.cssselect import CSSSelector
from lxml import html, etree
import itertools
from functools import partial

def typematch(item, itemtype=''):
    return str(item.itemtype[0]) == itemtype
isproduct = partial(typematch, itemtype='http://schema.org/Product')

bestbuy = 'http://www.bestbuy.com/site/misc/new-technology/pcmcat234500050002.c?id=pcmcat234500050002'
found_schema_items = microdata.get_items(urllib.request.urlopen(bestbuy))
selector = CSSSelector('offer-link')
item_feed = html.fromstring(urllib.request.urlopen(bestbuy).read())

bestbuybaseurl = 'http://www.bestbuy.com'

links = [bestbuybaseurl+x.get('href') for x in  list(itertools.chain.from_iterable([x.getchildren() for x in item_feed.find_class('offer-link')]))]

top_products = list(filter(lambda item: typematch(item, itemtype =
    'http://schema.org/Product'),
    itertools.chain.from_iterable([microdata.get_items(urllib.request.urlopen(link))
        for link in links])))
