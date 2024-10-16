import socket
import threading

HEADER = 64
PORT = 5050
# SERVER = ""
# Another way to get the local IP address automatically
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
NPROB = 3

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def log(logstr):
    with open("./log/logs.txt","a") as f:
        f.write(logstr)
    

def handle_client(conn, addr):
    with open("./log/log_{addr}.txt",'a') as f:
        f.write(f"[NEW CONNECTION] {addr} connected.")
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT).strip()
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                try:
                    resp = str(reverseCoding(msg))
                except Exception as e:
                    resp = str(e)
                f.write(f"[{addr}] {msg} -> {resp}")
                log(f"[{addr}] {msg} -> {resp}")
                conn.send(resp.encode(FORMAT))
    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def reverseCoding(inp):

    a,b = map(int,inp.split(' '))
    return a+b

start()