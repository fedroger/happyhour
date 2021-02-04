import numpy as np
import matplotlib.pyplot as plt
import random


correct=0
incorrect=0
for time in range(3):
    SF = 8
    sf = 2**SF
    a = np.arange(sf)
    c = np.arange(3000-sf+1) 
    '有效数据个数'
    #print(a)
    f1=[]
    for i in range(sf):
        f=(np.exp(complex(0,np.pi*a[i]**2/sf)))*5
        f1=np.append(f1, f)
        #print(f1)
        #np.random.seed(10)
    delay=[10,100,150,200,500]
    attenuation=[0.8,0.7,0.5,0.4,0.1]
    n1 = np.random.normal(0,np.sqrt(0.5),(3000,))
    n2 = np.random.normal(0,np.sqrt(0.5),(3000,))
    n = n1+1j*n2

    for i in range(0,5):
        for j in range(sf):
            n[delay[i]+j]=n[delay[i]+j]+f1[j]*attenuation[i]
        '''
        print(f1)
        print(zeroappend1)
        print(zeroappend1.size)
        print(zeroappend2)
        print(zeroappend2.size)
        print(sequence2)
        print(sequence2.size)
        print(sequence3)
        print(sequence3.size)
        '''
   
    b =np.abs((np.correlate(n, f1, mode='valid')))/(5*5*sf)
    #print(b)
    plt.figure(figsize=(40, 20))
    plt.xlim(0,3000-sf+1)
    plt.ylim(b.min(),b.max())
    plt.title('cross-correlation')
    plt.stem(c,b,use_line_collection=(True)) 
    plt.show()
    print("b中最大的数为{}，位于第{}位".format(np.max(b), np.argmax(b)))
    delay_estimation=np.array([np.argmax(b)])
    #print(delay_estimation)
    for i in range(4):
        c = b
        c[np.argmax(c)] = np.min(b)
        #print(c)
        delay_estimation=np.append(delay_estimation, np.argmax(c))
        print("b中第{}大的数为{}，位于第{}位".format(i+2, np.max(c), np.argmax(c)))
        b = c
    print(delay_estimation)    
    if (delay==delay_estimation).all()==True:
        correct+=1
    else:
        incorrect+=1
        
print("correct",correct)
print("incorrect",incorrect)    
