import socket
import numpy as np
import pickle
import time
import os

'''
dataload = np.loadtxt('randomdata.csv', dtype='str', delimiter=',')
dataconvert = dataload.astype(np.complex64)
datas = dataconvert.reshape(221184,1)
'''
#判断是否为整数的函数
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        pass

#删除时间格式之间的特殊字符和空格的函数
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
    labv.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffersize)
    #发送文件数据，直到所有分块都收到确认，否则就循环发送
    #while positions:
    for pos in positions:
        labv.sendto(content[pos:pos+buffersize], pc_addr)
    labv.close()


labv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
labv_host = socket.gethostbyname(socket.gethostname())
labv_port = 9990
labv_addr = labv_host, labv_port
labv.bind(labv_addr)

pc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pc_host = socket.gethostbyname(socket.gethostname())
pc_port = 8880
pc_addr = pc_host, pc_port

buffersize = 32*1024
while True:
    
    data, addr = labv.recvfrom(buffersize)
    '''
    这里接受32kB数据量，UDP最多能接受65507字节，如果超过考虑切片
    一个复数的大小是32字节。
    sys.getsizeof()可以计算括号中的东西所占字节大小
    '''
    if is_integer(data.decode()):
        print(f'right and sampling number is {data.decode()} from {addr}')
        msg1=bytes('hello, PC, you are right', 'utf-8')
        labv.sendto(msg1, pc_addr)
        #读取数据并产生对应的采样数据
        n_samples = int(data.decode())
        n1 = np.random.normal(0,np.sqrt(0.5),(n_samples,))
        n2 = np.random.normal(0,np.sqrt(0.5),(n_samples,))
        n = n1+1j*n2
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
        labv.sendto(f"{filename}{SEPERATOR}{file_size}".encode(), pc_addr)
        #文件传输
        sendto(filename)
        
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