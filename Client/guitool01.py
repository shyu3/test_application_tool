import socket

import threading
import time
from struct import *
from tkinter import *
import tkinter.ttk
# socket.setblocking
# socket.setblocking(0)
# socket.settimeout(1)
socket.setdefaulttimeout(3)
runcmd=14593

# connections=[0]
# ReadSCANer=[0]
# WriteSCANer=[0]
def MB_Client_READ(sock,ind):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    timeoutCNT=0
    ReceiveCnt_READ=0
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

        try:
            receivemesg = sock.recv(1024)
            ReceiveCnt_READ+=1
            if ind<32:
                treeTable01.set(ind, column="one1", value=ReceiveCnt_READ)
            else :
                treeTable02.set(ind, column="one2", value=ReceiveCnt_READ)
            # print("Slave_WRITE Byte :", receivemesg)

        except socket.timeout:
            timeoutCNT=timeoutCNT+1
            if ind<32:
                treeTable01.set(ind, column="four1", value=timeoutCNT)
            else :
                treeTable02.set(ind, column="four2", value=timeoutCNT)
            listBOX.insert(END, str(sock.getpeername()[0])+" timeout count:"+str(timeoutCNT))

        except ConnectionError:
            listBOX.insert(END,"ConnectionError"+str(sock.getpeername()[0]))
            return

        TI=TI+1
        time.sleep(0.2)

def MB_Client_WRITE(sock,ind):
    TI=1
    startaddr=5
    quantityaddr=4
    bytecount=8
    timeoutCNT=0
    ReceiveCnt_WRITE=0
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

        try:
            receivemesg = sock.recv(1024)
            ReceiveCnt_WRITE+=1
            if ind<32:
                treeTable01.set(ind, column="two1", value=ReceiveCnt_WRITE)
            else :
                treeTable02.set(ind, column="two2", value=ReceiveCnt_WRITE)

            # print("Slave_WRITE Byte :", receivemesg)
        except socket.timeout:
            timeoutCNT=timeoutCNT+1
            if ind<32:
                treeTable01.set(ind, column="four1", value=timeoutCNT)
            else :
                treeTable02.set(ind, column="four2", value=timeoutCNT)
            # listBOX.insert(END, str(sock.getpeername()[0])+" timeout count:"+str(timeoutCNT))

        except ConnectionError:
            listBOX.insert(END,"ConnectionError"+str(sock.getpeername()[0]))
            # root.showinfo("Cuation!", str(sock.getpeername()[0])+"disconnected")
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
    entry2bt1.configure(state='disabled')
    btn1.configure(state='disabled')
    btn2.configure(state='normal')
    global connections
    connections=[x for x in range(CLIENT_NUM)]
    # for num in connections:
    index=0
    while index< CLIENT_NUM:
        connections[index]=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connections[index].setblocking(True)
        connections[index].settimeout(1)

        HOST = entry2IPADDR1.get()+'.'+entry2IPADDR2.get()+'.'+entry2IPADDR3.get()+'.'+str(int(entry2IPADDR4.get())+index)
        try:
            connections[index].connect((HOST,PORT))
            listBOX.insert(END,"Success to establish connection:"+HOST)
            if index<32:
                treeTable01.insert('', index, text=HOST,values=[0,0,"stop",0],iid=index)
            else :
                treeTable02.insert('', index-32, text=HOST,values=[0,0,"stop",0],iid=index)
        except socket.timeout:
            listBOX.insert(END,"Failed to establish connection:"+HOST)
            if index<32:
                treeTable01.insert('', index, text=HOST,values=[0,0,"unconnected",0],iid=index)
            else :
                treeTable02.insert('', index-32, text=HOST,values=[0,0,"unconnected",0],iid=index)

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
        try:
            ReadSCANer[index] = threading.Thread(target=MB_Client_READ,args=(connections[index],index,))
            WriteSCANer[index]=threading.Thread(target=MB_Client_WRITE,args=(connections[index],index,))
            ReadSCANer[index].daemon = True
            WriteSCANer[index].daemon = True
            ReadSCANer[index].start()
            WriteSCANer[index].start()
            listBOX.insert(END," start request FD : 3 X1 ,FD:6 X4")
        except:
            listBOX.insert(END,"No connection:"+str(connections[index].getpeername()[0]))

        index=index+1


def TRY_disconnect():
    index=0
    entry2bt1.configure(state='normal')
    btn1.configure(state='normal')
    btn2.configure(state='disabled')
    while index < int(entry2bt1.get()):
        try:
            ReadSCANer[index]._delete
            WriteSCANer[index]._delete
            if index<32:
                treeTable01.delete(index)
            else:
                treeTable02.delete(index)
        except:
            print("No ReadSCANer, WriteSCANer Thread")
            if index<32:
                treeTable01.delete(index)
            else:
                treeTable02.delete(index)
        connections[index].close()
        index+=1
    
    listBOX.insert(END,"disconnect all connections")
    print("disconnect all connections")

def TRY_clearlog():
    listBOX.delete(0,END)


# modbus multi-client window setting 
Button_X=575+440
BOX_X=475+440
HOST = '192.168.10.10'
PORT= 502
root= Tk()
root.title("Modbus Test tool for multi-64")

root.geometry("1080x600+500+200")
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
btn2 = Button(root,text="Start Req",command =TRY_Start_Reust,state='disabled')
btn2.place(x=Button_X,y=50+50-20,width=60,height=25)
#run button textrue
btn3 = Button(root,text="run",command =TRY_run)
btn3.place(x=Button_X,y=50+50+50-40,width=50,height=25)
#stop button textrue
btn3 = Button(root,text="stop",command =TRY_stop)
btn3.place(x=Button_X,y=50+50+50+50-60,width=50,height=25)
#disconnect button textrue
btn4 = Button(root,text="disconnect",command=TRY_disconnect,)
btn4.place(x=Button_X,y=50+50+50+100-80,width=65,height=25)
#clearlog button textrue
btn5 = Button(root,text="clear log",command=TRY_clearlog,)
btn5.place(x=Button_X,y=50+50+50+150-80,width=65,height=25)
#log text
frame=Frame(root)
frame.place(x=BOX_X-125,y=50+50+50+100+50,width=290,height=300-20)
# frame.pack(fill=X,anchor=N,pady=5)
scrollbar=Scrollbar(frame)
scrollbar.pack(side=RIGHT,fill=Y)
listBOX=Listbox(frame,yscrollcommand=scrollbar,bg="white",height=27,width=11)
listBOX.pack(side=LEFT,fill=X,expand=1)
scrollbar.config(command=listBOX.yview)
# txt4log=Text(root)
# txt4log.place(x=15,y=50,width=100,height=300)
# txt4log.insert(END,"")

# tree table
treeTable01=tkinter.ttk.Treeview(root, columns=["one1", "two1","three1","four1"], displaycolumns=["one1", "two1","three1","four1"])
treeTable01.place(x=10,y=20,width=390,height=560)
treeTable01.column("#0", width=80, anchor="w")
treeTable01.heading("#0", text="Node IP", anchor="center")
treeTable01.column("#1", width=50, anchor="center")
treeTable01.heading("one1", text="ReadRxCnt", anchor="center")
treeTable01.column("#2", width=50, anchor="center")
treeTable01.heading("two1", text="WriteRxCnt", anchor="center")
treeTable01.column("#3", width=50, anchor="center")
treeTable01.heading("three1", text="Status", anchor="center")
treeTable01.column("#4", width=30, anchor="center")
treeTable01.heading("four1", text="ErrorCnt", anchor="center")

treeTable02=tkinter.ttk.Treeview(root, columns=["one2", "two2","three2","four2"], displaycolumns=["one2", "two2","three2","four2"])
treeTable02.place(x=400,y=20,width=390,height=560)
treeTable02.column("#0", width=80, anchor="w")
treeTable02.heading("#0", text="Node IP", anchor="center")
treeTable02.column("#1", width=50, anchor="center")
treeTable02.heading("one2", text="ReadRxCnt", anchor="center")
treeTable02.column("#2", width=50, anchor="center")
treeTable02.heading("two2", text="WriteRxCnt", anchor="center")
treeTable02.column("#3", width=50, anchor="center")
treeTable02.heading("three2", text="Status", anchor="center")
treeTable02.column("#4", width=30, anchor="center")
treeTable02.heading("four2", text="ErrorCnt", anchor="center")



if __name__ == "__main__":

    root.mainloop()