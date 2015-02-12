__author__ = 'vantani'
from flask import Flask, jsonify

import locator
import logging
import datetime
from flask import request



app = Flask(__name__)
LOG_FILENAME = 'scrapper_access_log.log'
info_log = logging.getLogger('app_info_log')
info_log.setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1024 * 1024 * 100,
    backupCount=20
    )

info_log.addHandler(handler)

@app.before_request
def pre_request_logging():
    #Logging statement
    if 'text/html' in request.headers['Accept']:
        info_log.info('\t'.join([
            datetime.datetime.today().ctime(),
            request.remote_addr,
            request.method,
            request.url,
            request.data,
            ', '.join([': '.join(x) for x in request.headers])])
        )

@app.route('/')
def index():
    pass

@app.route('/api/1.0/books/<string:title>',methods=['GET'])
def search_books(title):

    return jsonify({'results':locator.process('books',title)})

@app.route('/api/1.0/mobiles/<string:title>',methods=['GET'])
def search_mobiles(title):
    return jsonify({'results':locator.process('mobiles',title)})

@app.route('/api/1.0/tv/<string:title>',methods=['GET'])
def search_tv(title):
    return jsonify({'results':locator.process('tv',title)})

@app.route('/api/1.0/electronics/<string:title>',methods=['GET'])
def search_electronics(title):
    return jsonify({'results':locator.process('electronics',title)})

@app.route('/api/1.0/kitchen/<string:title>',methods=['GET'])
def search_kitchen(title):
    return jsonify({'results':locator.process('kitchen',title)})

@app.route('/api/1.0/laptop/<string:title>',methods=['GET'])
def search_laptop(title):
    return jsonify({'results':locator.process('laptop',title)})

@app.route('/api/1.0/computers/<string:title>',methods=['GET'])
def search_computers(title):
    return jsonify({'results':locator.process('computers',title)})

if __name__ == '__main__':
    #Only for development
    app.debug = True
    app.run(port=5001)