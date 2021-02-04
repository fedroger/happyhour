import pymongo
from pymongo import MongoClient
import pickle
from bson.binary import Binary
import numpy as np


#connection establishment
client = MongoClient("mongodb+srv://Yinhaonan:yhn2020@yhnmongodb.334xk.mongodb.net/yhndb1?retryWrites=true&w=majority")
db1 = client["test"]
collection11 = db1["AP1"]
collection12 = db1["AP2"]
collection13 = db1["AP3"]
collection14 = db1["AP4"]
collection15 = db1["AP5"]
collection16 = db1["AP6"]

tm = '20210204215951'
sampling_number = '4096'
position = '(1,1)'
# !!!load .csv file and convert it into numpy array in specific shape 
dataload = np.loadtxt('G:\saved data\ 4096 20210204215951.csv', 
                      dtype='str', delimiter=',')
dataconvert = dataload.astype(np.complex64)
datas = dataconvert.reshape(4096,1)
#print(datas)


#!!!import all kinds of datas in collection11 in batch

e = Binary(pickle.dumps(datas,protocol=2))
label = {"time":tm, "sampling number":sampling_number,
             "position": position, "I/Qsamples": e}
collection12.insert_one(label)
        
        
        
        
        
        
        
        
        
        
        
        
        
