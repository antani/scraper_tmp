import pprint

from cheap.app.parsers.junglee_parser import JungleeParser


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
    # pprint.pprint(t.parse('Introduction to Algorithms'))
    # pprint.pprint(t.parse('kindle paperwhite'))
    # pprint.pprint(t.parse('Many Poko Pants'))
    # t= SnapdealParser()
    # pprint.pprint(t.parse('Many Poki Pants'))
    # pprint.pprint(t.parse('LG 32 inch LED'))
    # pprint.pprint(t.parse('Chromecast'))
    # t= InfibeamParser()
    # pprint.pprint(t.parse('Introduction to Algorithms'))
    # pprint.pprint(t.parse('XOLO Opus 3'))
    # t= EbayParser()
    # pprint.pprint(t.parse('Introduction to Algorithms'))
    # pprint.pprint(t.parse('XOLO Opus 3'))
    # t= CrosswordParser()
    # pprint.pprint(t.parse('Introduction to Algorithms'))

    # t= UreadParser()
    # pprint.pprint(t.parse('Introduction to Algorithms'))
    # t= LandmarkParser()
    # pprint.pprint(t.parse('Introduction to Algorithms'))
    #t= BookaddaParser()
    #pprint.pprint(t.parse('Introduction to Algorithms'))
    t= JungleeParser()
    pprint.pprint(t.parse('Introduction to Algorithms'))


