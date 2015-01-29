__author__ = 'vantani'
# -*- coding: utf-8 -*-
import logging
import logging.config
import memcache
import re
from memorised.decorators import memorise, memcache_none
from hashlib import md5
from lxml.html import parse,tostring
from pyquery import PyQuery as pq
from profilehooks import timecall
import urllib
import requests
from lxml import html
from similarity import string_similarity

mc = None
BASE_URL="http://www.junglee.com/mn/search/junglee/ref=nav_sb_noss?field-keywords={0}&rush=n"
logging.config.fileConfig('../logging.conf')
logger = logging.getLogger("root")

# Helper functions to clean up price values to a number
def sanitize_price(price_value):
    # Remove all Rupee symbols and commas
    cleaned_price = price_value.strip().replace(',','').replace(u'\u20b9','')
    # Remove all characters except a .
    non_decimal = re.compile(r'[^\d.]+')
    price_digs = non_decimal.sub('', cleaned_price)
    # After this there might be a leading . , remove it
    if price_digs =='':
        return 0

    if price_digs[0] == '.':
        price = price_digs[1:]
    else:
        price = price_digs
    return price


def getkey(str):
    key = str.encode('utf8')
    key = md5(key).hexdigest()
    logger.debug( key)
    return key

class JungleeParser:

    def __init__(self):
        self.mc = memcache.Client(['localhost:11211'], debug=1)

    def get_page(self,search_term,search_type="Rest"):
        val=self.mc.get(getkey("%s%s%s" % ("junglee",search_term,search_type)))
        if val is None:
            # sanitized_url = BASE_URL.format(urllib.quote(search_term))
            # val = parse(sanitized_url).getroot()
            # val.make_links_absolute()
            user_agent = {'User-agent': 'Mozilla/5.0'}
            response = requests.get(BASE_URL.format(urllib.quote(search_term)), headers=user_agent)
            val = html.fromstring(response.text)
            self.mc.set(getkey("%s%s%s" % ("junglee",search_term,search_type)),tostring(val))
        return val


    def parse(self,search_term):
        d = pq(self.get_page(search_term,"Rest"))

        price_d = d('div#atfResults.grid.results.largeGridResult.cols4 div.results-row div.data div.prodAds span.price').map(lambda i, e: pq(e).text())
        for p in price_d:
            logger.debug(p)

        name_d = d('div#atfResults.grid.results.largeGridResult.cols4 div.results-row div.data h3.title a.title').map(lambda i, e: pq(e).text())
        for p in name_d:
            logger.debug(p)

        author_d = d('div#atfResults.grid.results.largeGridResult.cols4 div.results-row div.data h3.title span.ptBrand').map(lambda i, e: pq(e).text())
        for p in author_d:
            logger.debug(p)

        discount_d = d('div.results-row div.data div.prodAds div.listPriceContainer span.listPriceSavings').map(lambda i, e: pq(e).text())
        for p in discount_d:
            logger.debug(p)

        img_d = d('div.results-row div.image.imageContainer a.faceout-image-anchor img').map(lambda i, e: pq(e).attr('src'))
        for p in img_d:
            logger.debug(p)

        url_d = d('div#atfResults.grid.results.largeGridResult.cols4 div.results-row div.data h3.title a.title').map(lambda i, e: pq(e).attr('href'))
        for p in url_d:
            logger.debug(p)

        prices=[]
        for price,name,author,discount,img,url in map(None, price_d,name_d,author_d,discount_d,img_d, url_d):
            if price:
                prices.append({'source':'junglee', 'price':float(sanitize_price(price)),
                               'name':name,
                               'author':author,
                               'discount':discount,'img':img,
                               'url':url,
                               'weight':string_similarity(search_term,name) if name else None})

        logger.debug( prices)
        return prices

