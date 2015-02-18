__author__ = 'vantani'
from threading import Thread
# Ref: http://stackoverflow.com/questions/3239617/how-to-manage-python-threads-results
from parsers import flipkart_parser
from parsers import amazon_parser
from parsers import infibeam_parser
from parsers import bookadda_parser
from parsers import crossword_parser
from parsers import ebay_parser
from parsers import junglee_parser
from parsers import landmark_parser
from parsers import snapdeal_parser
from parsers import uread_parser

def flipkart_books_handler(outList,search_term,search_type):
    t = flipkart_parser.FlipkartParser()
    # Modify existing object (important!)
    outList.append(t.flipkart_book_parser(search_term,search_type))

def flipkart_handler(outList,search_term,search_type):
    t = flipkart_parser.FlipkartParser()
    outList.append(t.flipkart_rest_parser(search_term,search_type))

def amazon_handler(outList,search_term,search_type):
    t= amazon_parser.AmazonParser()
    outList.append(t.parse(search_term,search_type))

def infibeam_handler(outList,search_term,search_type):
    t= infibeam_parser.InfibeamParser()
    outList.append(t.parse(search_term,search_type))

def bookadda_handler(outList,search_term,search_type):
    t= bookadda_parser.BookaddaParser()
    outList.append(t.parse(search_term,search_type))

def crossword_handler(outList,search_term,search_type):
    t= crossword_parser.CrosswordParser()
    outList.append(t.parse(search_term,search_type))

def ebay_handler(outList,search_term,search_type):
    t= ebay_parser.EbayParser()
    outList.append(t.parse(search_term,search_type))

def junglee_handler(outList,search_term,search_type):
    t= junglee_parser.JungleeParser()
    outList.append(t.parse(search_term,search_type))

def landmark_handler(outList,search_term,search_type):
    t= landmark_parser.LandmarkParser()
    outList.append(t.parse(search_term,search_type))

def snapdeal_handler(outList,search_term,search_type):
    t= snapdeal_parser.SnapdealParser()
    outList.append(t.parse(search_term,search_type))

def uread_handler(outList,search_term,search_type):
    t= uread_parser.UreadParser()
    outList.append(t.parse(search_term,search_type))


def doStuffWith(keyword,search_term,search_type):
    result = []
    handlers = {'flipkart_books':flipkart_books_handler,'flipkart':flipkart_handler,'amazon':amazon_handler,
                'infibeam':infibeam_handler, 'crossword':crossword_handler,
                'bookadda':bookadda_handler,'ebay':ebay_handler,
                'junglee':junglee_handler,'landmark': landmark_handler,'snapdeal':snapdeal_handler,
                'uread':uread_handler}

    target=handlers[keyword]
    thread = Thread(target=target, args=(result,search_term,search_type,))
    return(thread, result)

def process(search_type, search_term):
    processors = []
    if search_type == 'books':
        processors=['flipkart_books','amazon','crossword','ebay','infibeam','bookadda','junglee','landmark','uread']
    elif search_type in ['mobiles','electronics','kitchen','tv','laptop','computers']:
        processors=['flipkart','amazon','ebay','junglee','snapdeal']

    threads = [doStuffWith(k,search_term,search_type) for k in processors]
    results=[]
    for t in threads:
        t[0].start()
    for t in threads:
        t[0].join()
        ret = t[1]
        if ret:
            for r in ret[0]:
                results.append(r)

    # Sort name weight descending and price ascending
    # http://stygianvision.net/updates/python-sort-list-object-dictionary-multiple-key/
    sorted_items = sorted(results, key=lambda k: (-k['weight'], k['price']))
    return sorted_items

if __name__ == '__main__':
    print process('books','algorithms')