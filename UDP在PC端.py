import socket
import numpy as np
import pickle

pc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pc_host = socket.gethostbyname(socket.gethostname())
pc_port = 8880
pc_addr = pc_host, pc_port
pc.bind(pc_addr)
labv_host = socket.gethostbyname(socket.gethostname())
labv_port = 9990
labv_addr = labv_host, labv_port

request = input("please input sampling number:  ")
message = bytes(request, "utf-8")
pc.sendto(message, labv_addr)
while True:
    data, addr = pc.recvfrom(4096)
    #csv = pickle.loads(data)
    #print(csv)
    #nachricht = bytes("Hello, UDP Client", "utf-8")
    #server.sendto(nachricht, addr)
    print(data.decode())
    pc.close()
    break
