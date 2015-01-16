__author__ = 'vantani'
import pylibmc
from lxml.html import parse,tostring
from pyquery import PyQuery as pq
from profilehooks import timecall

mc = pylibmc.Client(["127.0.0.1"], binary=True,behaviors={"tcp_nodelay": True,"ketama": True})
BASE_URL="http://www.flipkart.com/search?q="

@timecall(immediate=False)
def get_page(search_term):
    if 'flipkart_test_{0}'.format(search_term) in mc:
        page=mc['flipkart_test_{0}'.format(search_term)]
        return page
    else:
        doc = parse(BASE_URL+search_term).getroot()
        doc.make_links_absolute()
        mc['flipkart_test_{0}'.format(search_term)] = tostring(doc)
        return tostring(doc)

@timecall(immediate=False)
def flipkart_book_parser(search_term):

    d = pq(get_page(search_term))
    print d('div.pu-final').text()
    print d('a.lu-title').text()
    print d('div.lu-title-wrapper span.fk-font-11').text()
    print d('div.pu-discount').text()

@timecall(immediate=False)
def flipkart_mobile_parser(search_term):
    d = pq(get_page(search_term))
    print d('div.pu-final').text()
    print d('div.pu-title a').text()
    print d('a.pu-image img').attr('src')
    print d('ul.pu-usp').text()


if __name__ == '__main__':
    flipkart_book_parser('algorithms')
    print '-' * 10
    flipkart_mobile_parser('lenovo vibe')