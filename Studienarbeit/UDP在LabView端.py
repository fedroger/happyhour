import socket
import numpy as np
import pickle

'''
dataload = np.loadtxt('randomdata.csv', dtype='str', delimiter=',')
dataconvert = dataload.astype(np.complex64)
datas = dataconvert.reshape(221184,1)
'''

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        pass


labv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
labv_host = socket.gethostbyname(socket.gethostname())
labv_port = 9990
labv_addr = labv_host, labv_port
labv.bind(labv_addr)

pc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pc_host = socket.gethostbyname(socket.gethostname())
pc_port = 8880
pc_addr = pc_host, pc_port

while True:
    
    data, addr = labv.recvfrom(4096)

    if is_integer(data.decode()):
        print(f'right and sampling number is {data.decode()} from {addr}')
        msg1=bytes('hello, PC, you are right', 'utf-8')
        labv.sendto(msg1, pc_addr)
        labv.close()
        break
    else:
        print('Error: Please input an integer number!')
        msg2=bytes('hello, PC, you are wrong', 'utf-8')
        labv.sendto(msg2, pc_addr)
        labv.close()
        break
    
#csv = pickle.dumps(datas)
#client.sendto(csv, ADDR)
#data, addr = client.recvfrom(4096)
#print(f"Server from {addr} says: {data.decode()}")

