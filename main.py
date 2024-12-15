from flask import Flask
from flask import request, jsonify
import datetime
import json
import random
import string

app = Flask(__name__)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length))

class UrlInfo:
    def __init__(self, url, short_code):
        self.short_code = short_code
        self.url = url
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()

class UrlShortener:
    def __init__(self):
        self.url_map = {}
    def shorten(self, url):
        short_code = random_string(6)
        while short_code in self.url_map:
            short_code = random_string(6)
        url_info = UrlInfo(url, short_code)
        self.url_map[short_code] = url_info
        return self.url_map[short_code].__dict__
    def get(self, short_code):
        if short_code in self.url_map:
            return self.url_map[short_code]
        else:
            return None
    def delete(self, short_code):
        del self.url_map[short_code]

url_shortener = UrlShortener()

@app.route('/shorten', methods=['POST'])
def shorten():
    request_data = request.get_json()
    url = request_data['url']
    response = url_shortener.shorten(url)
    return jsonify(response)

@app.route('/shorten/<short_code>', methods=['GET'])
def get(short_code):
    url_info = url_shortener.get(short_code)
    if url_info:
        return jsonify(url_info.__dict__)
    else:
        return jsonify({'error': 'Not found'}), 404

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete(short_code):
    url_shortener.delete(short_code)
    return jsonify({'message': 'Deleted'})

@app.route('/shorten/<short_code>', methods=['PUT'])
def update(short_code):
    request_data = request.get_json()
    url = request_data['url']
    url_info = url_shortener.get(short_code)
    if url_info:
        url_info.url = url
        url_info.modified_at = datetime.datetime.now()
        return jsonify(url_info.__dict__)
    else:
        return jsonify({'error': 'Not found'}), 404