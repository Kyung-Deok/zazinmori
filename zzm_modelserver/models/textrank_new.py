#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from newspaper import Article
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
from tqdm import tqdm, tqdm_pandas
import warnings
warnings.filterwarnings('ignore')


# In[5]:


df = pd.read_csv('/home/ubuntu/zzm_modelserver/datas/News Data.csv')


# In[6]:


# 텍스트 크롤링, 문장 단위 분리, 명사 추출
class SentenceTokenizer(object):
    def __init__(self):
        self.kkma = Kkma()
        self.twitter = Twitter()
        self.stopwords = [] # 불용어 처리 단어 등록 
            
    # url 기사 크롤링 및 텍스트 단위 분리
    def url2sentences(self, url):
        article = Article(url, language='ko')
        article.download()
        article.parse()
        sentences = self.kkma.sentences(article.text)
        
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
        
        return sentences
    
    # 텍스트 단위 분리
    def text2sentences(self, text):
        sentences = self.kkma.sentences(text)      
        for idx in range(0, len(sentences)):
            if len(sentences[idx]) <= 10:
                sentences[idx-1] += (' ' + sentences[idx])
                sentences[idx] = ''
        
        return sentences
    
    # 명사 추출
    def get_nouns(self, sentences):
        nouns = []
        for sentence in sentences:
            if sentence != '':
                nouns.append(' '.join([noun for noun in self.twitter.nouns(str(sentence)) 
                                       if noun not in self.stopwords and len(noun) > 1]))
        
        return nouns


# In[7]:


# TF-IDF 모델, 그래프 생성
class GraphMatrix(object):
    def __init__(self):
        self.tfidf = TfidfVectorizer()
        self.cnt_vec = CountVectorizer()
        self.graph_sentence = []
        
    # TF-IDF Matrix 생성 후 Sentence Graph 도출
    def build_sent_graph(self, sentence):
        tfidf_mat = self.tfidf.fit_transform(sentence).toarray()
        self.graph_sentence = np.dot(tfidf_mat, tfidf_mat.T)
        return  self.graph_sentence
    
    # Matrix 생성 후 word graph와 {idx: word}형태의 dictionary 도출
    def build_words_graph(self, sentence):
        cnt_vec_mat = normalize(self.cnt_vec.fit_transform(sentence).toarray().astype(float), axis=0)
        vocab = self.cnt_vec.vocabulary_
        return np.dot(cnt_vec_mat.T, cnt_vec_mat), {vocab[word] : word for word in vocab}


# In[8]:


# Textrank 알고리즘 적용
class Rank(object):
    def get_ranks(self, graph, d=0.85): # d = damping factor
        A = graph
        matrix_size = A.shape[0]
        for id in range(matrix_size):
            A[id, id] = 0 # diagonal 부분을 0으로 
            link_sum = np.sum(A[:,id]) # A[:, id] = A[:][id]
            if link_sum != 0:
                A[:, id] /= link_sum
            A[:, id] *= -d
            A[id, id] = 1
            
        B = (1-d) * np.ones((matrix_size, 1))
        ranks = np.linalg.solve(A, B) # 연립방정식 Ax = b
        return {idx: r[0] for idx, r in enumerate(ranks)}


# In[9]:


# TextRank 클래스를 구현
class TextRank(object):
    def __init__(self, text):
        self.sent_tokenize = SentenceTokenizer()
        
        if text[:5] in ('http:', 'https'):
            self.sentences = self.sent_tokenize.url2sentences(text)
        else:
            self.sentences = self.sent_tokenize.text2sentences(text)
        
        self.nouns = self.sent_tokenize.get_nouns(self.sentences)
                    
        self.graph_matrix = GraphMatrix()
        self.sent_graph = self.graph_matrix.build_sent_graph(self.nouns)
        self.words_graph, self.idx2word = self.graph_matrix.build_words_graph(self.nouns)
        
        self.rank = Rank()
        self.sent_rank_idx = self.rank.get_ranks(self.sent_graph)
        self.sorted_sent_rank_idx = sorted(self.sent_rank_idx, key=lambda k: self.sent_rank_idx[k], reverse=True)
        
        self.word_rank_idx =  self.rank.get_ranks(self.words_graph)
        self.sorted_word_rank_idx = sorted(self.word_rank_idx, key=lambda k: self.word_rank_idx[k], reverse=True)
        
    # 문서 요약 구현 ( 1줄 )
    def summarize(self, sent_num=1):
        summary = []
        index=[]
        for idx in self.sorted_sent_rank_idx[:sent_num]:
            index.append(idx)
        
        index.sort()
        for idx in index:
            summary.append(self.sentences[idx])
        
        return summary
    
    # 키워드 출력 구현 ( 10개 )
    def keywords(self, word_num=10):
        rank = Rank()
        rank_idx = rank.get_ranks(self.words_graph)
        sorted_rank_idx = sorted(rank_idx, key=lambda k: rank_idx[k], reverse=True)
        
        keywords = []
        index=[]
        for idx in sorted_rank_idx[:word_num]:
            index.append(idx)
            
        #index.sort()
        for idx in index:
            keywords.append(self.idx2word[idx])
        
        return keywords


# In[10]:


# 결과값 리스트로 저장
def Textderivation(input):
    t = []
    a = []
    k = []
    b = df[ df['corp_nm'].str.contains(input) ]
    b.reset_index(drop=True, inplace=True)
    
    for i in [4]: # 위치 및 도출 개수 지정
        ti = b['title'][i]
        t.append(ti)
        text = str(b['content'][i])
        textrank = TextRank(text)
        row = textrank.summarize(1) # 기사 핵심 문장 아웃풋
        a.extend(row)
        rowk = textrank.keywords()
        k.extend(rowk)
    
    
    return t, a, k


# In[11]:


# Textderivation('영진실업') # 결과값 예시
print(Textderivation('현대모비스'))


# # 결과값 리스트로 저장
# def Textderivation(input):
#     a = []
#     b = df[ df['corp_nm'].str.contains(input) ]
#     b.reset_index(drop=True, inplace=True)
#     
#     for i in range(0, len(b)):
#         text = str(b['content'][i])
#         textrank = TextRank(text)
#         row = textrank.summarize(1) # 기사 핵심 문장 아웃풋
#         a.extend(row)
#     
#     return a

# Textderivation('삼성전자') # 결과값 예시

# In[ ]:




