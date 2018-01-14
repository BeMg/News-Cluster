import sqlite3
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import jieba
import requests
import bs4
import re
import os
from random import sample


jieba.load_userdict("./data/dict.txt")
with open('./data/vec.obj', 'rb') as f:
    vec = pickle.load(f)

def getSoup(url):
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.text, 'lxml')
    return s

def get_content(url):
    try:
        title = ''
        text = ''
        if 'ettoday' in url:
            s = getSoup(url)
            title = s.find(class_=re.compile("title|title_article")).text
            ss = s.find(class_=re.compile("part_area_1|story"))
            sss = ss.findAll('p')
            for i in sss:
                text += i.text
                text += "\n\n"
            return (url, title, text)
        elif 'appledaily' in url:
            s = getSoup(url)
            title = s.find(class_="ndArticle_leftColumn").find('h1').text
            text = s.find(class_="ndArticle_margin").find('p').text
            return (url, title, text)
        elif 'udn' in url:
            s = getSoup(url)
            title = s.find(class_='story_art_title').text
            title = title.replace('\n', '')
            text = ''
            ss = s.find(id='story_body_content').findAll('p')
            for i in ss:
                text += i.text
            return (url, title, text)
        elif 'ltn' in url:
            s = getSoup(url)
            title = s.find(class_='whitecon articlebody').find('h1').text
            title = title.replace('\n', '')
            text = ''
            ss = s.find(class_='text').findAll('p')
            for i in ss:
                text += i.text
            return (url, title, text)
        else:
            return None
    except:
        return None

def preprocess(text, n_cluster):
    with open('./data/Kmeans_{}_obj.pickle'.format(n_cluster), 'rb') as f:
        kmean = pickle.load(f)
    seg = jieba.cut(text, cut_all=True)
    cluster = kmean.predict(vec.transform((" ".join(seg), )).toarray())[0]
    return cluster

def get_by_cluster(n_cluster, cluster, number):
    conn = sqlite3.connect('./data/news{}.db'.format(n_cluster))
    c = conn.cursor()
    c.execute('SELECT * FROM news WHERE cluster = "%s"' % cluster)
    data = c.fetchall()
    sdata = sample(data, number)
    return sdata