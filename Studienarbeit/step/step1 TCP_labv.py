import socket
import numpy as np
import time
import os
from os.path import basename

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    
def timestamp(s):
    try:
        s=s.replace(' ', '')
        s=s.replace('-', '')
        s=s.replace(':', '')
        return s
    except Exception:
        pass

positions=[]
def sendto(filename):
    #以二进制形式读取文件全部内容
    with open(filename, "rb") as f:
        content=f.read()
    #文件大小，之后会与buffersize作比较
    f_size=len(content)
    for start in range(f_size//buffersize+1):
        positions.append(start*buffersize)
    #设置发送缓存区大小
    #labv.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffersize)
    #发送文件数据，直到所有分块都收到确认，否则就循环发送
    #while positions:
    for pos in positions:
        pc.sendall(content[pos:pos+buffersize])
    labv.close()
    
labv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
labv_host = socket.gethostbyname(socket.gethostname())
labv_port = 9990
labv_addr = labv_host, labv_port
labv.bind(labv_addr)


pc_host = socket.gethostbyname(socket.gethostname())
pc_port = 8880
pc_addr = pc_host, pc_port
'''
labv.connect(pc_addr)
'''

buffersize = 32*1024
#传输数据分隔符
SEPERATOR = "<SEPERATOR>"

labv.listen(5)

while True:
    pc, address = labv.accept()
    print(f"Connection from {address} has been established!")
    data = pc.recv(buffersize).decode()
    command, sampling_number=data.split(",")
    if command == "IQ":
        if is_integer(sampling_number):
            print(f'right and sampling number is {sampling_number} from {address}')
            msg1=bytes('hello, PC, you are right', 'utf-8')
            pc.send(msg1)
            #读取数据并产生对应的采样数据
            n_samples = int(sampling_number)
            #n1 = np.random.normal(0,np.sqrt(0.5),(n_samples,))
            #n2 = np.random.normal(0,np.sqrt(0.5),(n_samples,))
            #n = n1+1j*n2
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
            n1 = np.random.normal(0,np.sqrt(0.5),(n_samples,))
            n2 = np.random.normal(0,np.sqrt(0.5),(n_samples,))
            n = n1+1j*n2
            for i in range(0,5):
                for j in range(sf):
                    n[delay[i]+j]=n[delay[i]+j]+f1[j]*attenuation[i]
            #将产生的数据存在一个.csv文件里
            path = 'G:/rawdata/ '
            localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            shijian=timestamp(localtime)
            filename=path+'{} '.format(n_samples)+shijian+'.csv'
            np.savetxt(filename, n, fmt='%.18e', delimiter=',')
            #读取文件大小
            file_size = os.path.getsize(filename)
            #传输数据分隔符
            SEPERATOR = "<SEPERATOR>"
            #发送文件名字和文件大小，必须进行编码处理
            pc.send(f"{filename}{SEPERATOR}{file_size}".encode())
            sendto(filename)
            #labv.close()
            pc.close()
            break
        else:
            print('Error: Please input an integer number!')
            msg2=bytes('hello, PC, you are wrong', 'utf-8')
            pc.send(msg2)
            labv.close()
            pc.close()
            break
    # other command (@TODO add oher command function)
    else:
        print("this command does not exist yet")
        labv.close()
        pc.close()
        break