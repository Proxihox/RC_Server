import subprocess
import sys
import signal

default_handler = None
file1 = "server.py"
file2 = "reverseCoding.out"

def handler(num, frame):
    p1.kill()
    p2.kill()
    default_handler(num,frame)

p1 = subprocess.Popen(
    ["python3",file1],
    stdin=subprocess.PIPE,   # Pipe for input to C++ program
    stdout=subprocess.PIPE,  # Pipe for output from C++ program
    stderr=subprocess.PIPE,  # Pipe for error messages
    text=True                # Ensures input/output are handled as text (not bytes)
)
p2 = subprocess.Popen(
    # ["./reverseCoding"],           # Path to the compiled C++ executable
    ["python3","reverseCoding.py"],
    stdin=subprocess.PIPE,   # Pipe for input to C++ program
    stdout=subprocess.PIPE,  # Pipe for output from C++ program
    stderr=subprocess.PIPE,  # Pipe for error messages
    text=True                # Ensures input/output are handled as text (not bytes)
)


if __name__ == "__main__":
    default_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, handler)
    x = 1
    y = 2
    while(True):
        out1 = p1.stdout.readline().strip()
        if(out1 == ""):
            out1 = str(x) + " " +str(y)
        print("in:",out1)
        # out2,err2 = p2.communicate(out1)
        # print("out:",out2,"err:",err2)
        # p1.stdin.write(out2)
        # #p1.stdin.flush()
        # x += 1
        # y += 1

        p2.stdin.write(out1)
        p2.stdin.flush()  # Ensure input is sent immediately
        in1 = out2 = p2.stdout.readline().strip()

        p1.stdin.write(in1)
        p1.stdin.flush()  # Ensure input is sent immediately



