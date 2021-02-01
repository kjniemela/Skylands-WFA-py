import socket
import sys
from _thread import *

#HOST = socket.gethostname()
HOST = 'localhost'
#HOST = '192.168.1.9'
PORT = 8080 # Arbitrary non-privileged port
servername = 'server'

stop = True
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')
 
#Bind socket to local host and port
##try:
s.bind((HOST, PORT))
##except socket.error(msg):
##    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
##    sys.exit()
     
print('Socket bind complete')
print('IP: ' + socket.gethostbyname(HOST) + ':' + str(PORT))
#UDP server responds to broadcast packets
#you can have more than one instance of these running
address = ('', PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(address)
server_socket.settimeout(5.0)

#Start listening on socket
s.listen(10)
print('Socket now listening')
##players = {}
##playerID = []
##playerconn = {}
##playerdata = {}
##autotasks = {}
connections = []

players = []
playerconn = []
playerdata = []

def convert_ints(ints):
    r = b''
    for i in ints:
        r += bytes([(i+32768)//256, (i+32768)%256])
    return r
def convert_bytes(s):
    r = []
    for i in range(0, len(s), 2):
        try:
            a = s[i]
            b = s[i+1]
            r.append(((a*256)+b)-32768)
        except IndexError:
            r.append(s[i])
    return r
def Send(conn, ctr, ints8=[], ints16=[]):
    global players
    try :
        m = bytes([ctr])
        if len(ints8) > 0:
            try:
                m += bytes(ints8)
            except ValueError:
                m += convert_ints(ints8)
        if len(ints16) > 0:
            m += convert_ints(ints16)
        conn.send(bytes([len(m)])+m)
    except ConnectionResetError:
        print('Error 10054: Connection Reset')
        leave(conn, [players[conn]])
        conn.close()
    except OSError:
        print('Error 10038: OS Error')
def SendToAll(message):
    global connections
    print(message)
    for i in range(len(connections)):
        Send(connections[i], message)
def add_player(conn, player):
    global players
    global playerconn
    global playerdata

    i = 0
    for p in players:
        if p == None:    
            players[i] = player
            playerconn[i] = conn
            playerdata[i] = [0, 0, 0]
            return i
        i += 1
    
    players.append(player)
    playerconn.append(conn)
    playerdata.append([0, 0])
    return len(players)-1
def clientthread(conn):
    global stop
    global players
    global playerconn
    global playerdata
        
    #Send(conn, 1, [123, 456])
    ton = 0
    ID = -1

    while ton == 0 and stop:    
        try:
            size = conn.recv(1)[0]
            rec = conn.recv(size)
        except ConnectionResetError:
            print('Error 10054: Connection Reset')
            conn.close()
            break
        except OSError:
            print('Error 10038: OS Error')
            break
        
        ctr = rec[0]#0: update pos - 1: set username - 2: close socket
        data = []
        if ctr == 0:
            data = convert_bytes(rec[1:])
            playerdata[ID] = data
            m = bytes([0])
            for i in range(len(playerdata)):
                if not i == ID and not players[i] == None:
                    m += bytes([i])
                    m += convert_ints(playerdata[i])
            conn.send(bytes([len(m)])+m)
        elif ctr == 1:
            data = [rec[1:].decode()] 
            ID = add_player(conn, data[0])
            Send(conn, 1, ints8=[ID])
        else:
            Send(conn, 2)

        #Send(conn, 0, [123, 456])
        if not rec or ctr == 2: 
            break

    players[ID] = None
    conn.close()
 
#now keep talking with the client
while stop:
    server_socket.settimeout(1.0)
    try:
        recv_data, addr = server_socket.recvfrom(4096)
        print(addr,':',recv_data.decode('utf-16'))
        server_socket.sendto(servername.encode('utf-16'), addr)
    except socket.timeout:
        pass
    
    #wait to accept a connection - blocking call
    s.settimeout(1.0)
    try:
        conn, addr = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,))
        connections.append(conn)
    except socket.timeout:
        pass
        
s.close()
