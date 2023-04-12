from tkinter import *
import socket


client = socket.socket()
client.connect(('localhost', 9898))

def handle(fd, mask):
    msg = client.recv(1024)
    text.insert(END, msg.decode('utf-8'))
    text.see(END)

def send_msg(event):
    msg = message_entry.get() + "\n"
    message_entry.delete(0, END)
    client.send(bytes(msg.encode()))

root = Tk()
root.title("PUM Chat")
root.geometry("300x250")
message_entry = Entry(width=90)
text = Text(root, height=15, width=90)
text.pack()
message_entry.pack()
root.bind("<Return>", send_msg)

fileno = client.fileno()
root.tk.createfilehandler(fileno, READABLE, handle)

root.mainloop()