#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gensim, logging
import sys
import string, codecs
import MeCab
from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score
from words import words

# SVM 準備
clf = svm.SVC()

import sys
print sys.stdout.encoding


def s(model, pos, nag, topn=200):
    return model.most_similar(positive=pos, negative=nag, topn=topn)

def suggest(model, word):
    output = []

    # print words
    
    max_sim = -1.0
    max_sim_word = None

    try:
        # 入力ワードと同じようなカテゴリの単語を取得
        for item in words:
            # コサイン類似度
            print type(item[0])
            print item[1]
            print word
            sim = model.similarity(word, item[0])
            print sim
            print "-" * 30
            if sim > max_sim :
                max_sim = sim
                max_sim_word = item

        print max_sim_word[0] 
        print max_sim_word[1]
        print "-" * 30

        # 選択された単語対とにた関係性の単語を取得
        for item in s(model, [max_sim_word[0], word], [max_sim_word[1]]):
            # 類似度が大きすぎる単語は弾く
            if model.similarity(word, item[0]) < 0.5 :
                output.append((item[0], model.similarity(word, item[0])))
    except KeyError:
        print "KeyError"

    return output