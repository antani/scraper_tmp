from parsers.flipkart_parser import FlipkarParser

if __name__ == '__main__':
    #flipkart_book_parser('algorithms')

    t = FlipkarParser()
    print t.flipkart_rest_parser('Levis 501 Jeans')
    print '-' * 10
    print t.flipkart_book_parser('introduction to algorithms')
    print '-' * 10
    print t.flipkart_book_parser('Autobiography of a Yogi')
    print '-' * 10
    print t.flipkart_rest_parser('Vans Classics Authentic Canvas Shoes')