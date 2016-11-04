#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gensim, logging
import sys
import string, codecs
import MeCab
import json
import falcon

# reload(sys)
# sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# sys.setdefaultencoding('utf-8')

# モデル読み込み
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = gensim.models.word2vec.Word2Vec.load("jpw-wakati-model-utf8")
print "model load compl_ete"

def s(pos, nag, topn=200):
	return model.most_similar(positive=pos, negative=nag, topn=topn)

input = u'日本酒'
output = []

for item in s([u'販売', input], [u'単位']):
	if model.similarity(input, item[0]) < 0.5 :
		# 単語の連結率も算出する必要がある.
		# 単語の連結率が高いものは、珍しさがないので、推薦を行わない
		output.append((item[0], model.similarity(input, item[0])))
output[:20]

# クロスオリジンを許可
ALLOWED_ORIGINS = ['http://127.0.0.1:8080']

class CorsMiddleware(object):
	def process_request(self, request, response):
		origin = request.get_header('Origin')
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
		
		output = []
		try:
			for item in s([u'販売', param], [u'単位']):
				if model.similarity(param, item[0]) < 0.5 :
					output.append((item[0], model.similarity(param, item[0])))
		except KeyError:
			print "KeyError"
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
	httpd = simple_server.make_server("127.0.0.1", 8000, app)
	httpd.serve_forever()
