import socket

import threading
import time
from struct import *
from tkinter import *
# socket.setblocking
# socket.setblocking(0)
# socket.settimeout(1)
socket.setdefaulttimeout(3)
runcmd=14593
timeoutCNT=0
# connections=[0]
# ReadSCANer=[0]
# WriteSCANer=[0]
def MB_Client_READ(sock):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    global timeoutCNT
    while True:
        
        if TI > 65535:
            TI=0

        FD=3
        addr=5
        cnt=1
        packet=pack(">HHBBBBHH",TI,0,0,6,1,FD,addr,cnt)
        # print("Request_READ :",packet)
        try:
            sock.send(packet)
        except:
            return
            # print("Request_WRITE  : timeout",timeoutCNT)

        # try:
        #     receivemesg=sock.recv(1024)
        #     print("Slave_WRITE Byte :", receivemesg)
        # except:
        #     print("Slave_READ Byte : timeout",timeoutCNT)
        # timeout_ms=0
        # while timeout_ms < 1000:
        try:
            receivemesg = sock.recv(1024)
            # print("Slave_WRITE Byte :", receivemesg)

        except socket.timeout:
            timeoutCNT=timeoutCNT+1
            listBOX.insert(END, str(sock.getpeername()[0])+" timeout count:"+str(timeoutCNT))
            
            # timeout_ms +=1 
            # time.sleep(0.001)
        except ConnectionError:
            listBOX.insert(END,str(sock.getpeername()[0])+ConnectionError)
            return

        TI=TI+1
        time.sleep(0.2)

def MB_Client_WRITE(sock):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    global timeoutCNT
    global runcmd
    while True:
        if TI > 65535:
            TI=0
    
        packet=pack(">HHHBBHHBHHHH",TI,0,15,1,16,startaddr,quantityaddr,bytecount, 6000,runcmd,200,300)
        # print("Request_WRITE :",packet)
        try:
            sock.send(packet)
        except:
            return

        # try:
        #     receivemesg=sock.recv(1024)
        #     print("Slave_WRITE Byte :", receivemesg)
        # except:
        #     print("Slave_READ Byte : timeout",timeoutCNT)
        # timeout_ms=0
        # while timeout_ms < 1000:
        try:
            receivemesg = sock.recv(1024)
            # print("Slave_WRITE Byte :", receivemesg)
        except socket.timeout:
            timeoutCNT=timeoutCNT+1
            listBOX.insert(END, str(sock.getpeername()[0])+" timeout count:"+str(timeoutCNT))
            
            # timeout_ms +=1 
            # time.sleep(0.001)
            
        except ConnectionError:
            print("Error ConnectionError:")
            listBOX.insert(END,str(sock.getpeername()[0])+ConnectionError)
            return   
        
        TI=TI+1
        time.sleep(0.2)

def TRY_run():
    global runcmd
    runcmd=14594
    # print("Success to RUN")
    listBOX.insert(END,"Success to RUN:14594")
    return

def TRY_stop():
    global runcmd
    runcmd=14593
    # print("Success to STOP")
    listBOX.insert(END,"Success to STOP:14593")
    return
    

def TRY_connect():
    CLIENT_NUM=int(entry2bt1.get())

    TI=0
    global connections
    connections=[x for x in range(CLIENT_NUM)]
    
    # for num in connections:
    index=0
    while index< CLIENT_NUM:
        connections[index]=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connections[index].setblocking(True)
        connections[index].settimeout(1)
        #HOST = entry2IPADDR1.get()+'.'+entry2IPADDR2.get()+'.'+entry2IPADDR3.get()+'.'+entry2IPADDR4.get()
        HOST = entry2IPADDR1.get()+'.'+entry2IPADDR2.get()+'.'+entry2IPADDR3.get()+'.'+str(int(entry2IPADDR4.get())+index)
        try:
            connections[index].connect((HOST,PORT))
            listBOX.insert(END,"Success to establish connection:"+HOST)
        except connections[index].timeout:
            listBOX.insert(END,"Failed to establish connection :"+HOST)
            
        # if   connections[index].connect((HOST,PORT))== False:
        #     print("Failed to establish connection")
        # else :
        #     print("Success to establish connection")

        index=index+1

def TRY_Start_Reust():
    CLIENT_NUM=int(entry2bt1.get())
    index=0
    global ReadSCANer
    global WriteSCANer
    ReadSCANer=[x for x in range(CLIENT_NUM)]
    WriteSCANer=[x for x in range(CLIENT_NUM)]
    while index < CLIENT_NUM:
        # connections[index]=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ReadSCANer[index] = threading.Thread(target=MB_Client_READ,args=(connections[index],))
        WriteSCANer[index]=threading.Thread(target=MB_Client_WRITE,args=(connections[index],))
        ReadSCANer[index].daemon = True 
        WriteSCANer[index].daemon = True 
        ReadSCANer[index].start()
        WriteSCANer[index].start()
        listBOX.insert(END," start request FD : 3 X1 ,FD:6 X4 : "+str(connections[index].getpeername()[0]))
        index=index+1

# def TRY_connectThread():
#         CONNECTOR[i] = threading.Thread(target=MB_Client_READ,args=(connections[index],))
#         CONNECTOR[i].start()

def TRY_disconnect():
    index=0
    while index < int(entry2bt1.get()):

        ReadSCANer[index]._delete
        WriteSCANer[index]._delete
        connections[index].close()
        index+=1
        
    listBOX.insert(END,"disconnect all connections")
    print("disconnect all connections")


# modbus multi-client window setting 
Button_X=575
BOX_X=475
HOST = '192.168.10.10'
PORT= 502
root= Tk()
root.title("Modbus Test tool for multi-64")

root.geometry("640x400+500+200")
root.resizable(False, False)
# IP ADDRESS texture
label1 =Label(root, text ="Start IP address:")
label1.place(x=BOX_X-100,y=15)
entry2IPADDR1=Entry(root)
entry2IPADDR1.place(x=BOX_X+0,y=15,width=30,height=25)
entry2IPADDR1.insert(END,"192")
entry2IPADDR2=Entry(root)
entry2IPADDR2.place(x=BOX_X+32,y=15,width=30,height=25)
entry2IPADDR2.insert(END,"168")
entry2IPADDR3=Entry(root)
entry2IPADDR3.place(x=BOX_X+32*2,y=15,width=30,height=25)
entry2IPADDR3.insert(END,"0")
entry2IPADDR4=Entry(root)
entry2IPADDR4.place(x=BOX_X+32*3,y=15,width=30,height=25)
entry2IPADDR4.insert(END,"10")

#connect button textrue
label2 =Label(root, text ="num of node:")
label2.place(x=BOX_X-100,y=50)
btn1 = Button(root,text="connect",command =TRY_connect)
btn1.place(x=Button_X,y=50)
entry2bt1=Entry(root)
entry2bt1.place(x=BOX_X,y=50,width=80,height=25)
entry2bt1.insert(END,"1")
#Start Req button textrue
btn2 = Button(root,text="Start Req",command =TRY_Start_Reust)
btn2.place(x=Button_X,y=50+50,width=60,height=25)
#run button textrue
btn3 = Button(root,text="run",command =TRY_run)
btn3.place(x=Button_X,y=50+50+50,width=50,height=25)
#stop button textrue 
btn3 = Button(root,text="stop",command =TRY_stop)
btn3.place(x=Button_X,y=50+50+50+50,width=50,height=25)
#disconnect button textrue
btn4 = Button(root,text="disconnect",command=TRY_disconnect,)
btn4.place(x=Button_X,y=50+50+50+200,width=65,height=25)
#log text
frame=Frame(root)
frame.place(x=15,y=20,width=350,height=350)
# frame.pack(fill=X,anchor=N,pady=5)
scrollbar=Scrollbar(frame)
scrollbar.pack(side=RIGHT,fill=Y)
listBOX=Listbox(frame,yscrollcommand=scrollbar,bg="white",height=27,width=11)
listBOX.pack(side=LEFT,fill=X,expand=1)
scrollbar.config(command=listBOX.yview)

# txt4log=Text(root)
# txt4log.place(x=15,y=50,width=100,height=300)
# txt4log.insert(END,"")

if __name__ == "__main__":

    root.mainloop()