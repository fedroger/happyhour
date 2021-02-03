import socket
import numpy as np
import pickle
from os.path import basename
import os

positions=[]
def recv(filebasename,file_size):
    path = 'G:/saved data/'
    filename=path+filebasename
    with open(filename, "wb") as f:
        for start in range(file_size//buffersize+1):
            #positions.append(start*buffersize)
        #while positions:
        #for pos in positions:
            data_received,addr = pc.recvfrom(buffersize)
            f.write(data_received)
    print('received successfully')
    

pc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pc_host = socket.gethostbyname(socket.gethostname())
pc_port = 8880
pc_addr = pc_host, pc_port
pc.bind(pc_addr)

labv_host = socket.gethostbyname(socket.gethostname())
labv_port = 9990
labv_addr = labv_host, labv_port

buffersize = 32*1024
SEPERATOR = "<SEPERATOR>"

request = input("please input sampling number:  ")
message = bytes(request, "utf-8")
pc.sendto(message, labv_addr)
while True:
    data, addr = pc.recvfrom(buffersize)
    #csv = pickle.loads(data)
    #print(csv)
    #nachricht = bytes("Hello, UDP Client", "utf-8")
    #server.sendto(nachricht, addr)
    print(data.decode())
    received,addr = pc.recvfrom(buffersize)
    filename, file_size = received.decode().split(SEPERATOR)
    print(f'filepath is {filename}')
    print(f'filesize is {file_size} Byte')
    filebasename = basename(filename)
    file_size = int(file_size)
    recv(filebasename,file_size)
    pc.close()
    break