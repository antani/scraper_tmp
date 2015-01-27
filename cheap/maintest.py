from parsers.flipkart_parser import FlipkartParser
from parsers.amazon_parser import AmazonParser
from parsers.snapdeal_parser import SnapdealParser
from parsers.infibeam_parser import InfibeamParser
from parsers.ebay_parser import EbayParser
from parsers.crossword_parser import CrosswordParser
from parsers.uread_parser import UreadParser
import pprint

if __name__ == '__main__':
    #flipkart_book_parser('algorithms')

    # t = FlipkartParser()
    # print t.flipkart_rest_parser('Levis 501 Jeans')
    # print t.flipkart_book_parser('introduction to algorithms')
    # print '-' * 10
    # print t.flipkart_book_parser('Autobiography of a Yogi')
    # print '-' * 10
    # print t.flipkart_rest_parser('Vans Classics Authentic Canvas Shoes')
    # t= AmazonParser()
    # pprint.pprint(t.amazon_parser('Introduction to Algorithms'))
    # pprint.pprint(t.amazon_parser('kindle paperwhite'))
    # pprint.pprint(t.amazon_parser('Many Poko Pants'))
    # t= SnapdealParser()
    # pprint.pprint(t.snapdeal_parser('Many Poki Pants'))
    # pprint.pprint(t.snapdeal_parser('LG 32 inch LED'))
    # pprint.pprint(t.snapdeal_parser('Chromecast'))
    # t= InfibeamParser()
    # pprint.pprint(t.infibeam_parser('Introduction to Algorithms'))
    # pprint.pprint(t.infibeam_parser('XOLO Opus 3'))
    # t= EbayParser()
    # pprint.pprint(t.ebay_parser('Introduction to Algorithms'))
    # pprint.pprint(t.ebay_parser('XOLO Opus 3'))
    # t= CrosswordParser()
    # pprint.pprint(t.crossword_parser('Introduction to Algorithms'))

    t= UreadParser()
    pprint.pprint(t.uread_parser('Introduction to Algorithms'))


