__author__ = 'vantani'
from flask import Flask, jsonify

import locator


app = Flask(__name__)

@app.route('/')
def index():
    pass

@app.route('/api/1.0/books/<string:title>',methods=['GET'])
def search_books(title):
    return jsonify({'results':locator.process('books',title)})

@app.route('/api/1.0/mobiles/<string:title>',methods=['GET'])
def search_mobiles(title):
    return jsonify({'results':locator.process('mobiles',title)})

if __name__ == '__main__':
    #Only for development
    app.debug = True
    app.run(port=5001)