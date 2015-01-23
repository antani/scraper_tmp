from parsers.flipkart_parser import FlipkartParser
from parsers.amazon_parser import AmazonParser
import pprint

if __name__ == '__main__':
    #flipkart_book_parser('algorithms')

    # t = FlipkartParser()
    # print t.flipkart_rest_parser('Levis 501 Jeans')
    # print '-' * 10
    # print t.flipkart_book_parser('introduction to algorithms')
    # print '-' * 10
    # print t.flipkart_book_parser('Autobiography of a Yogi')
    # print '-' * 10
    # print t.flipkart_rest_parser('Vans Classics Authentic Canvas Shoes')
    t= AmazonParser()
    pprint.pprint(t.amazon_book_parser('Introduction to Algorithms'))