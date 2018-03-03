#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""

import tkinter

from chatclientlibrary import *

msg_list = None

# We'll set this up to be called by our ChatClient on every message
# It just pokes the message into our user interface
def uiOnMessage(msg):
    msg_list.insert(tkinter.END, msg)
    msg_list.yview(tkinter.END) # scroll to end

def initUI(chatClient):
    global msg_list
    
    top = tkinter.Tk()
    top.title("Chatter")
    
    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    my_msg.set("")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()
    
    def uiDoSend(event=None):
        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        chatClient.send(msg)
    
    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", uiDoSend)
    entry_field.pack()
    entry_field.focus()
    send_button = tkinter.Button(top, text="Send", command=uiDoSend)
    send_button.pack()

    def on_closing(event=None):
        """This function is to be called when the window is closed."""
        print("client is closing\n")
        chatClient.send("{quit}")
        top.quit()
    top.protocol("WM_DELETE_WINDOW", on_closing)




if __name__ == '__main__':
    
    chatClient = ChatClient()
    
    # This is the code running when you run this file directly
    print("Start of main code")
    initUI(chatClient)
    
    #----Now comes the sockets part----
    #HOST = input('Enter host: ')
    #PORT = input('Enter port: ')
    HOST = 'localhost'
    PORT = '33000'
    
    chatClient.connect(HOST, PORT, uiOnMessage)
    
    tkinter.mainloop()  # Starts GUI execution.
    print("End of main code")
