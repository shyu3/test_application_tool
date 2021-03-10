import socket

import threading
import time
from struct import *

quit=0
def send(sock):
    TI=1
    while True:
        FD=3
        addr=0
        cnt=10
        packet=pack(">HHBBBBHH",TI,0,0,6,1,FD,addr,cnt)
        print("Request :",packet)
        sock.send(packet)
        TI=TI+1
        time.sleep(1)

def receive(sock):
    while True:
        receivemesg=sock.recv(1024)
        print("Slave Byte :", receivemesg)
        #if input("input:")=='q' :
        #  client_socket.close()
sendmesg=0
HOST = '192.168.10.10'
PORT= 502

client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))

# client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)
# client_socket.setsockopt(socket.SOL_TCP,socket.TCP_KEEPIDLE,10)
# client_socket.setsockopt(socket.SOL_TCP,socket.TCP_KEEPINTVL,2)
# client_socket.setsockopt(socket.SOL_TCP,socket.TCP_KEEPCNT,3)

# sender = threading.Thread(target=send,args=(client_socket,))
# receiver=threading.Thread(target=receive,arg=(client_socket,))

TI=0 #Transfer ID
while True:
    FD =16
    startaddr=1
    quantityaddr=1
    cnt=TI
    datavalue=258

    FD=int(input("input FD:"))
    if FD == 'q':
        client_socket.close()
    
    startaddr=int(input("input startaddr:"))

    # packet=pack("BBBBBBBB",1,2,3,4,5,6,7,8)

    # # FD:0x03 hold regist(40000)MBAP/2Byte            /2Byte     /1Byte         +PDU:1Byte         /2 Byte    /2 Byte
    # packet=pack(">HHHBBHH",TI,0,6,1,3,startaddr,quantityaddr)
    # # FD:0x04 input regist(30000)MBAP/2Byte            /2Byte     /1Byte         +PDU:1Byte         /2 Byte    /2 Byte
    # packet=pack(">HHHBBHH",TI,0,6,1,4,startaddr,quantityaddr)
    # # FD:0x06 hold regist(40000)MBAP/2Byte            /2Byte     /1Byte         +PDU:1Byte         /2 Byte    /2 Byte
    # packet=pack(">HHHBBHH",TI,0,6,1,6,startaddr,quantityaddr)
    # # FD:0x10 hold regist(40000)MBAP/2Byte            /2Byte     /1Byte         +PDU:1Byte         /2 Byte    /2 Byte
    # packet=pack(">HHHBBHH",TI,0,9,1,16,startaddr,quantityaddr,bytecount, datavalue)

    if FD== 16:
        quantityaddr=int(input("input quantityaddr : "))
        bytecount=2*quantityaddr
        datavalue=int(input("input datavalue:"))

        packet=pack(">HHHBBHHBH", TI,0,9,1,16,startaddr, quantityaddr,bytecount,datavalue)
    else:
        if FD!=6:
            datavalue=int(input("input quantityaddr : "))
        else:
            datavalue=int(input("input datavalue : "))
    
        packet=pack(">HHHBBHH", TI,0,6,1, FD, startaddr,datavalue)

    print("Request :",packet)
    client_socket.send(packet)

    receivemesg=client_socket.recv(1024)
    print("Slave Byte:", receivemesg)
    TI=TI+1

    #time.sleep(1)
    #print("Slave string: ", receivemesg.decode())

# sender.start()
# receiver.start()
