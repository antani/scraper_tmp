__author__ = 'vantani'
# -*- coding: utf-8 -*-
import logging
import logging.config
from hashlib import md5
from lxml.html import parse,tostring

from pyquery import PyQuery as pq
from titlecase import titlecase

import memcache
import re
from similarity import string_similarity
import string_utils
import uuid

mc = None
BASE_URL="http://www.amazon.in/s/field-keywords="
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


    def parse(self,search_term,search_type):
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
            if price:
                if name:
                    weight = string_similarity(string_utils.clean_words(search_term), string_utils.clean_words(name))
                else:
                    weight = 0.0

                uuid_tmp=str(uuid.uuid4())

                price={'uuid':uuid_tmp,'source':'http://localhost/static/cache/images/stores/Amazon.png', 'price':float(sanitize_price(price)),
                       'name':titlecase(name),
                       'author':author,
                       'discount':discount,'img':img if string_utils.is_url(img) else 'http://google.com',
                       'url':url,'weight':weight,'type':search_type
                       }

                if price:
                    self.mc.set(uuid_tmp,price,time=84000)
                    prices.append(price)

        logger.debug( prices)
        return prices

