#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import time
import socket

def receive():
    global before
    while True:
        try:
            questions = client_socket.recv(buffer_size).decode("utf8")
            before = time.time()
            questions_list.insert(tkinter.END, questions)
            questions_list.see(tkinter.END)
        except OSError:
            break


def send(event=None):
    """Handles sending of messages."""
    msg = my_msg.get()
    msg = msg.lower()
    if time.time() - before > 60:
        questions_list.insert(tkinter.END, "60 seconds passed you got 0 points from this question \n",'warning')
        msg = "not possible answer given by user"
    if not msg:
        msg = "No message"
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "\nTest is finished!\nYour Result is showing the screen. You can close the window ! \n ":
        #client_socket.close()
        on_closing()
    if msg == "{quit}":
        #client_socket.close()
        on_closing()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    client_socket.close()
    top.quit()

top = tkinter.Tk()
top.title("Remote Quiz App")
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your answers here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

questions_list =tkinter.Text(messages_frame,height=55, width=80,yscrollcommand=scrollbar.set)
questions_list.tag_config('warning', background="yellow", foreground="red")
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
questions_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
questions_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)


#-- sockets part----

buffer_size = 1024
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 33000
ADDR = (HOST, PORT)


client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
