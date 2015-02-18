__author__ = 'vantani'
# -*- coding: utf-8 -*-
import logging
import logging.config
from hashlib import md5
from lxml.html import tostring
import urllib
import requests
from lxml import html

from pyquery import PyQuery as pq
from titlecase import titlecase

import memcache
import re
from similarity import string_similarity
import string_utils
import uuid

mc = None
BASE_URL="http://www.snapdeal.com/search?keyword={0}&catId=&categoryId=&suggested=false&vertical=&noOfResults=20&clickSrc=go_header&lastKeyword=algorithms&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&url=&utmContent=&catalogID=&dealDetail="
logging.config.fileConfig('../logging.conf')
logger = logging.getLogger("root")

# Helper functions to clean up price values to a number
def sanitize_price(price_value):
    if price_value:
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

class SnapdealParser:

    def __init__(self):
        self.mc = memcache.Client(['localhost:11211'], debug=1)

    def get_page(self,search_term,search_type="Rest"):
        val=self.mc.get(getkey("%s%s%s" % ("snapdeal",search_term,search_type)))
        if val is None:
            # sanitized_url = BASE_URL.format(urllib.quote(search_term))
            # val = parse(sanitized_url).getroot()
            # val.make_links_absolute()
            user_agent = {'User-agent': 'Mozilla/5.0'}
            response = requests.get(BASE_URL.format(urllib.quote(search_term)), headers=user_agent)
            val = html.fromstring(response.text)
            self.mc.set(getkey("%s%s%s" % ("snapdeal",search_term,search_type)),tostring(val))
        return val


    def parse(self,search_term,search_type):
        d = pq(self.get_page(search_term,"book"))
        price_d = d('div.product-price div span#price').map(lambda i, e: pq(e).text())
        for p in price_d:
            logger.debug(p)

        name_d = d('div.product_grid_box div.productWrapper div.hoverProductWrapper.product-txtWrapper div.product-title a').map(lambda i, e: pq(e).text())
        for p in name_d:
            logger.debug(p)

        author_d = d('div.a-row.a-spacing-small div.a-row.a-spacing-none').map(lambda i, e: pq(e).text())
        for p in author_d:
            logger.debug(p)

        discount_d = d('div.productWrapper div.hoverProductWrapper.product-txtWrapper a#prodDetails.hit-ss-logger.somn-track.prodLink.hashAdded div.product-price div span#disc').map(lambda i, e: pq(e).text())
        for p in discount_d:
            logger.debug(p)

        img_d = d('div.hoverProductImage.product-image a img.gridViewImage').map(lambda i, e: pq(e).attr('src'))
        for p in img_d:
            logger.debug(p)

        url_d = d('div.product_grid_box div.productWrapper div.hoverProductWrapper.product-txtWrapper div.product-title a').map(lambda i, e: pq(e).attr('href'))
        for p in url_d:
            logger.debug(p)

        prices=[]
        for price,name,author,discount,img,url in map(None, price_d,name_d,author_d,discount_d,img_d, url_d):
            if name:
                    weight = string_similarity(string_utils.clean_words(search_term), string_utils.clean_words(name))
            else:
                    weight = 0.0

            uuid_tmp=str(uuid.uuid4())
            price={'uuid':uuid_tmp,'source':'http://localhost/static/cache/images/stores/Snapdeal.png', 'price': float(sanitize_price(price)),
                   'name':titlecase(name),
                   'author':author,
                   'discount':discount,'img':img if string_utils.is_url(img) else 'http://google.com',
                   'url':url,'type':search_type,
                   'weight':weight
                   }
            if price:
                self.mc.set(uuid_tmp,price,time=84000)
                prices.append(price)

        logger.debug( prices)
        return prices

