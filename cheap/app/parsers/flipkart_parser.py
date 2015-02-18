__author__ = 'vantani'
# -*- coding: utf-8 -*-

import logging
import logging.config
from hashlib import md5
from lxml.html import parse,tostring

from pyquery import PyQuery as pq
from titlecase import titlecase
import uuid
import memcache
import string_utils
from similarity import string_similarity
import re


mc = None
BASE_URL="http://www.flipkart.com/search?q="
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

class FlipkartParser:

    def __init__(self):
        #mc = pylibmc.Client(["127.0.0.1"], binary=True,behaviors={"tcp_nodelay": True,"ketama": True})
        self.mc = memcache.Client(['localhost:11211'], debug=1)
        #self.mc.flush_all()

    def get_page(self,search_term,search_type="Rest"):
        val=self.mc.get(getkey("%s%s%s" % ("flipkart",search_term,search_type)))
        if val is None:
            val = parse(BASE_URL+search_term).getroot()
            val.make_links_absolute()
            self.mc.set(getkey("%s%s%s" % ("flipkart",search_term,search_type)),tostring(val))
        return val


    def flipkart_book_parser(self,search_term,search_type):

        d = pq(self.get_page(search_term,"book"))
        price_d = d('div.pu-final').map(lambda i, e: pq(e).text())
        for p in price_d:
            logger.debug( p)

        name_d = d('a.lu-title').map(lambda i, e: pq(e).text())
        for p in name_d:
            logger.debug( p)

        author_d = d('div.lu-title-wrapper span.fk-font-11').map(lambda i, e: pq(e).text())
        for p in author_d:
            logger.debug( p)

        discount_d = d('div.pu-discount').remove('span.pu-old').map(lambda i, e: pq(e).text())
        for p in discount_d:
            logger.debug( p)

        img_d = d('div.lu-image a.lu-image-link img').map(lambda i, e: pq(e).attr('src'))
        for p in img_d:
            logger.debug( p)

        url_d = d('a.lu-title').map(lambda i, e: pq(e).attr('href'))
        for p in url_d:
            logger.debug( p)

        prices=[]
        for price, name, img, url, author, discount in map(None, price_d,name_d,img_d,url_d,author_d,discount_d ):
            if price:
                if name:
                    weight = string_similarity(string_utils.clean_words(search_term), string_utils.clean_words(name))
                else:
                    weight = 0.0

                price = {'uuid':str(uuid.uuid4()),'source':'http://localhost/static/cache/images/stores/Flipkart.png', 'price':float(sanitize_price(price)),'name':(name),
                         'img':img if string_utils.is_url(img) else 'http://google.com', 'url':url,'author':author,
                         'discount':' '.join(discount.split()) if discount else None,
                         'weight':weight,'type':search_type}
                if price:
                    self.mc.set(price['uuid'],price,time=84000)
                    prices.append(price)

        logger.debug( prices)
        return prices



    def flipkart_rest_parser(self, search_term,search_type):
        d = pq(self.get_page(search_term))
        price_d = d('div.pu-final').map(lambda i, e: pq(e).text())
        for p in price_d:
            logger.debug( p)

        name_d = d('div.pu-title a').map(lambda i, e: pq(e).text())
        for p in name_d:
            logger.debug( p)

        img_d = d('a.pu-image img').map(lambda i, e: pq(e).attr('src'))
        for p in img_d:
            logger.debug( p)

        url_d = d('div.pu-title a').map(lambda i, e: pq(e).attr('href'))
        for p in url_d:
            logger.debug( p)

        usp_d = d('ul.pu-usp').map(lambda i, e: pq(e).text())
        for p in usp_d:
            logger.debug( p)

        discount_d = d('div.pu-discount').remove('span.pu-old').map(lambda i, e: pq(e).text())
        for p in discount_d:
            logger.debug( p)

        prices=[]
        for price, name, img, url, usp, discount in map(None, price_d,name_d,img_d,url_d,usp_d,discount_d ):
            if price:
                if name:
                    weight = string_similarity(string_utils.clean_words(search_term), string_utils.clean_words(name))
                else:
                    weight = 0.0


                price={'uuid':str(uuid.uuid4()),'source':'http://localhost/static/cache/images/stores/Flipkart.png', 'price':float(sanitize_price(price)),'name':name,
                       'img':img if string_utils.is_url(img) else 'http://google.com', 'url':url,'usp':usp,
                       'discount':discount,'type':search_type,
                       'weight':weight}

                if price:
                    self.mc.set(price['uuid'],price,time=84000)
                    prices.append(price)

        logger.debug(prices)
        return prices


