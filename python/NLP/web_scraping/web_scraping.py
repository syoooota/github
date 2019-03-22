# -*- coding: utf-8 -*-

#import numpy as np
import glob,  MeCab, pickle
import urllib.request, urllib.error
from bs4 import BeautifulSoup as bs
import sys
sys.setrecursionlimit(10000)

#スクレイピング
"""
url = 'https://headlines.yahoo.co.jp/rss/list'
html = urllib.request.urlopen(url)
soup = bs(html, "html.parser")

news = soup.select("#ynCopyright h4")

links = soup.find_all("ul", class_="ymuiList clearFix yjSt")

#print(news)
list1 = []
list2 = []
for i,k in zip(links, news):
    list2.append(k.getText())
    for j in i.find_all('a'):
        list1.append(j.get('href'))
    list2.append(list1)
"""
"""
f=open('a.txt','rb')
#pickle.dump(list2,f)
list2=pickle.load(f)
f.close()

list1=[]
test=[]
for i in range(0,len(list2),2):
    k,j=list2[i], list2[i+1]
    l=j[:30]
    j=j[30:]
    list1.append([k,l])
    test.append([k,j])
    #print('{} : {}'.format(i))

f=open('test.txt','wb')
pickle.dump(test,f)
f=open('b.txt','wb')
pickle.dump(list1,f)
f.close()
"""
f=open('b.txt','rb')
list1=pickle.load(f)
f.close()
#print(len(list1[0][1]))


list2 = []
list3 = []
for i in list1:
    name,url=i

    for k in url:
        xml = urllib.request.urlopen(k)
        soup = bs(xml, "lxml")
        item = soup.find_all('item')
        for j in item:
            title=j.title.string
            url2 = j.find_all('link')[0].getText()
            if url2 == '':
                a = str(j).split('\n')
                for tmp in a:
                    if '<link/>' in tmp:
                        url2=tmp[7:]
                        break
        
            list2.append(title)
            html = urllib.request.urlopen(url2)
            soup2 = bs(html, "html.parser")
            for tmp in soup2.find_all('p'):
                list3.append(tmp.getText())
            list2.append(list3)
            list3 = []
    f=open('yahoo_news/'+name+'.txt','wb')
    pickle.dump(list2,f)
    f.close()
    list2 = []            

'''
