import socket

import threading
import time
from struct import *

quit=0

# client_socket_struct[2] 
def MB_Client_READ(sock):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    while True:
        FD=3
        addr=5
        cnt=1
        packet=pack(">HHBBBBHH",TI,0,0,6,1,FD,addr,cnt)
        print("Request_READ :",packet)
        sock.send(packet)
        receivemesg=sock.recv(1024)
        print("Slave_READ Byte :", receivemesg)
        
        TI=TI+1
        time.sleep(0.2)

def MB_Client_WRITE(sock):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    while True:

        packet=pack(">HHHBBHHBHHHH",TI,0,15,1,16,startaddr,quantityaddr,bytecount, 0,14593,200,300)
        print("Request_WRITE :",packet)
        sock.send(packet)
        receivemesg=sock.recv(1024)
        print("Slave_WRITE Byte :", receivemesg)
        TI=TI+1
        time.sleep(0.2)

        #if input("input:")=='q' :
        #  client_socket.close()

def send(sock):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    while True:
        FD=3
        addr=5
        cnt=1
        packet=pack(">HHBBBBHH",TI,0,0,6,1,FD,addr,cnt)
        print("Request_READ :",packet)
        sock.send(packet)
        packet=pack(">HHHBBHHBHHHH",TI,0,15,1,16,startaddr,quantityaddr,bytecount, 0,14593,200,300)
        print("Request_WRITE :",packet)
        sock.send(packet)
        TI=TI+1
        time.sleep(0.2)

def receive(sock):
    while True:
        receivemesg=sock.recv(1024)
        print("Slave01 Byte :", receivemesg)
        #if input("input:")=='q' :
        #  client_socket.close()
sendmesg=0
HOST = '192.168.10.10'
PORT= 502

# client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# client_socket.connect((HOST,PORT))

# client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_KEEPALIVE,1)
# client_socket.setsockopt(socket.SOL_TCP,socket.TCP_KEEPIDLE,10)
# client_socket.setsockopt(socket.SOL_TCP,socket.TCP_KEEPINTVL,2)
# client_socket.setsockopt(socket.SOL_TCP,socket.TCP_KEEPCNT,3)
# connector=threading.Thread(target=connect,args=(client_socket,))
# sender = threading.Thread(target=send,args=(client_socket,))
# receiver=threading.Thread(target=receive,args=(client_socket,))

TI=0 #Transfer ID
if __name__ == "__main__":
    CLIENT_NUM=5
    TI=0
    connections=[x for x in range(CLIENT_NUM)]
    sender=[x for x in range(CLIENT_NUM)]
    receiver=[x for x in range(CLIENT_NUM)]
    # for num in connections:
    index=0
    while connections[index] < 2:
        connections[index]=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        HOST = '192.168.10.' + str(index+10)
        if connections[index].connect((HOST,PORT)) == False:
            print("Failed to establish connection")
        else :
            sender[index] = threading.Thread(target=send,args=(connections[index],))
            receiver[index]=threading.Thread(target=receive,args=(connections[index],))
            sender[index].start()
            receiver[index].start()  
            print("Success to establish connection")

        index=index+1

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
        # packet=pack(">HHHBBHHBH",TI,0,9,1,16,startaddr,quantityaddr,bytecount, datavalue)

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
