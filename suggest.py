#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gensim, logging
import sys
import string, codecs
import MeCab
from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score

# SVM 準備
clf = svm.SVC()


def s(model, pos, nag, topn=200):
	return model.most_similar(positive=pos, negative=nag, topn=topn)

def suggest(model, word):
	output = []
	try:
		for item in s(model, [u'販売', word], [u'単位']):
			if model.similarity(word, item[0]) < 0.5 :
				output.append((item[0], model.similarity(word, item[0])))
	except KeyError:
		print "KeyError"
	return output