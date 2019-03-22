import numpy as np
import glob,pickle
from matplotlib import pyplot as plt


def del_muimi2(muimi,msHz,wind,div,start):
    num=msHz*muimi
    intnum = int((num-div)/(wind-div))
    amari = num%(wind-div)    
    if amari+div > wind/2:
        intnum += 1
    
    a=muimi-start
    num=msHz*a
    intnum2 = int((num-amari)/(wind-div))
    num = num%(wind-div)
    if num+div > wind/2:
        intnum2 += 1
    return intnum,intnum2

def del_muimi(muimi,msHz,wind,div):
    num=msHz*muimi
    intnum = int((num-div)/(wind-div))
    num = num%(wind-div)
    if num+div > wind/2:
        intnum += 1
    return intnum

path = 'datasets'
def learn():
    import tensorflow as tf
    import random
    batch = 5000
    xlen = 12
    f = open('phones.txt', 'rb')
    phones = pickle.load(f)
    f.close()    
    phoneslen = len(phones)
    x=tf.placeholder(tf.float32,[batch,xlen])/100
    y = tf.placeholder(tf.float32,[batch,phoneslen])
    flag = tf.placeholder(tf.float32,[batch,1])
    condition = tf.placeholder_with_default(False,shape=())
    
    hidden1=tf.layers.dense(x, 2048, activation=tf.nn.sigmoid)
    #hidden1=tf.contrib.layers.maxout(tf.layers.dense(x, 2048),1024)
    print('h1',hidden1.shape)
    #hidden2 = tf.layers.dense(hidden1, 2048, activation=tf.nn.sigmoid)
    hidden2=tf.contrib.layers.maxout(tf.layers.dense(hidden1, 2024),1012)
    hidden2_drop = tf.layers.dropout(hidden2)
    #hidden3 = tf.layers.dense(hidden2_drop, 3048, activation=tf.nn.sigmoid)
    hidden3=tf.contrib.layers.maxout(tf.layers.dense(hidden2_drop, 2024),1012)
    hidden3_drop = tf.layers.dropout(hidden3,rate=0.3)
    #hidden4 = tf.layers.dense(hidden3_drop, 2048, activation=tf.nn.sigmoid)
    hidden4=tf.contrib.layers.maxout(tf.layers.dense(hidden3_drop, 2048),1024)
    #hidden4_drop = tf.layers.dropout(hidden4,rate=0.1)
    #hidden5=tf.layers.dense(hidden4, 2048, activation=tf.nn.sigmoid)
    #hidden5=tf.layers.dense(hidden4_drop, 2048, activation=tf.nn.sigmoid)
    #hidden5_drop = tf.layers.dropout(hidden5,rate=0.2)
    #hidden6=tf.layers.dense(hidden5, 2048, activation=tf.nn.sigmoid)
    #hidden6_drop = tf.layers.dropout(hidden6,rate=0.1)    
    output = tf.layers.dense(hidden4, phoneslen)
    print('out',output.shape)
    out_ = tf.cond(condition,lambda:output,lambda:flag*output)
    loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=out_,labels=y)
    
    print('loss',loss.shape)
    loss_ = tf.reduce_mean(loss,axis=0)
    train_step = tf.train.AdamOptimizer().minimize(loss_)
    
    with tf.Session() as sess:
        addr = glob.glob(path + '/teach_train*')

        fig = plt.figure(figsize=(10, 6))
        X, Y = [], []
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        #saver.restore(sess, "./学習後変数/acoustic/acous")
        ite = 30
        train=np.zeros((batch,xlen))
        teach=np.zeros((batch,phoneslen))        
        count = 0
        Flag = np.zeros((batch,1))
        random.shuffle(addr)
        loss_train = 0
        while ite:
            
            for i in addr:
                #f = open(i, 'rb')
                data = np.load(i)
                
                #print(data.shape)
                #(2219, 3, 1)
                #print('count',count)
                for j in data:
                    tr = j[-1,0]
                    te = j[1]
                    
                    for i in tr:
                        teach[count,te[0][0][0]] += 1                    
                        train[count] = i
                        count += 1
                        #print(train)
                        #print(teach)
                        if count == batch:
                            
                            _,loss_train,o,t= sess.run([train_step,loss_,out_,y],feed_dict={x:train,
                                                                                y:teach,flag:Flag,condition:True})
                            count = 0
                            #print(o)
                            #print(t)
                            

                            teach=np.zeros((batch,phoneslen))
                            train=np.zeros((batch,xlen))
                    
                
                print('ite', ite, 'loss=', loss_train)
                '''
                plt.clf()
                X.append(len(Y)*1)
                Y.append(np.log(loss_train))                
                plt.plot(X, Y)
                plt.title("loss function")
                plt.ylim(0, 2)
                plt.xlim(0, len(addr)*ite)
                plt.draw()
                plt.pause(0.01)  
                '''
            
            #train = np.array(train)
            
            Flag[:batch-count] += 1.0
            _,loss_train= sess.run([train_step,loss],feed_dict={x:train,
                                                                y:teach,flag:Flag,condition:False})
            count = 0
            train=np.zeros((batch,xlen))
            teach=np.zeros((batch,phoneslen))
            Flag = np.zeros((batch,1))
                
            saver.save(sess, "./学習後変数/acoustic/acous")
            print('ite', ite, 'loss=', loss_train)
            ite -= 1
    

    plt.savefig('/home/admin/画像/Acous.jpg')
    

def Estim():
    import tensorflow as tf
    import random
    batch = 5000
    xlen = 12
    f = open('phones.txt', 'rb')
    phones = pickle.load(f)
    f.close()    
    phoneslen = len(phones)
    x=tf.placeholder(tf.float32,[batch,xlen])/100
    y = tf.placeholder(tf.float32,[batch,phoneslen])
    flag = tf.placeholder(tf.float32,[batch,1])
    condition = tf.placeholder_with_default(False,shape=())
    
    hidden1=tf.layers.dense(x, 2048, activation=tf.nn.sigmoid)
    #hidden1=tf.contrib.layers.maxout(tf.layers.dense(x, 2048),1024)
    print('h1',hidden1.shape)
    #hidden2 = tf.layers.dense(hidden1, 2048, activation=tf.nn.sigmoid)
    hidden2=tf.contrib.layers.maxout(tf.layers.dense(hidden1, 2024),1012)
    hidden2_drop = tf.layers.dropout(hidden2)
    #hidden3 = tf.layers.dense(hidden2_drop, 3048, activation=tf.nn.sigmoid)
    hidden3=tf.contrib.layers.maxout(tf.layers.dense(hidden2_drop, 2024),1012)
    hidden3_drop = tf.layers.dropout(hidden3,rate=0.3)
    #hidden4 = tf.layers.dense(hidden3_drop, 2048, activation=tf.nn.sigmoid)
    hidden4=tf.contrib.layers.maxout(tf.layers.dense(hidden3_drop, 2048),1024)
    #hidden4_drop = tf.layers.dropout(hidden4,rate=0.1)
    #hidden5=tf.layers.dense(hidden4, 2048, activation=tf.nn.sigmoid)
    #hidden5=tf.layers.dense(hidden4_drop, 2048, activation=tf.nn.sigmoid)
    #hidden5_drop = tf.layers.dropout(hidden5,rate=0.2)
    #hidden6=tf.layers.dense(hidden5, 2048, activation=tf.nn.sigmoid)
    #hidden6_drop = tf.layers.dropout(hidden6,rate=0.1)    
    output = tf.layers.dense(hidden4, phoneslen)
    print('out',output.shape)
    out_ = tf.cond(condition,lambda:output,lambda:flag*output)
    loss = tf.nn.softmax_cross_entropy_with_logits_v2(logits=out_,labels=y)
    
    print('loss',loss.shape)
    loss_ = tf.reduce_mean(loss,axis=0)
    train_step = tf.train.AdamOptimizer().minimize(loss_)
    
    with tf.Session() as sess:
        addr = glob.glob(path + '/teach_train*')

        fig = plt.figure(figsize=(10, 6))
        X, Y = [], []
        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        #saver.restore(sess, "./学習後変数/acoustic/acous")
        ite = 30
        train=np.zeros((batch,xlen))
        teach=np.zeros((batch,phoneslen))        
        count = 0
        Flag = np.zeros((batch,1))
        random.shuffle(addr)
        loss_train = 0
if __name__ == "__main__":
    #learn()