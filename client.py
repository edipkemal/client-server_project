import socket                
import sys
from sys import stdin
from _thread import*

host = "localhost"
port = 1026

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
except socket.error as msg:
    print("[Server inactive] Message:", msg)
    sys.exit()
    
username=input("Username: ")

s.send(username.encode())

while 1:
    permission=s.recv(2048).decode("utf-8")
    if permission=="bid":
        message=input("Enter your bid -> ")
        s.send(message.encode())
        if  int(message)<0:
            print("Good bye..")
            break
        print("Please wait until everyone makes his/her bid.")
    else:
        data=s.recv(2048).decode("utf-8")
        print(data)
        if data=="All items are sold. Public auction is finished.":
            break

s.close() 
