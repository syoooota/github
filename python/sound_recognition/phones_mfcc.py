# -*- coding: utf-8 -*-

import numpy as np
from pydub import AudioSegment
import glob, scipy.fftpack.realtransforms
import sklearn.mixture, os, os.path, pickle




class GMM:
    #np.seterr(all="raise")
    def __init__(self, K, X):
        self.K = K
        self.X=X

    def scale(self,X):
        """データ行列Xを属性ごとに標準化したデータを返す"""
        # 属性ごとに平均値と標準偏差を計算
        mu = np.reshape(np.mean(X, axis=1),(-1,1))
        sigma = np.reshape(np.std(X, axis=1),(-1,1))

        # 属性ごとデータを標準化
        X = (X - mu) / sigma

        return X
    def ZeroOneNorm(self,X):
        return (X-X.min()) / (X.max()-X.min())

    def gaussian(self,x, mu, sigma,m):
        """多変量ガウス関数"""
        x = np.reshape(x,(-1, 1,1, m))
        # (N,1,1,m)
        mu = np.reshape(mu, (1, -1, 1,m))
        #(1,K,1,1)
        a =x-mu
        #exp 709～-745.0 8.218407e+307:4.940656e-324
        #(N,K,1,m)
        temp1 = 1 / ((2 * np.pi) ** (m / 2.0))
        temp2 = 1 / ((np.linalg.det(sigma) ** 0.5)+(1e-100))
        #temp2 = (np.ndarray.astype((1 / (np.linalg.det(sigma) ** 0.5))*1000, np.int))/1000.0
        l1,l2,l3,l4=a.shape
        #print (np.linalg.inv(sigma)[0])
        cpsigma = np.zeros((self.K, m, m))
        for i in range(self.K):
            cpsigma[i] = np.eye(m)
        arr = np.sum(np.reshape(a,(l1,l2,l4,l3))*np.linalg.solve(sigma,cpsigma),-2)
        del cpsigma
        #arr = np.sum(np.reshape(a, (l1, l2, l4, l3)) * np.array(li), -2)
        temp3 = -0.5*np.sum(arr*np.reshape (a,(l1,l2,l4)), -1)
        temp3[temp3 < -700] = -700
        temp3[temp3 > 700] = 700
        #(N,K) = (N,K,1,m)*(1,K,m,m)*(N,m,1)
        temp2 = np.reshape(temp1*temp2,(1,-1))
        return temp2 * np.exp(temp3)

    def main(self):

        N, m = self.X.shape
        self.X = self.scale(self.X)
        #self.X = self.ZeroOneNorm(self.X)
        #mu = (np.random.rand(self.K, m)-0.5)/100
        mu = np.random.rand(self.K, m)
        #mu = np.sum(self.X, axis=0)/N
        pi = np.random.rand(self.K)
        sigma = np.zeros((self.K, m, m))
        for i in range(self.K):
            sigma[i] = np.eye(m)


        # 対数尤度の初期値を計算
        gauss = self.gaussian(self.X, mu, sigma, m)
        # (N,K)
        temp = np.sum(pi * gauss, axis=1)
        # (N)
        # 対数尤度
        like = np.sum(np.log(temp), axis=0)

        diff = 1
        while (diff > 0.01):
            X = np.reshape(self.X, (N, 1, m))
            # E-step : 現在のパラメータを使って、負担率を計算
            gauss = self.gaussian(X, mu, sigma, m)
            temp = np.reshape(np.sum(pi * gauss, axis=-1), (-1, 1))
            temp2 = pi * gauss
            # 各Kの負担率
            gamma = temp2 / temp
            # (N,K)

            # M-step : 現在の負担率を使って、パラメータを再計算
            Nk = np.reshape(np.sum(gamma, axis=0), (-1, 1))
            mu = np.sum(np.reshape(gamma,(N, self.K, 1)) * X, axis=0) / Nk
            #mu /= 2
            # (K,m)

            temp3 = X - mu
            # (N,K,m)
            temp3 = np.reshape(temp3, (N, self.K, m, 1)) * np.reshape(temp3, (N, self.K, 1, m))
            sigma = np.sum(np.reshape(gamma, (N, self.K, 1, 1)) * temp3, axis=0) \
                    / np.reshape(Nk, (self.K, 1, 1))
            #sigma[np.isnan(sigma)] = 0
            #sigma /= 2
            pi = np.reshape(Nk / N, (-1))
            # 対数尤度の計算
            gauss = self.gaussian(X, mu, sigma, m)

            temp = np.sum(pi * gauss, axis=-1)
            new_like = np.sum(np.log(temp+(1e-10)))
            print ('like', new_like)
            diff = np.sqrt((like - new_like) ** 2)
            print ('diff',diff)
            like = new_like
        return pi * gauss




def transmel(f):
    return 1127.01048 * np.log(f / 700.0 + 1.0)

def transhelz(m):
    return 700.0 * (np.exp(m / 1127.01048) - 1.0)

#間違ってるっぽい(failed)
def dct(x):
    n = len(x[0])
    top = np.ones(n)/np.sqrt(2)
    vertical = np.array([np.cos(((2*i+1)/2*n)*np.pi) for i in range(n)])
    side = np.reshape(np.arange(1, n), (-1,1))
    arr = np.vstack((top, side*vertical))
    arr = np.sqrt(2/n)*arr
    return np.sum(arr*np.reshape(x, (-1, 1, n)), axis=-1)


def calc_mfcc(s):
    downrate = 16000
    '''
    #wav
    numch = wav.getnchannels()
    samplewidth = wav.getsampwidth()   
    samplerate = wav.getframerate()
    numsamples = wav.getnframes()
    print("チャンネル数 = ", numch)
    print("サンプル幅 (バイト数) = ", samplewidth)
    print("サンプリングレート (Hz) =", samplerate)
    print("サンプル数 =", numsamples)
    print("録音時間 =", numsamples / samplerate)
    wav = np.frombuffer(wav.readframes(wav.getnframes()) , dtype= "int16")
    '''
    #numch = wav.channels()
    samplerate = s.frame_rate
    numsamples = s.duration_seconds
     
    wav = np.array(s.get_array_of_samples())
    downsamp = (samplerate/downrate)
    #print(downsamp)
    
    arr=[]
    i = 0
    while(1):
        try:
            intnum = int(i)
            i = i+downsamp
            arr.append(wav[intnum])
        except:
            break
    
    downwav = np.array(arr)
    #14118
    N=(downrate//1000)*20
    #320
    #hammingWindow = np.hamming(N)    # ハミング窓
    hanningWindow = np.hanning(N)    # ハニング窓
    #blackmanWindow = np.blackman(N)  # ブラックマン窓
    #bartlettWindow = np.bartlett(N)  # バートレット窓

    arr = []
    i,j = 0,0
    cut = (downrate//1000)*2
    #(32)
    while(j < len(downwav)):
        j = N+(N-cut)*i
        arr.append(downwav[((N-cut)*i):(N+(N-cut)*i)])
        i+=1
    
    arr = np.array(arr[:-1])
    #print(arr.shape)
    window = hanningWindow*arr
    
    # ローパスフィル処理（カットオフ周波数(N/2)を超える帯域の周波数信号を0にする）
    spectle = np.abs(np.fft.fft(window))[:,:N//2]
    
    #make mel filters
    #ローパスフィルタにより16000 -> 8000, indexも320 -> 160に減る
    uplim = downrate//2 #上限
    maxind = N//2
    chnel = 26
    upmel = transmel(uplim)
    #unmel = transmel(unlim)
    tmp = upmel/chnel
    melarr = np.arange(0, chnel+1) * tmp
    helzarr = transhelz(melarr)
    #8000以降をカットしただけで、index間隔は320
    helzarr = np.round(helzarr / (downrate/N))
    helzarr = helzarr.astype(int)
    ##helzarr = np.hstack((np.hstack(([0], helzarr)), maxind))
    #print(helzarr)
    
    melfilters = np.zeros((chnel, maxind))
    tmp = 0
    while(tmp < len(helzarr)-2):
        start,top,end = helzarr[tmp],helzarr[tmp+1],helzarr[tmp+2]
        for i,j in zip(np.arange(start, top), np.arange(top, end)):
            melfilters[tmp, i] = (1/(top-start)) * (i-start)
            melfilters[tmp, j] = 1 - (1/(end-top)) * (j-top)
        tmp += 1
        
    #print(melfilters.shape)
    spectle = (np.reshape(spectle, (-1, 1, maxind)) * melfilters).sum(1)
    spectle = np.log10(spectle+1e-8)
    
    #mfcc = dct(spectle)
    mfcc=scipy.fftpack.realtransforms.dct(spectle,type=2,norm="ortho", axis=-1)
    return mfcc[:,:12]


if __name__ == "__main__":
    import AcousticModel as AM
    from bs4 import BeautifulSoup as bs
    
    path = 'datasets'
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)    
    addr = glob.glob('./wiki_eng_speech/*/*.ogg')
    teac_addr = glob.glob('./wiki_eng_speech/*/*.swc')
    f = open('phones.txt', 'rb')
    li = pickle.load(f)
    f.close()
    phones = np.array(li)    
    #sound = AudioSegment.from_file('/home/admin/python_work/音声認識/wiki_eng_speech/Adrian_Lowe/audio.ogg','ogg')
    #wav = wave.open('/home/admin/python_work/音声認識/audio (online-audio-converter.com).mp3', 'r')
    nolist=[]
    zure = 0
    flag = False
    for og in range(len(addr)):
        if addr[og][:-9] != teac_addr[og+zure][:-11]:
            if addr[og][:-10] != teac_addr[og+zure][:-11]:
                #print('Error',addr[og][:-10],teac_addr[og+zure][:-11])
                zure -= 1
                
                #print(addr[og],teac_addr[og+zure])
        print(addr[og])
        #continue
        f = open(teac_addr[og+zure], encoding='utf-8')
        xml = f.read()
        f.close()
        soup = bs(xml, 'lxml')
        soup = soup.find_all("ph")
        if len(soup) == 0:
            continue
        #sound = AudioSegment.from_file(addr[og],'ogg')
        try:
            sound = AudioSegment.from_file(addr[og],'ogg')
        except:
            nolist.append(addr[og])
            continue
        
               
        ph = np.array([[j.get("type"), j.get("start"), j.get("end")] for j in soup])
        ind = [np.where(phones == ph[j, 0]) for j in range(len(ph))]
        arr2 = [np.array([ph[j, 1], ph[j, 2]]) for j in range(len(ph))]
        str_end = np.array(arr2,dtype=np.int)
        
        #print(str_end.shape,flag)
        
        if flag == False:
            mfcc = []
            count = 0            
            for i in str_end:
                try:
                    s = sound[i[0]:i[1]]
                    mfcc.append([[phones[ind[count]]],[ind[count]],[calc_mfcc(s)]])
                except:
                    #print('outind',i[0],i[1],count,len(sound))
                    flag = True
                    L_s = len(sound)
                    break
                if phones[ind[count]] != ph[count,0]:
                    print(phones[ind[count]],ind[count],ph[count,0])
                    break
                count += 1
        elif flag == True:
            str_end = str_end[count:] - L_s
            flag = False
            for i in str_end:
                try:
                    s = sound[i[0]:i[1]]
                    mfcc.append([[phones[ind[count]]],[ind[count]],[calc_mfcc(s)]])
                except:
                    L_s += len(sound)
                    flag = True
                    break
                if phones[ind[count]] != ph[count,0]:
                    print(phones[ind[count]],ind[count],ph[count,0])
                    break
                count += 1                

        np.save(path+'/teach_train'+str(og),np.array(mfcc))
        
    print("nolist")
    print(nolist)
    np.save('nolist.txt',np.array(nolist))

