
from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus('/home/admin/python_work/自然言語処理/Neural_Translation/trans_data/train.ja')

model = word2vec.Word2Vec(sentences, sg=1,size=1000, min_count=0, window=2)
model.save("./word2vec/jp/skipgram.jp")