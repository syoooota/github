# -*- coding: utf-8 -*-

import numpy as np
import glob, pickle, RNN
import tensorflow as tf
from scipy.stats import norm
from gensim.models import word2vec


def weight_init(shape):
    w = tf.random_normal(shape, stddev=1.0)
    return tf.Variable((w-0.5)*2)

def bias_init(shape):
    b = tf.random_normal(shape, stddev=1.0)
    return tf.Variable(b)

def gate_weight_init(sizex,sizey):
    dec_wx = weight_init([sizex,sizey])
    dec_wy = weight_init([sizex])
    dec_ix = weight_init([sizex,sizey])
    dec_iy = weight_init([sizex])
    dec_fx = weight_init([sizex,sizey])
    dec_fy = weight_init([sizex])
    dec_ox = weight_init([sizex,sizey])
    dec_oy = weight_init([sizex])
    
    gatex = tf.stack([dec_wx, dec_ix,dec_fx,dec_ox])
    gatey = tf.stack([dec_wy, dec_iy,dec_fy,dec_oy])
    
    bx = bias_init([sizex])
    bi = bias_init([sizex])
    bf = bias_init([sizex])
    bo = bias_init([sizex])
    gateb = tf.stack([bx,bi,bf,bo])
    return gatex, gatey, gateb

def one_lstm(batch,dec_inp,dec_wx1,dec_wy1,dec_b1,z,c):
    #dec_inp = tf.convert_to_tensor(dec_inp, dtype=tf.float32)
    dec_inp=tf.reshape(dec_inp,[batch,1,1,-1])
    z=tf.reshape(z,[batch,1,-1])
    
    gates = tf.reduce_sum(tf.multiply(dec_inp, dec_wx1), axis=-1)+tf.multiply(z, dec_wy1) + dec_b1
    gates=tf.reshape(gates,[4,batch,-1])
    gateh = tf.tanh(tf.unstack(gates[0]))
    gates = tf.sigmoid(tf.unstack(gates[1:]))
    c = tf.multiply(tf.unstack(gates[0]), gateh) + tf.multiply(tf.unstack(gates[1]), c)
    h = tf.multiply(tf.unstack(gates[2]), tf.tanh(c))
    return h,c

'''
failed
def blackout(batch,output):
    D = np.random.rand(5000)
    blackout = 0
    output=tf.reshape(output,[batch,-1])
    for y in tf.unstack(output):
        #tf.cond(y==D,lambda:)
        #if [D==y].any() :
            #D[D==y] += 1e-5
        qdy = norm.pdf(loc=0.5, scale=1, x=D)
        sdy = np.exp(D)
        qy = np.sum(norm.pdf(loc=0.5, scale=1, x=y))
        sy=np.exp(y)
        py = (sy/qy) / ((sy/qy)+(np.sum(sdy/qdy)))
        blackout +=-np.log(py) - np.log(1 - py)
    return blackout
'''

   

tf.reset_default_graph()
batch = 1
max_sentence_len = 100
y_max_sentence_len = 130
f = open('trans_data/vocab.en', 'rb')
vocab_en = pickle.load(f)
f = open('trans_data/vocab.jp', 'rb')
vocab_jp = pickle.load(f)
f.close()
#print(len(vocab_en),len(vocab_jp))
goi_num=len(vocab_jp)
teach_num=len(vocab_en)

x_reduc=256
y_reduc = 100
hidden1=100
hidden2=100

E1=tf.Variable(weight_init([goi_num,x_reduc]),name='E1',trainable=False)
with tf.Session() as sess:
    saver = tf.train.Saver({'skipgram':E1})
    saver.restore(sess, "../word2vec/jp/256/skipgram.jp")

#符号化器(encoder)
input = tf.placeholder(shape=[batch,max_sentence_len,goi_num,1],dtype=tf.float16)
teach = tf.placeholder(shape=[y_max_sentence_len+2,teach_num+2,batch],dtype=tf.float16)
flag = tf.placeholder(tf.int32,[batch,2])
bflag = tf.placeholder(tf.int32,[batch,2])
del_zero = tf.placeholder(tf.float32,[max_sentence_len,batch,1,1])
y_del_zero = tf.placeholder(tf.float32,[batch,y_max_sentence_len+2,1])
#E1 = word2vec.Word2Vec.load("../word2vec/jp/skipgram.jp")#(goinum,1000)


fw_wx1,fw_wy1,fw_b1 = gate_weight_init(hidden1,x_reduc)
fw_wx2,fw_wy2,fw_b2 = gate_weight_init(hidden2,hidden1)
bw_wx1,bw_wy1,bw_b1 = gate_weight_init(hidden1,x_reduc)
bw_wx2,bw_wy2,bw_b2 = gate_weight_init(hidden2,hidden1)

dec_wx1,dec_wy1,dec_b1 = gate_weight_init(hidden1,y_reduc+hidden2)
dec_wx2,dec_wy2,dec_b2 = gate_weight_init(hidden2,hidden1)

att_wa1 = tf.Variable(weight_init([hidden2,hidden2]))
att_wa2 = tf.Variable(weight_init([hidden2*2,hidden2]))
att_wo = tf.Variable(weight_init([(teach_num+2),hidden2]))
E1=tf.cast(E1,dtype=tf.float16)
in_opp=tf.reduce_sum(tf.multiply(input,E1), axis=-2)
in_opp=tf.cast(tf.reshape(in_opp,[batch,max_sentence_len,x_reduc]),dtype=tf.float32) 

del E1

fwout1,bwout1=RNN.bi_direct_lstm(in_opp, fw_wx1, fw_wy1, fw_b1,
                                 bw_wx1, bw_wy1, bw_b1)
fwout1=tf.multiply(tf.convert_to_tensor(fwout1),del_zero)
#fwout1 shape=(100, 2, 1, 10)
fw_h1=tf.gather_nd(fwout1,flag)

bwout1=tf.multiply(tf.convert_to_tensor(bwout1),del_zero[::-1])
bw_h1=tf.gather_nd(bwout1,bflag)

fwout2,bwout2 = RNN.bi_direct_lstm_2l(fwout1, bwout1, fw_wx2,fw_wy2,fw_b2,
                                      bw_wx2, bw_wy2, bw_b2)
#[senten, hidden2]
fwout2=tf.multiply(tf.convert_to_tensor(fwout2),del_zero)
#fwout1 shape=(100, 2, 1, 10)
fw_h2=tf.gather_nd(fwout2,flag)

bwout2=tf.multiply(tf.convert_to_tensor(bwout2),del_zero[::-1])
bw_h2=tf.gather_nd(bwout2,bflag)



#復号化器(decoder)
Hs=tf.convert_to_tensor(fwout2, dtype=tf.float32)+tf.convert_to_tensor(bwout2, dtype=tf.float32)
Hs=tf.reshape(Hs,[-1,batch,hidden2])
h1 = fw_h1+bw_h1
h = fw_h2+bw_h2
del fwout1,fwout2,bwout1,bwout2

E2 = np.reshape(np.arange(1,(teach_num+2)*y_reduc+1), (y_reduc,(teach_num+2),1))*1e-5
E2 = tf.convert_to_tensor(E2,dtype=tf.float16)
c1 = 0
c2 = 0
loss = []
patch = tf.zeros((hidden2,batch), dtype=tf.float32)
for t in tf.unstack(teach):
    y=tf.reduce_sum(tf.multiply(t,E2),axis=1)
    y=tf.cast(y,dtype=tf.float32)
    #y.shape(300,20)
    dec_inp=tf.concat((patch,y),axis=0)
    
    h1,c1 = one_lstm(batch,dec_inp,dec_wx1,dec_wy1,dec_b1, h1,c1)
    h,c2 = one_lstm(batch,h1,dec_wx2,dec_wy2,dec_b2, h,c2)
    a = tf.nn.softmax(tf.reduce_sum(tf.multiply(tf.reduce_sum(tf.multiply(att_wa1,tf.reshape(h,[batch,1,-1])),axis=-1), Hs),axis=-1))
    a = tf.reduce_sum(tf.multiply(Hs,tf.reshape(a,[-1,batch,1])),axis=0)
    c_dash = tf.reshape(tf.concat([a,tf.reshape(h,[batch,-1])],axis=-1),[batch,-1,1])
    patch=tf.tanh(tf.reduce_sum(tf.multiply(att_wa2,c_dash),axis=1))
    patch=tf.reshape(patch,[-1,batch])
    att_wo=tf.reshape(att_wo,[-1,hidden2,1])
    output = tf.reduce_sum(tf.multiply(att_wo,patch),axis=1)
    #loss += blackout(batch,output) failed
    loss.append(output)

del E2
loss= tf.multiply(tf.transpose(tf.convert_to_tensor(loss),[2,0,1]), y_del_zero)
#[batch,y_max_sentence_len+2,teach_num+2]
tra_teach=tf.transpose(teach,[2,0,1])
allloss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=loss,labels=tra_teach)/(teach_num+2),axis=0)
train_step = tf.train.AdamOptimizer().minimize(allloss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
   
    saver = tf.train.Saver()
    ite=3
    
    f=open('trans_data/train.ja')
    L = len(f.readlines()[:100000])
    f.close()
    while ite:
        for i in range(0, L, batch):
            xlist=[]
            yFlag=[]
            Flag=[]
            zer=np.zeros([max_sentence_len,batch])
            yzer=np.zeros([batch,y_max_sentence_len+2,1])
            f=open('trans_data/train.ja')
            train = f.readlines()[i:i+batch]
            f.close()
            train = [i.split()for i in train]
            f=open('trans_data/train.en')
            tea = f.readlines()[i:i+batch]
            f.close()
            tea = [i.split()for i in tea]

            one_train = np.zeros((batch, max_sentence_len, goi_num,1))              
            for batch_num,ele1 in enumerate(train):
                for sen_ind,ele2 in enumerate(ele1):
                    one_train[batch_num, sen_ind, vocab_jp.index(ele2),0] = 1.0
                    ##xlist.append([batch_num, sen_ind, vocab_jp.index(ele2),0])
                Flag.append([sen_ind,batch_num])
                zer[:sen_ind+1,batch_num]=np.ones(sen_ind+1)
            zer=np.reshape(zer,(max_sentence_len,batch,1,1))

            one_teach = np.zeros((y_max_sentence_len, teach_num,batch))            
            for batch_num,ele1 in enumerate(tea):
                for sen_ind,ele2 in enumerate(ele1):
                    one_teach[sen_ind, vocab_en.index(ele2),batch_num] = 1.0
                yFlag.append([[sen_ind+2],[teach_num+1],[batch_num]])
                yzer[batch_num,:sen_ind+3,0]=np.ones(sen_ind+3)          
            
            del train,tea
            bFlag = np.array(Flag)
            for k in range(batch):
                bFlag[k,0] = -1*bFlag[k,0]+(y_max_sentence_len-1)            
            #pad = np.zeros((y_max_sentence_len+2, teach_num+2,batch))
            one_teach = np.pad(one_teach,[(1,1),(1,1),(0,0)], 'constant')
            #yzer = np.pad(yzer,[(0,0),(1,1),(0,0)], 'constant')
            
            #[batch,y_max_sentence_len]
            one_teach[0,0,:] = one_teach[0,0,:] + 1.0
            ##one_teach[-1,-1,:] = one_teach[-1,-1,:] + 1.0
            for j in yFlag:
                one_teach[j] = one_teach[j] + 1.0
            del yFlag
            #(y_max_sentence_len, teach_num,batch)

            _, loss_train= sess.run([train_step,allloss,],feed_dict={input:one_train,
                                                                 teach:one_teach,flag:Flag,
                                                                 del_zero:zer,bflag:bFlag,
                                                                 y_del_zero:yzer})
            print(ite,np.sum(loss_train)/batch)
        saver.save(sess, "variable/Jp_to_En/")
        ite -=1

