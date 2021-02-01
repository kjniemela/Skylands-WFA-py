from random import *
from time import sleep
import socket   #for sockets
import sys  #for exit
import time

def recv_timeout(the_socket,timeout=0.1):
    #make socket non blocking
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data=[];
    data='';
     
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(8192).decode('utf-16')
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(total_data)

class Game():
    def convert_ints(self, ints):
        r = b''
        for i in ints:
            r += bytes([(i+32768)//256, (i+32768)%256])
        return r
    def convert_bytes(self, s):
        r = []
        for i in range(0, len(s), 2):
            try:
                a = s[i]
                b = s[i+1]
                r.append(((a*256)+b)-32768)
            except IndexError:
                r.append(s[i])
        return r
    
    def Send(self, ctr, ints8=[], ints16=[], s="", p=False):
        try :
            m = bytes([ctr])
            if len(ints8) > 0:
                try:
                    m += bytes(ints8)
                except ValueError:
                    m += self.convert_ints(ints8)
            if len(ints16) > 0:
                m += self.convert_ints(ints16)
            if not s == "":
                m += s.encode()
            self.s.send(bytes([len(m)])+m)
        except socket.error:
            print('Send failed')

        self.Recv(p)
        
    def Recv(self, p=False):
        #self.s.settimeout(0.5)
        reply = None
        try:
            size = self.s.recv(1)[0]
            rec = self.s.recv(size)
            ctr = rec[0]#0: update pos - 1: assign ID -
            if ctr == 0:
                for i in range(1, len(rec[1:]), 7):
                    self.playerdata[rec[i]] = self.convert_bytes(rec[i+1:i+7])
                data = self.convert_bytes(rec[1:])
                if p:
                    print(ctr, self.playerdata)
            elif ctr == 1:
                self.player = rec[1]
        except socket.timeout:
            pass
        
    def __init__(self, IP, username):
        self.name = username
        self.isOn = True
        self.player = 0
        self.playerdata = {}
        self.players = []
        self.messages = []
        self.ship = None
        self.world = None
        self.gui = None
        self.log = ['Log Start']
        
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error(msg):
            print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
            sys.exit();
         
        print('Socket Created')
        host = IP
        if host == '' or host == 'localhost':
            host = 'localhost:8080'
        host, port = host.split(':')
        port = int(port)

         
        try:
            remote_ip = socket.gethostbyname(host)
         
        except socket.gaierror:
            #could not resolve
            print('Hostname could not be resolved. Exiting')
            sys.exit()
             
        print('Ip address of ' + host + ' is ' + remote_ip)
        #Connect to remote server
        try:
            self.s.connect((remote_ip , port))
        except ConnectionRefusedError:
            print('No server on this network!')
        print('Socket Connected to ' + host + ' on ip ' + remote_ip)
        self.Send(1, s=username)
    def setShip(self, ship):
        self.ship = ship
    def setWorld(self, world):
        self.world = world
    def setGUI(self, gui):
        self.gui = gui
    def leave(self, event=None):
        self.Send(2)
        self.isOn = False
    def tick(self):
        #self.SendMessage('\ufeff'.join(self.messages))
        self.messages = []
