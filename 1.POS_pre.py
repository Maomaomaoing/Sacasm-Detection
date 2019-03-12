# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 14:10:25 2017

@author: user
"""

import csv
import jieba
import numpy as np
import jieba.posseg

contents = []
POS = ['Ag', 'a', 'ad', 'an', 'b', 'c', 'dg', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm','Ng', 'n', 'nr', 'ns', 'nt', 'nz', 'o', 'p', 'q', 'r', 's', 'tg', 't', 'u', 'vg', 'v', 'vd', 'vn', 'w', 'x', 'y', 'z', 'un']
all_POS = ['a', 'c', 'd', 'e', 'eng', 'm', 'n', 'non', 'p', 'q', 't', 'u', 'v', 'x']
POS_dict = dict(zip(all_POS,range(1,15)))

def decrease(POS) :
    # a, non, c, d, m, n, p, q, t, u, v, eng, x, e
      
    n_POS = ['ng', 'nr', 'nrfg', 'nrt', 'ns', 'nt', 'nz', 'r', 'rg', 'rr', 'rz', 's']
    v_POS = ['vd', 'vg', 'vi', 'vn', 'vq']
    a_POS = ['ad', 'ag', 'an', 'z', 'zg']
    d_POS = ['df', 'dg']
    m_POS = ['mg', 'mq']
    t_POS = ['tg']
    u_POS = ['ud', 'ug', 'uj', 'ul', 'uv', 'uz']
    e_POS = ['e', 'y', 'o']

    if n_POS.count(POS) > 0 :
        POS = 'n'
    elif v_POS.count(POS) > 0 :
        POS = 'v'
    elif a_POS.count(POS) > 0 :
        POS = 'a' 
    elif d_POS.count(POS) > 0 :
        POS = 'd' 
    elif m_POS.count(POS) > 0 :
        POS = 'm' 
    elif t_POS.count(POS) > 0 :
        POS = 't' 
    elif u_POS.count(POS) > 0 :
        POS = 'u' 
    elif e_POS.count(POS) > 0 :
        POS = 'e' 
    elif all_POS.count(POS) == 0 :
        POS = 'non' 
    return POS


"""切成句"""
f = open('mobile00.csv', 'r', encoding='utf-8')
for row in csv.reader(f): #每行一篇評論 
    contents.extend(row[3].split("  "))
f.close()
print('cut sentence complete')

"""刪除空白"""
for c,sen in enumerate(contents):
    if len(contents[c])>=1:
        if contents[c][0] == ' ':
            if contents[c][1] == ' ':
                contents[c] = contents[c][2:]
            else:
                contents[c] = contents[c][1:]
    else:
        del contents[c]
print('delete space complete')   
print('not sarcasm sen num: '+str(len(contents)))
#contents = contents[:1201] #取500筆

"""讀取嘲諷句"""
f = open('irony.txt','r', encoding='utf-8')
for row in csv.reader(f):
    contents.extend(row)
print('total sen num: '+str(len(contents)))

"""切成詞，判斷詞性"""
content_POS = []
for s,sentence in enumerate(contents):
    sentence_POS = []
    seg = jieba.posseg.cut(sentence)
    for w in seg:
        w.flag = decrease(w.flag)
        sentence_POS.append([w.word, POS_dict.get(w.flag)])
    content_POS.append(sentence_POS)
    if (s+1) % 1000 == 0:
        print('sentence',s+1,' complete')
np.save('all_content_POS',content_POS)

#content_POS = np.load('content_POS.npy')