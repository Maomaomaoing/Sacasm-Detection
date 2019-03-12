# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 13:13:35 2017

@author: user
"""

import csv
import numpy as np
from gensim import models
import math
from numpy import array

def update_pn_list():
    temp_set = positive_word | negative_word
    positive_word.clear()
    negative_word.clear()
    for word in word_score:
        if word not in temp_set:
            if word_score[word] > 0:
                positive_word.add(word)
            if word_score[word] < 0:
                negative_word.add(word)
    print('p: '+str(len(positive_word)),'n: '+str(len(negative_word)))
    
    
    
"""建立極性詞典"""

words = set()
f = open('sentiment_content.txt', 'r', encoding='utf-8')
for row in csv.reader(f): 
    if len(row) > 0:
        for word in row[0].split(" "):
            words.add(word)
f.close()

word_score = dict(zip(words,[0]*len(words)))
print('total word: '+str(len(word_score)))

#np.save('word_score',word_score)
#word_score = np.load('word_score.npy')

"""載入情緒字典"""
positive_word = []
negative_word = []

f = open('NTUSD_positive_traditional.csv', 'r', encoding='utf-8')
spamreader = csv.reader(f, delimiter='\n')
for row in spamreader:
    positive_word.extend(row)
f.close()
positive_word = set(positive_word)
f = open('NTUSD_negative_traditional.csv', 'r', encoding='utf-8')
spamreader = csv.reader(f, delimiter='\n')
for row in spamreader:
    negative_word.extend(row)
f.close()
negative_word = set(negative_word)

"""標記已在字典中的字"""

for word in word_score:
    if word in positive_word:
        word_score[word] += 1 
        #print(word)
    if word in negative_word:
        word_score[word] -= 1 
        #print(word)
print('1')
positive_word.clear()
negative_word.clear()
for word in word_score:
    if word_score[word] > 0:
        positive_word.add(word)
    if word_score[word] < 0:
        negative_word.add(word)
print('p: '+str(len(positive_word)),'n: '+str(len(negative_word)))
     
        
"""載入w2v model"""
model = models.Word2Vec.load_word2vec_format('med250.model.bin',binary=True)

"""第2~8輪標記"""

err_num = []

for n in range(7):
    print(n+2)
    for word in positive_word:
        try:
            res = model.most_similar(word,topn = 5)
            for item in res:
                    word_score[item[0]] += item[1]*word_score[word]
        except:
            err_num.append(word)
    for word in negative_word:
        try:
            res = model.most_similar(word,topn = 5)
            for item in res:
                    word_score[item[0]] += item[1]*word_score[word]
        except:
            err_num.append(word)          
    update_pn_list()
    print('t: '+str(sum(map(lambda t : 1 if t[1] != 0 else 0,word_score.items()))))
"""取log"""

for word in word_score:
    if word_score[word] > 0:
        word_score[word] = math.log10(word_score[word])
    elif word_score[word] < 0:
        word_score[word] = -(math.log10(math.fabs(word_score[word])))
   

"""儲存極性詞典"""
#np.save('word_score',word_score)
np.save('word',list(word_score.keys()))
np.save('score',list(word_score.values()))
positive_word = list(positive_word)
negative_word = list(negative_word)
np.save('positive_word',positive_word)
np.save('negative_word',negative_word)

f = open('positive_word.txt','w')
f.writelines('\n'.join(positive_word))
f.close()

f = open('negative_word.txt','w')
f.writelines('\n'.join(negative_word))
f.close()

print('word, POS, score, vector')

"""將sen score, word score, POS儲存在一起"""
content_POS = list(np.load('all_content_POS.npy'))

"""只取一部分非嘲諷"""
np.random.seed(1)
# 376, not sarcasm = 4000-376 = 3624, total = 4000
content_POS_score = list(np.random.choice(content_POS[:564021],3624))
content_POS_score.extend(content_POS[564022:])
content_POS = content_POS_score
content_POS_score = []
word_score = dict(zip(np.load('word.npy'),np.load('score.npy')))

for s,sentence in enumerate(content_POS):
    temp = [0.0]
    total_score = 0.0
    #content_POS_score[s].insert(0,total_score)
    for w,word in enumerate(sentence):
        if word[0] in word_score:
            score = word_score[word[0]]
            total_score = total_score + score
        else:
            score = 0.0
        temp.extend([word[1],score])
    temp[0] = total_score
    content_POS_score.append(temp)

np.save('content_POS_score',content_POS_score)

"""轉成CNN輸入形式"""
data = list(np.load('content_POS_score.npy'))

n_sar = 3624
sar = 376
"""刪長句, 短句補0"""
too_long = []
for r,row in enumerate(data):
    if len(row) < 121:
        data[r].extend(list(np.repeat(0,121-len(row))))
for r,row in enumerate(data):        
    if len(row) > 121:
        too_long.extend([r])
for index in reversed(too_long):
    del data[index]
print("total: "+str(len(data)))

"""len"""
for r,row in enumerate(data):
    data[r] = array(data[r])
    if len(row)!=121:
        print('length not same, number '+str(r))
        
for r,row in enumerate(data):
    data[r] = array(data[r])
    
np.save('data',data)


"""
word_score = dict(zip(np.load('word.npy'),np.load('score.npy')))

for key, value in sorted(word_score.items(),key = lambda t : t[1] ):
    print("%s: %s" % (key, value))
"""
"""
for r,row in enumerate(data):
    if len(row) < 121:
        data[r].extend(list(np.repeat(0,121-len(row))))
for r,row in enumerate(data):        
    if len(row) > 121:
        del data[r]
        if r<3624:
            n_sar = n_sar-1
        else:
            sar = sar-1
print("not sarcasm: "+str(n_sar))
print("sarcasm: "+str(sar))
"""