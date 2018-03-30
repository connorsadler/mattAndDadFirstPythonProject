#!/usr/bin/env python3

#
# Server for multithreaded (asynchronous) chat application
# 

from socket import AF_INET, socket, SOCK_STREAM

from threading import Thread
import threading
import time
import random
import sys
from netutils import *
from debug import DEBUG

clients = {}
addresses = {}
HOST = ''
PORT = 33000
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

import socket as sock
serverIP = sock.gethostbyname_ex(sock.gethostname())
print("Server running on: " + str(serverIP))

def printex(msg):
    threadName = threading.currentThread().name
    print(threadName + " - " + msg)

class ServerBackgroundAcceptClientConnectionsThread(threading.Thread):
    def __init__(self):
        self.nextClientId = 1
        threading.Thread.__init__(self)
    
    def run(self):
        threading.currentThread().name = "[ServerBackgroundAcceptClientConnectionsThread]"
        self.accept_incoming_connections()
        
    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = SERVER.accept()
            print("%s:%s has connected." % client_address)
            
            client.send(bytes("Welcome one".ljust(BUFSIZ), "utf8"))
            client.send(bytes("Welcome two".ljust(BUFSIZ), "utf8"))
            client.send(bytes("Welcome three".ljust(BUFSIZ), "utf8"))
            client.send(bytes("Welcome to ... chatroom!".ljust(BUFSIZ), "utf8"))
            client.send(bytes("Now type your name and press enter!".ljust(BUFSIZ), "utf8"))
    
            print("The client is clientId: " + str(self.nextClientId))
            client.send(bytes("MINECRAFT: YOURCLIENTID: " + str(self.nextClientId), "utf8"))
            self.nextClientId += 1
            
            addresses[client] = client_address
            Thread(target=handle_client, args=(client,)).start()

#
# Handles a single client connection
# Runs in a separate thread
# Takes client socket as argument.
#
def handle_client(client):
    firstMessageFromClient = client.recv(BUFSIZ_FIRSTMESSAGE).decode("utf8")
    name = firstMessageFromClient.rstrip() # Trim trailing spaces
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    
    broadcast("%s has joined the chat!" % name)
    clients[client] = name
    threading.currentThread().name = "[Thread for Client: " + name + "]"
    
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            # Normal message from client
            # 1 - send it to our game logic code
            handleMessageFromClient(name)
            # 2 - send it to all clients
            broadcast(msg.ljust(BUFSIZ), name + ": ")
        else:
            # QUIT message
            try:
                client.send(bytes("{quit}", "utf8"))
            except ConnectionResetError:
                print("send to client failed - ignoring")
            client.close()
            del clients[client]
            broadcast("%s has left the chat." % name)
            break

lock = threading.Lock()

#
# Broadcasts a message to all the clients
# prefix is for name identification.
#
def broadcast(msg, prefix=""):  
    threadName = threading.currentThread().name
    if DEBUG:
        print(threadName + ' >>> broadcast: ', msg)

    # prevent multiple client processing threads broadcasting at the same time
    with lock:
        # if msg is a string then we turn it into bytes
        msgBytes = msg
        if isinstance(msgBytes, str):
            msgBytes = bytes(msgBytes, "utf8")
        # msg will now be bytes
        
        # send to all clients
        for sock in clients:
            try:
                sock.send(bytes(prefix, "utf8") + msgBytes)
            except ConnectionResetError:
                print("ConnectionResetError - skipping this client")
    
    if DEBUG:
        print(threadName + ' <<< broadcast: ', msg)

#
# Server background game logic thread
# Any server side game logic runs in this thread
#
class ServerBackgroundGameLogicThread(threading.Thread):   
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        threading.currentThread().name = "[ServerBackgroundGameLogicThread]"
        while True:
            global clients
            printex("Background thread checking server status")
            printex("  client count: " + str(len(clients)))
            broadcast("Server is still running - hi there")
            serverTick()
            time.sleep(5)
    
#
# Game logic
#

# dict of "name" (player name, string) -> score (integer)
scores = {}

def addOneToScoreForPlayer(name):
    if name in scores:
        scoreForThisPlayer = scores[name]
    else:
        scoreForThisPlayer = 0
    scoreForThisPlayer += 1
    scores[name] = scoreForThisPlayer

# Any message from any client comes in here
def handleMessageFromClient(name):
    #print("handleMessageFromClient, name: " + name + "\n")
    #print("randomWord: " + randomWord + "\n")
    #addOneToScoreForPlayer(name)
    #broadcast(name + ", you scored a point, well done")
    if False:
        print("Dummy code")

# the current word the players need to guess
randomWord = "none"
mylist = ['hello', 'body', 'zombie', 'toilet', 'flush', 'world', 'cheese' ]

# Called by server code every 5 seconds
def serverTick():
    # allow write access to our global variable to store the current word the players need to guess
    global randomWord 

    # tell players the current scores
    broadcastScores()

    # choose a new random word from the list
    wordIndex = random.randint(0, len(mylist)-1)
    randomWord = mylist[wordIndex]
    # tell players the new word
#     broadcast("Please type the word: " + randomWord)
    
def broadcastScores():
    scoresString = ""
    for name in scores.keys():
        scoresString += ", " + name + ": " + str(scores[name])
    broadcast(bytes("Scores: " + scoresString, "utf-8"))

        
#    
# If you run this file directly, this is the code that will execute
#
if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    t = ServerBackgroundGameLogicThread()     
    ACCEPT_THREAD = ServerBackgroundAcceptClientConnectionsThread()
    t.start()
    ACCEPT_THREAD.start()
    
    ACCEPT_THREAD.join()
    SERVER.close()





