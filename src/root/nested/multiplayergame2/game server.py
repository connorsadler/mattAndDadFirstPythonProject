#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading
import time
import random
from netutils import *

clients = {}
addresses = {}
HOST = ''
PORT = 33000
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

nextClientId = 1

def accept_incoming_connections():
    global nextClientId
    
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        
        client.send(bytes("Welcome to ... chatroom!\n"+
                          "Now type your name and press enter!", "utf8"))

        print("The client is clientId: " + str(nextClientId))
        client.send(bytes("MINECRAFT: YOURCLIENTID: " + str(nextClientId), "utf8"))
        nextClientId += 1
        
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    firstMessageFromClient = client.recv(BUFSIZ_FIRSTMESSAGE).decode("utf8")
    name = firstMessageFromClient.rstrip() # Trim trailing spaces
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    broadcast("%s has joined the chat!" % name)
    clients[client] = name
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            # Normal message from client
            handleMessageFromClient(name)
            broadcast(msg, name+": ")
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

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    print('message broadcast: ', msg)
    for sock in clients:
        # if msg is a string then we turn it into bytes
        msgBytes = msg
        if isinstance(msgBytes, str):
            msgBytes = bytes(msgBytes, "utf8")
        # msg will now be bytes
        try:
            sock.send(bytes(prefix, "utf8") + msgBytes)
        except ConnectionResetError:
            print("ConnectionResetError - skipping this client")


class MiThread(threading.Thread):   
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            global clients
            print("Background thread checking server status")
            print("  client count: " + str(len(clients)))
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
    t = MiThread()     
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    t.start()    
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    
    ACCEPT_THREAD.join()
    SERVER.close()





