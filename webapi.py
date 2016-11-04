#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gensim, logging
import sys
import string, codecs
import MeCab
import json
import falcon
from sklearn import svm
from suggest import suggest

# reload(sys)
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.setdefaultencoding('utf-8')

# モデル読み込み
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = gensim.models.word2vec.Word2Vec.load("jpw-wakati-model-utf8")
print "model load compl_ete"

# クロスオリジンを許可
ALLOWED_ORIGINS = ['http://192.168.11.2', 'http://192.168.0.6']

class CorsMiddleware(object):
	def process_request(self, request, response):
		origin = request.get_header('Origin')
		print ALLOWED_ORIGINS
		if origin in ALLOWED_ORIGINS:
			response.set_header('Access-Control-Allow-Origin', origin)

class NumPyArangeEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, np.ndarray):
			return obj.tolist() # or map(int, obj)
		return json.JSONEncoder.default(self, obj)

# API
class word2vec(object):
	def on_get(self, req, resp):
		param = req.get_param("word")
		if param == None:
			# 単語が指定されていない
			print "param an error"
			resp.body = json.dumps(u'word error')
			return
		# 推薦単語を取得
		output = suggest(model, param)
		# クロスオリジンを許可
		resp.set_header('Access-Control-Allow-Origin', '*')
		# リクエスト挿入
		# resp.body = json.dumps(output[:20], cls=NumPyArangeEncoder)
		resp.body = json.dumps(output, cls=NumPyArangeEncoder)

# Falcon 起動
app = falcon.API(middleware=[CorsMiddleware()]);
app.add_route("/word2vec", word2vec())

if __name__ == "__main__":
	from wsgiref import simple_server
	# サーバ起動
	httpd = simple_server.make_server("192.168.11.4", 8000, app)
	httpd.serve_forever()