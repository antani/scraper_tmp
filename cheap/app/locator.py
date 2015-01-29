__author__ = 'vantani'
from threading import Thread
# Ref: http://stackoverflow.com/questions/3239617/how-to-manage-python-threads-results
import sys
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



def multikeysort(items, columns):
    from operator import itemgetter

    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in
                 columns]

    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
            else:
                return 0

    return sorted(items, cmp=comparer)



def flipkart_books_handler(outList,search_term):
    t = flipkart_parser.FlipkartParser()
    # Modify existing object (important!)
    outList.append(t.flipkart_book_parser(search_term))

def flipkart_handler(outList,search_term):
    t = flipkart_parser.FlipkartParser()
    outList.append(t.flipkart_rest_parser(search_term))

def amazon_handler(outList,search_term):
    t= amazon_parser.AmazonParser()
    outList.append(t.parse(search_term))

def infibeam_handler(outList,search_term):
    t= infibeam_parser.InfibeamParser()
    outList.append(t.parse(search_term))

def bookadda_handler(outList,search_term):
    t= bookadda_parser.BookaddaParser()
    outList.append(t.parse(search_term))

def crossword_handler(outList,search_term):
    t= crossword_parser.CrosswordParser()
    outList.append(t.parse(search_term))

def ebay_handler(outList,search_term):
    t= ebay_parser.EbayParser()
    outList.append(t.parse(search_term))

def junglee_handler(outList,search_term):
    t= junglee_parser.JungleeParser()
    outList.append(t.parse(search_term))

def landmark_handler(outList,search_term):
    t= landmark_parser.LandmarkParser()
    outList.append(t.parse(search_term))

def snapdeal_handler(outList,search_term):
    t= snapdeal_parser.SnapdealParser()
    outList.append(t.parse(search_term))

def uread_handler(outList,search_term):
    t= uread_parser.UreadParser()
    outList.append(t.parse(search_term))


def doStuffWith(keyword,search_term):
    result = []
    handlers = {'flipkart_books':flipkart_books_handler,'flipkart':flipkart_handler,'amazon':amazon_handler,
                'infibeam':infibeam_handler, 'crossword':crossword_handler,
                'bookadda':bookadda_handler,'ebay':ebay_handler,
                'junglee':junglee_handler,'landmark': landmark_handler,'snapdeal':snapdeal_handler,
                'uread':uread_handler}

    target=handlers[keyword]
    thread = Thread(target=target, args=(result,search_term,))
    return(thread, result)

def process(search_type, search_term):
    processors = []
    if search_type == 'books':
        processors=['flipkart_books','amazon','crossword','ebay','infibeam','bookadda','junglee','landmark','uread']
    else:
        processors=['flipkart','amazon','ebay','junglee','snapdeal']

    threads = [doStuffWith(k,search_term) for k in processors]
    results=[]
    for t in threads:
        t[0].start()
    for t in threads:
        t[0].join()
        ret = t[1]
        for r in ret[0]:
            results.append(r)

    sorted_items = multikeysort(results, ['-weight','price'])
    return sorted_items

if __name__ == '__main__':
    print process('books','algorithms')