import numpy as np
import matplotlib.pyplot as plt
import random


SF = 6
sf = 2**SF
m=2
N_CP=16
N_seq=3*(N_CP+m*sf)
a=np.arange(sf)
b = np.arange(sf*m)
c=np.arange(N_seq)
d=np.arange(N_seq-sf+1)

gd=np.exp(-1j*np.pi*a**2/sf)
gu=np.exp(1j*np.pi*a**2/sf)
gd_seq=np.exp(-1j*np.pi*b**2/sf)
gu_seq=np.exp(1j*np.pi*b**2/sf)

gd_cp=np.zeros(N_CP)
gu_cp=np.zeros(N_CP)
zero=np.zeros(N_CP+m*sf,dtype=complex)
x=np.concatenate((gd_cp,gd_seq,gu_cp,gu_seq,zero))

n1 = np.random.normal(0,np.sqrt(0.5),(N_seq,))
n2 = np.random.normal(0,np.sqrt(0.5),(N_seq,))
n = n1+1j*n2
fo=3.5
print("real frequency offset is {}".format(fo) )    
for i in range(x.size):
    x[i]=x[i]*np.exp(1j*np.pi*2*(i/sf)*fo)
x=x+n

 

crrl_d_i = np.abs((np.correlate(x, gd, mode='valid'))) 
crrl_u_i = np.abs((np.correlate(x, gu, mode='valid'))) 




nd=[]
nu=[]
for i in range(d.size):
    if crrl_d_i[i]>40:
       nd=np.append(nd,i)
    elif crrl_u_i[i]>40:
        nu=np.append(nu,i)

#print(nd)
#print(nu)        
fo_est=(N_CP+m*sf-(nu[0]-nd[0]))*0.5 
print("integer frequency offset is {}".format(fo_est) )   
  
for i in range(x.size):
    x[i]=x[i]*np.exp(-1j*np.pi*2*(i/sf)*fo_est)  
    
autocorrelation=[]
jiaodu=[]
for i in range(x.size-2*sf+1):
    ji=x[i:i+sf]*np.conjugate(x[i+sf:i+sf*2])
    he=ji.sum()
    jueduizhi=np.abs(he)
    jiao=np.angle(he)
    autocorrelation=np.append(autocorrelation,jueduizhi)
    jiaodu=np.append(jiaodu,jiao)
#print(autocorrelation)
autocorrelation=np.concatenate((autocorrelation,np.zeros(2*sf-1)))    
e=np.arange(x.size-2*sf+1)   
plt.figure(figsize=(40, 20))
plt.xlim(-10,N_seq)
plt.ylim(autocorrelation.min(),autocorrelation.max())
plt.title('cross-correlation')
#plt.stem(c,autocorrelation,use_line_collection=(True))
plt.stem(d,crrl_d_i,use_line_collection=(True)) 
plt.stem(d,crrl_u_i,use_line_collection=(True))
plt.show() 
d1=[]
u1=[]   
maxposition=np.argmax(autocorrelation)
for i in range(maxposition-5,maxposition+5):
    d1=np.append(d1,autocorrelation[i])
for i in range(maxposition+sf*2+N_CP-5,maxposition+sf*2+N_CP+5):
    u1=np.append(u1,autocorrelation[i])
du1=d1+u1
index=np.argmax(du1)
#print(index)    
idealposition=maxposition+(index-5)
foo=jiaodu[idealposition]/(np.pi*2)
print("fractional frequency offset is {}".format(-foo) )
print("estimated frequency offset is {}".format(fo_est-foo))
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
