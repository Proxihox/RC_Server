import socket
import threading
import subprocess
import signal

HEADER = 64
PORT = 65432
# SERVER = ""
# Another way to get the local IP address automatically
SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)
print(ADDR)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
NPROB = 3
LOGS = True

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

default_handler = None

def log(logstr):
    with open("./log/logs.txt","a") as f:
        f.write(logstr)

def handler(num, frame):
    default_handler(num,frame)

def handle_client(conn, addr):
    
    rc = subprocess.Popen(
        # ["./reverseCoding"],           # Path to the compiled C++ executable
        ["python3","reverseCoding.py"],
        stdin=subprocess.PIPE,   # Pipe for input to C++ program
        stdout=subprocess.PIPE,  # Pipe for output from C++ program
        stderr=subprocess.PIPE,  # Pipe for error messages
        text=True                # Ensures input/output are handled as text (not bytes)
    )
    with open("./log/log_"+str(addr)+".txt",'w') as f:
        if(LOGS):
            f.write(f"[NEW CONNECTION] {addr} connected.")
            f.flush()
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                #resp,err = rc.communicate(msg)
                if(LOGS):
                    f.write(f"Recv: {msg}")
                    f.flush()
                rc.stdin.write(msg+"\n")
                rc.stdin.flush()
                resp = rc.stdout.readline().strip()
                rc.stdout.flush()
                if(LOGS):
                    f.write(f"-> {resp}")
                    f.flush()
                print(f"{resp}")
                conn.send(resp.encode(FORMAT))
    rc.stdin.close()
    rc.stdout.close()
    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()