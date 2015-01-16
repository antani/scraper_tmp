__author__ = 'vantani'
from lxml import html
from lxml.cssselect import CSSSelector
import requests
import pylibmc
from lxml.html import parse,tostring
from pyquery import PyQuery as pq
from lxml import etree


mc = pylibmc.Client(["127.0.0.1"], binary=True,behaviors={"tcp_nodelay": True,"ketama": True})

def get_page(url):
    doc = parse(url).getroot()
    doc.make_links_absolute()
    return tostring(doc)

def flipkart_book_parser(search_term):

    if 'flipkart_test_{0}'.format(search_term) in mc:
        page=mc['flipkart_test_{0}'.format(search_term)]
    else:
        page=get_page('http://www.flipkart.com/search?q={0}'.format(search_term))
        mc['flipkart_test_{0}'.format(search_term)] =page

    d = pq(page)
    print d('div.pu-final').text()
    print d('a.lu-title').text()
    print d('div.lu-title-wrapper span.fk-font-11').text()
    print d('div.pu-discount').text()


def flipkart_mobile_parser(search_term):

    if 'flipkart_test_{0}'.format(search_term) in mc:
        page=mc['flipkart_test_{0}'.format(search_term)]
    else:
        page=get_page('http://www.flipkart.com/search?q={0}'.format(search_term))
        mc['flipkart_test_{0}'.format(search_term)] =page

    d = pq(page)
    print d('div.pu-final').text()
    print d('div.pu-title a').text()
    print d('a.pu-image img').attr('src')
    print d('ul.pu-usp').text()


if __name__ == '__main__':
    flipkart_book_parser('algorithms')
    #flipkart_mobile_parser('lenovo vibe')