import pymongo
from pymongo import MongoClient
import pickle
from bson.binary import Binary
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

client = MongoClient("mongodb+srv://Yinhaonan:yhn2020@yhnmongodb.334xk.mongodb.net/yhndb1?retryWrites=true&w=majority")
db1 = client["test"]
collection11 = db1["AP1"]
collection12 = db1["AP2"]
collection13 = db1["AP3"]
collection14 = db1["AP4"]
collection15 = db1["AP5"]
collection16 = db1["AP6"]


db2 = client["Estimation"]
collection21 = db2["AP01"]
collection22 = db2["AP02"]
collection23 = db2["AP03"]
collection24 = db2["AP04"]
collection25 = db2["AP05"]
collection26 = db2["AP06"]



#!!!extract datas from db1, process datas with pandas and then import into db2
result = collection12.find_one({'time': '20210205002153',
                                'position' : '(1,2)'})
y = pickle.loads(result['I/Qsamples'])
#z = pd.DataFrame(y)
z=y.reshape(5000,)
print(z)

#!!!channel estimation
SF = 8
sf = 2**SF
a = np.arange(sf)
c = np.arange(5000-sf+1) 
'有效数据个数'
#print(a)
f1=[]
for i in range(sf):
    f=(np.exp(complex(0,np.pi*a[i]**2/sf)))*5
    f1=np.append(f1, f)
b =np.abs((np.correlate(z, f1, mode='valid')))/(5*5*sf)
#print(b)
plt.figure(figsize=(40, 20))
plt.xlim(0,5000-sf+1)
plt.ylim(b.min(),b.max())
plt.title('cross-correlation')
plt.stem(c,b,use_line_collection=(True)) 
plt.show()
print("b中最大的数为{}，位于第{}位".format(np.max(b), np.argmax(b)))
delay_estimation=np.array([np.argmax(b)])
attenuation_est=np.array([np.max(b)])
#print(delay_estimation)
for i in range(4):
    c = b
    c[np.argmax(c)] = np.min(b)
    #print(c)
    delay_estimation=np.append(delay_estimation, np.argmax(c))
    attenuation_est=np.append(attenuation_est,np.max(c))
    print("b中第{}大的数为{}，位于第{}位".format(i+2, np.max(c), np.argmax(c)))
    b = c
print(delay_estimation)  
print(attenuation_est)

#!!! save the results in estimation database
dl_est='{}'.format(delay_estimation)
at_est='{}'.format(attenuation_est)
label = {"time":'20210205002153', "position": "(1,2)", 
         "delay estimation": dl_est, 
         "attenuation estimation":at_est}
collection22.insert_one(label)








 