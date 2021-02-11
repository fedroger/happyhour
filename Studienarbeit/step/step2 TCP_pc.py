import socket
import numpy as np
from os.path import basename



positions=[]
def recv(filebasename,file_size):
    path = 'G:/saved data/'
    filename=path+filebasename
    with open(filename, "wb") as f:
        for start in range(file_size//buffersize+1):
            #positions.append(start*buffersize)
        #while positions:
        #for pos in positions:
            data_received = pc.recv(buffersize)
            f.write(data_received)
    print('received successfully')
    
buffersize = 32*1024
#传输数据分隔符
SEPERATOR = "<SEPERATOR>"

pc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pc_host = socket.gethostbyname(socket.gethostname())
pc_port = 8880
pc_addr = pc_host, pc_port
pc.bind(pc_addr)

labv_host = socket.gethostbyname(socket.gethostname())
labv_port = 9990
labv_addr = labv_host, labv_port
pc.connect(labv_addr)

buffersize = 32*1024
SEPERATOR = "<SEPERATOR>"

request = input("please input command and corresponding sampling number :  ")
message = bytes(request, "utf-8")
pc.send(message)


while True:
    data = pc.recv(buffersize)
    print(data.decode())
    if data.decode()=='hello, PC, you are right':
        received = pc.recv(buffersize).decode()
        filename, file_size = received.split(SEPERATOR)
        print(f'filepath is {filename}')
        print(f'filesize is {file_size} Byte')
        filebasename = basename(filename)
        file_size = int(file_size)
        recv(filebasename,file_size)
        pc.close()
        break
    else:
        pc.close()
        break