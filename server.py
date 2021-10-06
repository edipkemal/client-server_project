import socket
import sys
from _thread import*
import time
import random
users={}
max_bid=0
max_bidder="No one"
b="bid"
w="wait"
items=["Mona Lisa","The Scream","Starry Night","Girl With A Pearl Earring"]
bids=[]
bid_count=0
client_num=0
old_bid=0
item_index=0

def show_all_bidders(users):
    disp_info=""
    for user in users:
        disp_info+=user+" : "+str(users[user])+"$\n"
    return disp_info

def thread_job(c):
    global bid_count
    global bids
    global max_bid
    global max_bidder
    global client_num
    global old_bid
    global item_index
    global printed
    username=c.recv(2048).decode("utf-8")
    if username in users:
        c.send(w.encode())
        c.send("This user name already taken! Please connect again and choose a unique name.".encode("utf-8"))
        c.close()
        client_num-=1
        return 0

    users[username]=0
    c.send(w.encode("utf-8"))
    c.send("\nWelcome! We are making your registration..\nPlease wait until everyone registered.".encode("utf-8"))
    while client_num !=len(users): #wait until everyone join
        continue
    time.sleep(0.2)
    c.send(w.encode("utf-8"))
    c.send("All users are registered.\nPublic auction is starting..".encode("utf-8"))
    time.sleep(1)
    bidded=0

    while 1:
        if  bid_count==len(users): # everyone bidded
            c.send(w.encode("utf-8"))
            highest_bidder="\n"+show_all_bidders(users)+"#####\nHighest bidder is "+max_bidder+". His/Her bid is "+str(max_bid)+"\n#####"
            c.send(highest_bidder.encode("utf-8"))
            printed=0
            bid_count=0
            bidded=0
            bid_count=0
            time.sleep(0.2)
            if max_bid==old_bid: # no new bid, item sold
                c.send(w.encode("utf-8"))
                msg=items[int(round(item_index))]+" sold to "+max_bidder+" with "+str(max_bid)+"$"
                c.send(msg.encode("utf-8"))
                time.sleep(1)
                item_index+=1/client_num
                max_bid=0
                old_bid=0
                bids.clear()
                users[username]=0
            else:
                time.sleep(1)
                old_bid=max_bid            
            
        elif bidded==0: #this user did not bid this round, he will bid now
            if int(round(item_index))>len(items)-1:
                c.send(w.encode())
                c.send("All items are sold. Public auction is finished.".encode())
                users.pop(username)
                c.close()
                client_num-=1
                time.sleep(1)
                break
            time.sleep(0.2)
            c.send(w.encode("utf-8"))
            msg="\n**********\nCurrent item: "+items[int(round(item_index))]+"\nHighest bid: "+str(max_bid)+"$\n**********"
            c.send(msg.encode("utf-8"))
            time.sleep(0.2)
            c.send(b.encode("utf-8"))
            bid=c.recv(2048).decode("utf-8")
            bid=int(bid)
            if bid<0: #user exits
                users.pop(username)
                c.close()
                client_num-=1
                break
            max_bid=max(max_bid,bid)
            if bid==max_bid: #max bidder is this user
                max_bidder=username
            bids.append(bid)
            if bid>users[username]: #bid is bigger than this bidder's old bid
                users[username]=bid
            bid_count+=1
            bidded=1
    c.close()

def server():
    client_lim=5
    host = "localhost"
    port = 1026
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket Created")
    
        soc.bind((host, port)) 
        print("Socket connected to the port {}".format(port))
    
        soc.listen(client_lim)      
        print("Socket listening")
    except socket.error as msg:
        print("Error:",msg)
        
    while True: 
       c, addr = soc.accept()      
       print('Coming connection:', addr)
       start_new_thread(thread_job, (c,))
       global client_num
       client_num+=1
           
if __name__ == "__main__":
    sys.exit(server())   