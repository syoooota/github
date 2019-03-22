# -*- coding: utf-8 -*-

import numpy as np
import glob, wave, MeCab, pickle, re
from sklearn.feature_extraction.text import TfidfVectorizer


def word_counter(text):
    count = {}
    m = MeCab.Tagger("-Ochasen")
    for i in text:
        m_text = m.parseToNode(i)
        
        while m_text:
            hinsi = m_text.feature.split(',')[0]
            if hinsi in ['名詞']:
                word = m_text.surface
                if word in count.keys():
                    count[word] +=1
                else:
                    count[word] = 1
            m_text = m_text.next        
    
    return count
    
def filter_manuscript(script):
    script =  script.replace('\n', '')
    
    # 英文を取り除く（日本語の中の英字はそのまま）
    script = re.sub(r'[a-zA-Z0-9]+[ \,\.\':;\-\+?!]', '', script)
    # 記号や数字は「、」に変換する。
    # (単純に消してしまうと意味不明な長文になりjanomeがエラーを起こす)
    
    script = re.sub(
        r'[!"“#$%&()\*\+\-\.,\/:;<=>?@\[\\\]^_`{|}~]+', '、', script)
    script = re.sub(r'[（金）（土）（日）（月）（火）（水）（木）]', '、', script)
    script = re.sub(r'[0-9]+', '、', script)
    script = re.sub(r'[（）【】『』｛｝「」［］《》〈〉]', '、', script)

    return script


name = glob.glob('yahoo_news/*')
text=[]
list1=[]
a = name[5][11:][:-4]

for i in name:
    f=open(i,'rb')
    text=pickle.load(f)
    f.close()
    
    text = str(text)

    script = filter_manuscript(text)
    
    
    words = word_counter(script.split('、'))
    dic = words.copy()
    for k,v in words.items():
        
        if (v < 20) or (v > 200):
            del(dic[k])
        
    words = dic
    del dic
    list1.append(words)
"""
f=open(a+'_bunkai.txt','wb')
pickle.dump(words,f)
f.close()
"""
'''
name = glob.glob('bunkai/*')
lxt=[]
for i in name:
    f=open(i,'rb')
    list1.append(pickle.load(f))
f.close()
'''
print(list1[0])
list3=[]
for i in list1:
    list2=[]
    for k,v in i.items():

        list2.append((k+' ')*v)
    list3.append(' '.join(list2))



vectorizer = TfidfVectorizer(stop_words=['english','ん' ,'たち','上','氏','１' ], token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(list3).toarray()
features = vectorizer.get_feature_names()
#vecs=np.sort(vecs, axis=1)[:,::-1]




list1 = []
print(vecs.shape)

for i in vecs:
    dict={}
    for k,v in zip(features,i):
        dict[k] = v
       
    list1.append(sorted(dict.items(), key=lambda x:-x[1])[:10])

learn = np.array(list1)
#print(learn)
np.save('learn',learn)
