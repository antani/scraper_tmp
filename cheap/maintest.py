__author__ = 'vantani'
# -*- coding: utf-8 -*-
#import pylibmc
import memcache
from memorised.decorators import memorise, memcache_none

from lxml.html import parse,tostring
from pyquery import PyQuery as pq
from profilehooks import timecall
import re

#mc = pylibmc.Client(["127.0.0.1"], binary=True,behaviors={"tcp_nodelay": True,"ketama": True})
mc = memcache.Client(['localhost:11211'], debug=0)
mc.flush_all()

BASE_URL="http://www.flipkart.com/search?q="

# Helper functions to clean up price values to a number
def sanitize_price(price_value):
    #Remove all Rupee symbols and commas
    cleaned_price = price_value.strip().replace(',','').replace(u'\u20b9','')
    #Remove all characters except a .
    non_decimal = re.compile(r'[^\d.]+')
    price_digs = non_decimal.sub('', cleaned_price)
    #After this there might be a leading . , remove it
    #print source,"---",price_digs

    if price_digs =='':
        return 0

    if price_digs[0] == '.':
        price = price_digs[1:]
    else:
        price = price_digs
    return price


@memorise()
@timecall(immediate=False)
def get_page(search_term):
    # if 'flipkart_test_{0}'.format(search_term) in mc:
    #     page=mc['flipkart_test_{0}'.format(search_term)]
    #     return page
    # else:
    doc = parse(BASE_URL+search_term).getroot()
    doc.make_links_absolute()
    #mc['flipkart_test_{0}'.format(search_term)] = tostring(doc)
    return tostring(doc)

@timecall(immediate=False)
def flipkart_book_parser(search_term):

    d = pq(get_page(search_term))
    print d('div.pu-final').text()
    print d('a.lu-title').text()
    print d('div.lu-title-wrapper span.fk-font-11').text()
    print d('div.pu-discount').text()
    for elem in  d('div.lu-image a.lu-image-link img'):
        print elem.get('src')
    for elem in  d('a.lu-title'):
        print elem.get('href')

@memorise(parent_keys=['search_term'])
@timecall(immediate=False)
def flipkart_rest_parser(search_term):
    d = pq(get_page(search_term))
    price_d = d('div.pu-final').map(lambda i, e: pq(e).text())
    for p in price_d:
        print p

    name_d = d('div.pu-title a').map(lambda i, e: pq(e).text())
    for p in name_d:
        print p

    img_d = d('a.pu-image img').map(lambda i, e: pq(e).attr('src'))
    for p in img_d:
        print p

    url_d = d('div.pu-title a').map(lambda i, e: pq(e).attr('href'))
    for p in url_d:
        print p

    usp_d = d('ul.pu-usp').map(lambda i, e: pq(e).text())
    for p in usp_d:
        print p

    discount_d = d('div.pu-discount').remove('span.pu-old').map(lambda i, e: pq(e).text())
    for p in discount_d:
        print p

    prices=[]
    for price, name, img, url, usp, discount in map(None, price_d,name_d,img_d,url_d,usp_d,discount_d ):
        prices.append({'source':'flipkart', 'price':sanitize_price(price),'name':name,
                       'img':img, 'url':url,'usp':usp,
                       'discount':discount})

    print prices
    return prices


if __name__ == '__main__':
    #flipkart_book_parser('algorithms')
    print '-' * 10
    flipkart_rest_parser('Huggies Diapers')
