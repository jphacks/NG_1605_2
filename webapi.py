#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gensim, logging
import sys
import string, codecs
import MeCab
import json
import falcon

# モデル読み込み
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = gensim.models.word2vec.Word2Vec.load("jpw-wakati-model-utf8")
print "model load compl_ete"

# クロスオリジンを許可
ALLOWED_ORIGINS = ['http://127.0.0.1:8080']

class CorsMiddleware(object):
	def process_request(self, request, response):
		origin = request.get_header('Origin')
		if origin in ALLOWED_ORIGINS:
			response.set_header('Access-Control-Allow-Origin', origin)

# API
class word2vec(object):
	def on_get(self, req, resp):
		print "receive"

# Falcon 起動
app = falcon.API(middleware=[CorsMiddleware()]);
app.add_route("/word2vec", word2vec())

if __name__ == "__main__":
	from wsgiref import simple_server
	# サーバ起動
	httpd = simple_server.make_server("127.0.0.1", 8000, app)
	httpd.serve_forever()