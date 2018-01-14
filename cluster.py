import sqlite3
import json
import pickle
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import MiniBatchKMeans
import numpy as np

def newsInsert(data, db):
    conn = sqlite3.connect("./data/"+db)
    c = conn.cursor()
    c.executemany("INSERT INTO news VALUES (?,?,?)", data)
    conn.commit()
    conn.close()

conn = sqlite3.connect("./data/news.db")
c = conn.cursor()
c.execute("SELECT * FROM news")
srcdata = c.fetchall()

length = len(srcdata)
jieba.load_userdict("./data/dict.txt")

with open("./data/vec.obj", "rb") as f:
    vec = pickle.load(f)

for i in range(10):
    filename = "Kmeans_{}_obj.pickle".format(i+5)
    with open("./data/"+filename, "rb") as f:
        kmean = pickle.load(f)
    cnt = 0
    dstdata = []
    for url, title, txt in srcdata:
        cnt += 1
        print("{}:{}/{}".format(i, cnt, length))
        seg = jieba.cut(txt, cut_all=True)
        cluster = kmean.predict(vec.transform((" ".join(seg), )).toarray())[0]
        dstdata.append((url, title, str(cluster)))
        if cnt%10000 == 0:
            newsInsert(dstdata, "news{}.db".format(i+5))
            dstdata = []   
    
    if len(dstdata) > 0:
        newsInsert(dstdata, "news{}.db".format(i+5))
        
