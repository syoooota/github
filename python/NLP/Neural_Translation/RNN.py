import numpy as np
import tensorflow as tf


def bi_direct_lstm(input, fw_gatex,fw_gatey,fw_bias, bw_gatex,bw_gatey,
                   bw_bias):
    gomi,l = fw_gatey.get_shape()
    del gomi
    #[gatesuu, hidden1]
    fw_h = tf.zeros(l, dtype=tf.float32)
    bw_h = tf.zeros(l, dtype=tf.float32)
    fw_c = tf.zeros(l, dtype=tf.float32)
    bw_c = tf.zeros(l, dtype=tf.float32)
    del l
    batch,sentence_len,gm=input.get_shape()
    del gm
    foward_outputs = []
    back_outputs = []
    i = 0
    #flag=tf.reduce_sum(tf.reduce_sum(input,axis=-1),axis=0)
    #[sentence_len]
    input=tf.reshape(input,[batch,sentence_len,1,1,-1])
    def process(input_element):
        nonlocal i,fw_c,fw_h,bw_c,bw_h,sentence_len,batch
        
        gates = tf.reduce_sum(tf.multiply(input_element, fw_gatex),-1)+tf.multiply(fw_h, fw_gatey)+fw_bias
        gates=tf.reshape(gates,[4,batch,-1])
        gateh = tf.tanh(tf.unstack(gates[0]))
        gates= tf.sigmoid(tf.unstack(gates[1:]))
        fw_c = tf.multiply(tf.unstack(gates[0]),gateh)+tf.multiply(tf.unstack(gates[1]),fw_c)
        fw_h = tf.reshape(tf.multiply(tf.unstack(gates[2]),tf.tanh(fw_c)),[batch, 1, -1])
        foward_outputs.append(fw_h)
        i += 1
        if i<sentence_len:
         #   _=tf.cond(tf.equal(flag[i],0), lambda:0,lambda:process(input[:,i]))
            process(input[:,i])
        
        gates = tf.reduce_sum(tf.multiply(input_element, bw_gatex),-1)+tf.multiply(bw_h, bw_gatey)+bw_bias
        gates=tf.reshape(gates,[4,batch,-1])
        gateh = tf.tanh(tf.unstack(gates[0]))
        gates= tf.sigmoid(tf.unstack(gates[1:]))
        bw_c = tf.multiply(tf.unstack(gates[0]),gateh)+tf.multiply(tf.unstack(gates[1]),bw_c)
        bw_h = tf.reshape(tf.multiply(tf.unstack(gates[2]),tf.tanh(bw_c)),[batch, 1, -1])
        back_outputs.append(bw_h)
            
    process(input[:,0])
    return foward_outputs, back_outputs
       


def bi_direct_lstm_2l(fw_input,bw_input, fw_gatex,fw_gatey,fw_bias, bw_gatex,bw_gatey,
                      bw_bias):
    
    gomi,l = fw_gatey.get_shape()
    del gomi
    fw_h = tf.zeros(l, dtype=tf.float32)
    bw_h = tf.zeros(l, dtype=tf.float32)
    fw_c = tf.zeros(l, dtype=tf.float32)
    bw_c = tf.zeros(l, dtype=tf.float32)
    del l
    foward_outputs = []
    back_outputs = []
    batch,ks,gm=fw_input[0].get_shape()
    del ks,gm
    #for i,j in zip(fw_input, bw_input):
    for i in tf.unstack(fw_input):
        #fw:i
        i=tf.reshape(i,[batch,1,1,-1])
        gates = tf.reduce_sum(tf.multiply(i, fw_gatex), -1)+tf.multiply(fw_h, fw_gatey) + fw_bias
        gates=tf.reshape(gates,[4,batch,-1])
        gateh = tf.tanh(tf.unstack(gates[0]))
        gates= tf.sigmoid(tf.unstack(gates[1:]))
        fw_c = tf.multiply(tf.unstack(gates[0]),gateh)+tf.multiply(tf.unstack(gates[1]),fw_c)
        fw_h = tf.reshape(tf.multiply(tf.unstack(gates[2]),tf.tanh(fw_c)),[batch, 1, -1])
        foward_outputs.append(fw_h)
    for j in tf.unstack(bw_input):
        #bw:j
        j=tf.reshape(j,[batch,1,1,-1])
        gates = (tf.reduce_sum(tf.multiply(j, bw_gatex), -1) +tf.multiply(bw_h, bw_gatey)) + bw_bias
        gates=tf.reshape(gates,[4,batch,-1])
        gateh = tf.tanh(tf.unstack(gates[0]))
        gates= tf.sigmoid(tf.unstack(gates[1:]))
        bw_c = tf.multiply(tf.unstack(gates[0]),gateh)+tf.multiply(tf.unstack(gates[1]),bw_c)
        bw_h = tf.reshape(tf.multiply(tf.unstack(gates[2]),tf.tanh(bw_c)),[batch, 1, -1])
        back_outputs.append(bw_h)
    return foward_outputs, back_outputs

def lstm(input, gatex,gatey,bias,h0=None):
    if h0 == None:
        h = tf.zeros(len(input[0]), dtype=tf.float32)
    else:
        h = h0
    c = tf.zeros(len(input[0]), dtype=tf.float32)
    outputs = []
    for i in input:
        gates = (tf.reduce_sum(tf.multiply(i, gatex), -1) +
                 tf.reduce_sum(tf.multiply(h, gatey), -1)) + bias
        # gates(hidden, input, forgotten, output)
        gates[0] = tf.tanh(gates[0])
        gates[1:] = tf.sigmoid(gates[:1])
        c = tf.multiply(gates[1], gates[0]) + tf.multiply(gates[2], c)
        h = tf.multiply(gates[3], tf.tanh(c))

        outputs.append(h)

    return outputs


