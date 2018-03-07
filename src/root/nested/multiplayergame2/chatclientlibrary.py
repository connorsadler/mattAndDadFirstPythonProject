from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from netutils import *

class ChatClient():
    def __init__(self):
        print("ChatClient is being constructed\n")
        self.client_socket = None
        self.receive_thread = None
    
    def connect(self, HOST, PORT, onMessageCallback, onQuitCallback):
        if not PORT:
            PORT = 33000
        else:
            PORT = int(PORT)
        
        ADDR = (HOST, PORT)

        # onMessageCallback is a function which will be called on every message we receive e.g. to update user interface
        self.onMessageCallback = onMessageCallback
        self.onQuitCallback = onQuitCallback
        
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)
        
        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()
    
    def getClientId(self):
        # takes the tuple of the client socket (e.g. ('127.0.0.1', 55767) )
        # and grabs just the local port
        return str(self.client_socket.getsockname()[1])
    
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(BUFSIZ).decode("utf8")
                self.onMessageCallback(msg)
            except OSError:  # Possibly client has left the chat.
                break

    # Handles sending of messages
    # Optionally pads the message to a certain length
    # event is passed by binders
    def send(self, msg, padToLength = -1):
        print("ChatClient sending: " + msg)
        if padToLength > 0:
            msg2 = msg.ljust(padToLength)
        else:
            msg2 = msg.ljust(BUFSIZ)
            
        #         msg += EOM
        
        self.client_socket.send(bytes(msg2, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()
            self.onQuitCallback()




