# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 20:18:14 2017

@author: user
"""
import csv
import numpy as np
from gensim.models import word2vec

content_POS = list(np.load('all_content_POS.npy'))

"""取出n,a,d,v詞性的詞"""
sentiment_POS = []
sentiment_content = []
ADNV = [1,3,7,13]
for sentence in content_POS:
    sen = []
    for word in sentence:
        if word[1] in ADNV:
            sen.append(word)
    if len(sen) != 0:
        sentiment_POS.append(sen)

"""刪除停用詞"""
print("delete stopword")
stopwordset = set()
with open('stopwords.txt','r',encoding='utf-8') as sw:
    stopwordset.add(' ')
    for line in sw:
        stopwordset.add(line.strip('\n'))

for sentence in sentiment_POS:
    temp_sen = []
    for word in sentence:
        if word[0] not in stopwordset:
            temp_sen.append(word[0])
    sentiment_content.append(temp_sen)              
        
f = open('sentiment_content.txt', 'w', encoding='utf-8')
spamwriter = csv.writer(f, lineterminator = '\n', delimiter=' ', quoting = csv.QUOTE_NONE)
spamwriter.writerows(sentiment_content)
f.close() 



"""訓練詞向量"""
print("train word2vec")
sentences = word2vec.Text8Corpus('sentiment_content.txt')
model = word2vec.Word2Vec(sentences, size=250) # default sg = 0, use CBOW, hs = 0, use negative smapling
model.save_word2vec_format(u'med250.model.bin', binary=True)

"""bin檔轉txt，讀單詞向量"""
model = word2vec.Word2Vec.load_word2vec_format('med250.model.bin', binary=True)
model.save_word2vec_format('med250.model.txt', binary=False)

word_list = []
vec_list = []
f = open('med250.model.txt','r',encoding = 'utf-8')
for r,row in enumerate(csv.reader(f)):
    if r==0:       
        line = row[0].split(' ')
        total_num = int(line[0])
        vec_len = int(line[1])
        #np.save('total_num',total_num)
    else:
        line = row[0].split(' ')
        word = line[0]
        vec = []
        for v in line[1:250]:
            vec.extend([float(v)])
        word_list.extend([word])
        vec_list.append(vec)
np.save('word_list',word_list)
np.save('vec_list',vec_list)
f.close()
# word_vec = [list(np.load('word_list.npy')),np.load('vec_list.npy')]
