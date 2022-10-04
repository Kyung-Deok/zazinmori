#!/usr/bin/env python
# coding: utf-8

# In[71]:


import pandas as pd
import numpy as np
from konlpy.tag import Kkma
import re
from tqdm import tqdm
from collections import Counter
from string import punctuation # 구두점을 제거하는데 필요
from konlpy.tag import Mecab
import itertools
import networkx as nx
# import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')


# In[78]:


# 데이터 불러오기
df = pd.read_csv("/home/ubuntu/zzm_modelserver/datas/final_list_qtype.csv")
df


# In[73]:


def textcount(input):
    df['corp_nm'].fillna('미입력', inplace=True) # Nan값 전처리
    title_df = df[df['corp_nm'].str.contains(input, na=False)]
    etc2 = title_df[['a1', 'a2', 'a3', 'a4', 'a5']].values.astype(str).tolist()
    
    
    def strip_punctuation(s):
        return ''.join(c for c in s if c not in punctuation)

    clean_title = []
    for sent in etc2 :
        clean = strip_punctuation(sent)
        clean_title.append(clean)
    
    m = Mecab()
    dataset = []
    for i in range(len(clean_title)) :
        dataset.append(m.nouns(re.sub('[^가-힣a-zA-Z\s]', '', clean_title[i])))
        
    stopwords = [input]
    f = open("/home/ubuntu/zzm_modelserver/datas/stopwords.txt", encoding='UTF8')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        stopwords.append(line)
    f.close()

    def cleansing(document):
        corpus = []
        for d in document:
            doc = []
            for word in d:
                low_word = word.lower()
                if (low_word not in stopwords) and (len(low_word)!=1):
                    doc.append(word)
            corpus.append(doc)
        return corpus

    
    dataset = cleansing(dataset)
    dataset2 = sum(dataset, [])
    count = Counter(dataset2)
    korean = count.most_common(100)
    
    return korean


# In[74]:


# textcount('삼성전자')


# In[75]:


'''
def networkdiagram(input):
    
    a = []
    for v,b in textcount(input):
        a.append(v)

    G = nx.Graph()
    G.add_nodes_from([( input, {"count": 500 })])
    G.add_nodes_from([(tag, {"count":count}) for tag, count in textcount(input)])
    G.add_edges_from([ ( input, edge ) for edge in a ])

    plt.figure(figsize=(20,20))
    pos = nx.spring_layout(G, k=0.5) 
    node_size = [ d['count']*50 for (n,d) in G.nodes(data=True)] 
    nx.draw_networkx_nodes(G, pos, node_color='b', alpha=0.2, node_size=node_size)
    nx.draw_networkx_labels(G, pos, font_size=14, font_family='/user/share/fonts/nanum/NanumGothicBold.ttf')
    # edge_width = [ d['weight']*0.5 for (u,v,d) in G.edges(data=True)] 
    nx.draw_networkx_edges(G, pos, alpha=0.1, edge_color='black')
    plt.axis('off')
'''


# In[76]:


# networkdiagram('카카오')

