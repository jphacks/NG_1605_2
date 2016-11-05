#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gensim, logging
import sys
import string, codecs
import MeCab
from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score
# from words import words

# SVM 準備
clf = svm.SVC()

import sys
print sys.stdout.encoding

# 頑張って集めた面白げな単語対
words = [
    [u'単位', u'販売'],
    [u'萌え', u'枕草子'],
    [u'イリオモテヤマネコ', u'交通事故'],
    [u'高視聴率', u'イ'],
    [u'尖塔', u'盗まれる'],
    [u'総理', u'3次元'],
    [u'市民球団', u'ガチャピン'],
    [u'漁船', u'変死体'],
    [u'カラーバー', u'特許'],
    [u'象', u'高齢化'],
    [u'ホットライン', u'オレオレ'],
    [u'将来', u'仏'],
    [u'お年玉', u'課税'],
    [u'グー', u'スパコン'],
    [u'絵に描いた餅', u'展示'],
    [u'鬼', u'人権侵害'],
    [u'PS3', u'脳内'],
    [u'バームクーヘン', u'干し'],
    [u'猫', u'職業訓練'],
    [u'豆腐', u'四万十川'],
    [u'置き石', u'墜落'],
    [u'月', u'所有権'],
    [u'低所得', u'練炭'],
    [u'うるう年', u'ボルボックス'],
    [u'国家錬金術師', u'合格'],
    [u'患者', u'iPod'],
    [u'帰宅', u'優勝'],
    [u'総理', u'くじ引き'],
    [u'原油', u'のりたま'],
    [u'残飯', u'オブジェ'],
    [u'ど根性', u'スイカ'],
    [u'放送', u'サブリミナル'],
    [u'死刑', u'多様化'],
    [u'投票', u'ハゲ'],
    [u'想像', u'出産'],
    [u'エイプリルフール', u'経済'],
    [u'カロリー', u'発売'],
    [u'メイド', u'季語'],
    [u'おしりかじり虫', u'死者'],
    [u'紅葉', u'ペンキ'],
    [u'かわいがる', u'相撲部屋'],
    [u'ラジオ', u'カラー'],
    [u'胎内', u'暴行'],
    [u'トンヌラ', u'命名'],
    [u'エレベーター', u'統一'],
    [u'シュレディンガーの猫', u'虐待']
]

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