from socket import *
import time, sys, threading, errno
from multiprocessing import Process, Pipe, Queue
from multiprocessing.connection import wait

class ClientThread(threading.Thread):
    def __init__(self,conn,Tconn,Lconn):
        threading.Thread.__init__(self)
        self.pipe = Tconn
        self.list_pipe = Lconn
        self.csocket = conn
        self.addr = self.csocket.getpeername()
        self.addr = (self.addr[0] + ':' + str(self.addr[1]))

    def run(self):
        while True:
            try:            
                if self.pipe.poll():
                    s = self.pipe.recv()
                    if s[0] == self.addr:
                        self.pipe.send(s)
                        msg = bytes(s[1],'ASCII')
                        self.csocket.send(msg)
                msg = self.csocket.recv(2048).decode()
                self.pipe.send(msg)
                if msg=='HELLO':
                    self.csocket.send(b'CONNECTED')
                    name = self.csocket.recv(2048).decode()
                    info = (name,self.addr)
                    self.list_pipe.send(info)
                    self.csocket.send(b'NAME NOTED')
                else:                
                    self.csocket.send(b'OK')
            except ConnectionResetError:
                self.csocket.close()
                self.list_pipe.send(info)
                break
        self.pipe.send(("Client: " + self.addr + " Disconnected."))

class serverTCP(Process):
    def __init__(self,sock_conn, client, list_conn):
        Process.__init__(self)
        TCP_Data = ("",20305)
        self.pipe = sock_conn
        self.client_pipe = client
        self.list_pipe = list_conn
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sock.bind(TCP_Data)

    def run(self):
        self.sock.listen(10)
        while True:        
            conn, addr = self.sock.accept()
            sock_T = ClientThread(conn, self.client_pipe, self.list_pipe)
            sock_T.start()
            self.pipe.send(addr[0] + ':' + str(addr[1]))
            
class list_IRDevices(Process):
    def __init__(self, conn1, conn2):
        Process.__init__(self)
        self.dict = {}    
        self.TCP_pipe = conn1
        self.main_pipe = conn2
    
    def run(self):
        while True:
            a = self.TCP_pipe.recv()
            name, info = a[:]
            if len(a) == 2:
                if name not in self.dict:
                    self.dict[name] = info
                else:
                    del self.dict[name]
            self.main_pipe.send(self.dict)
            
def process_message(s):
        command = s.split(' ')
        while True:
            try:
                command.remove('')
            except ValueError:
                break
        return command

if __name__ == '__main__':
    print('Loading')
    list_conn, client_list = Pipe()   # List to Client
    main_l_conn, list_TCP_conn = Pipe() # List to Main
    main_So_conn, TCP_conn = Pipe() # Main to Socket_Server
    main_conn, client_conn = Pipe() # Main to client
    tcp_p = serverTCP(TCP_conn, client_conn, client_list)
    up_ir_p = list_IRDevices(list_conn, list_TCP_conn)
    up_ir_p.start()
    tcp_p.start()
    dlist = {}
    print('Loaded')
    while True:
        while main_So_conn.poll():
            b = main_So_conn.recv()
            print("New client:", b)
        while main_l_conn.poll():
            dlist = main_l_conn.recv()
        while main_conn.poll():
            a = main_conn.recv()
            print(a)
        if dlist != {}:
            print(dlist)
            usr_r = input("msg: ")
            if usr_r == '':
                b = main_conn.recv()
                print(b)
            else:
                c = process_message(usr_r)
                main_conn.send(c)
                wait((main_conn,))
    
