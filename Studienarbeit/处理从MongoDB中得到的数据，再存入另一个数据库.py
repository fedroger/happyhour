import pymongo
from pymongo import MongoClient
import pickle
from bson.binary import Binary
import numpy as np
import pandas as pd


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
result = collection12.find_one({'time': '20210204215951',
                                'position' : '(1,1)'})
y = pickle.loads(result['I/Qsamples'])
#z = pd.DataFrame(y)
y.reshape(4096,)
print(y)
#b=str(z.mean().div(100+100j)[0])
#c=str(z.div(100+100j).apply(lambda x: x**2).mean()[0])
#positionj = {"time":tm, "location":a, "channelest": b, "powerest": c}
#collection21.insert_one(positionj)        




#!!!section1: data processing from a certain collection
#result = collection4.find_one({'time': '15:00', 'location':'(4,4)'})
#print(type(result))
#print(result)

#y = pickle.loads(result['position'] )
#print(y)
#z = pickle.loads(result['I/Qsamples'])
#print(z)

#a=pd.DataFrame(z)
#print(a)

#b=a.mean().div(100+100j)[0]
#c=a.div(100+100j).apply(lambda x: x**2).mean()[0]




#section2: simplied version for test
#e=pd.DataFrame(np.arange(5).reshape((5,1)))
#print(e)

#q=e.div(5).apply(lambda x: x**2).mean()[0]
#print(q)