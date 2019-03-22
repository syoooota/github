# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import glob, pickle, random

def weight_init(shape):
    w = tf.random_normal(shape, stddev=1.0)
    return (w-0.5)*2

batch = 1000
f = open('Neural_Translation/trans_data/vocab.jp', 'rb')
vocab_jp = pickle.load(f)
f.close()
goi_num = len(vocab_jp)
x_reduc=256
x=tf.placeholder(tf.float32,[None,goi_num])
y = tf.placeholder(tf.float32,[None,goi_num])

w1 = tf.Variable(weight_init([goi_num,x_reduc]), name='E1')
w2 = tf.Variable(weight_init([x_reduc,goi_num]))
hidden1=tf.matmul(x,w1)
output = tf.matmul(hidden1,w2)


loss=tf.losses.softmax_cross_entropy(logits=output,onehot_labels=y)/batch

train_step = tf.train.AdamOptimizer().minimize(loss)


with tf.Session() as sess:
    #windowサイズ
    C = 1
    #fig = plt.figure(figsize=(10, 6))
    #X, Y = [], []
    sess.run(tf.global_variables_initializer())
    saver = tf.train.Saver({'skipgram':w1})
    
    0
    ite = 10
    train = []
    teach = []


    f = open('/home/admin/python_work/自然言語処理/Neural_Translation/trans_data/train.ja')
    L = len(f.readlines())
    while ite:
        for i in range(0, L, batch):
            li=[]
            li2=[]
    
            f=open ('/home/admin/python_work/自然言語処理/Neural_Translation/trans_data/train.ja')
            train = f.readlines()[i:i+batch]
            f.close()
            train = [i.split()for i in train]

            for ind1,ele1 in enumerate(train):        
                for ind2,ele2 in enumerate(ele1):                   
                    if (ind2-C) < 0 or ind2+C >= len(ele1):
                        continue
                    else:
                        one_train = np.zeros((goi_num))
                        one_teach = np.zeros((goi_num))

                        one_train[vocab_jp.index(ele2)] = 1.0
                        for cind in range(C):
                            one_teach[vocab_jp.index(ele1[ind2-cind])] = 1.0
                            one_teach[vocab_jp.index(ele1[ind2+cind])] = 1.0

                        li.append(one_train)
                        li2.append(one_teach)
            

            
            li2 = np.reshape(np.vstack((np.array(li2))), (-1,goi_num))
            del train
            _, loss_train = sess.run([train_step, loss], feed_dict={x: np.vstack((np.array(li))),
                                                                    y: li2
                                                                    })

            print(ite, loss_train)
            #saver.save(sess, "word2vec/jp/skipgram.jp")

        ite -=1
        saver.save(sess, "word2vec/jp/256/skipgram.jp")
        #plt.savefig('/home/admin/画像/skipgram.jpg')


