__author__ = 'vantani'
# -*- coding: utf-8 -*-
import logging
import logging.config
import memcache
from memorised.decorators import memorise, memcache_none
from hashlib import md5
from lxml.html import parse,tostring
from pyquery import PyQuery as pq
from profilehooks import timecall
import re

mc = None
BASE_URL="http://www.amazon.in/s/field-keywords="
logging.config.fileConfig('logging.conf')
logger = logging.getLogger("root")

def getkey(str):
    key = str.encode('utf8')
    key = md5(key).hexdigest()
    logger.debug( key)
    return key

class AmazonParser:

    def __init__(self):
        self.mc = memcache.Client(['localhost:11211'], debug=1)

    def get_page(self,search_term,search_type="Rest"):
        val=self.mc.get(getkey("%s%s%s" % ("amazon",search_term,search_type)))
        if val is None:
            val = parse(BASE_URL+search_term).getroot()
            val.make_links_absolute()
            self.mc.set(getkey("%s%s%s" % ("amazon",search_term,search_type)),tostring(val))
        return val


    def amazon_parser(self,search_term):
        d = pq(self.get_page(search_term,"book"))
        price_d = d('div.a-row.a-spacing-none:nth-child(2) a.a-link-normal.a-text-normal span.a-size-base.a-color-price.s-price.a-text-bold').map(lambda i, e: pq(e).text())
        for p in price_d:
            logger.debug(p)

        name_d = d('h2.a-size-medium.s-inline.s-access-title.a-text-normal').map(lambda i, e: pq(e).text())
        for p in name_d:
            logger.debug(p)

        author_d = d('div.a-row.a-spacing-small div.a-row.a-spacing-none').map(lambda i, e: pq(e).text())
        for p in author_d:
            logger.debug(p)

        discount_d = d('div.a-row.a-spacing-none span.a-size-small.a-color-price').map(lambda i, e: pq(e).text())
        for p in discount_d:
            logger.debug(p)

        img_d = d('a.a-link-normal.a-text-normal img.s-access-image.cfMarker').map(lambda i, e: pq(e).attr('src'))
        for p in img_d:
            logger.debug(p)

        url_d = d('div.a-row.a-spacing-small a.a-link-normal.s-access-detail-page.a-text-normal').map(lambda i, e: pq(e).attr('href'))
        for p in url_d:
            logger.debug(p)

        prices=[]
        for price,name,author,discount,img,url in map(None, price_d,name_d,author_d,discount_d,img_d, url_d):
            prices.append({'source':'amazon', 'price':price,
                           'name':name,
                           'author':author,
                           'discount':discount,'img':img,
                           'url':url
                           })

        logger.debug( prices)
        return prices

