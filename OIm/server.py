# used for the main communication part
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = "0.0.0.0"   # need to change to ipv6 
PORT = 5000  #can change
LISTEN_LIMIT = 5

current_clients = [] # all the current connected clients
chatlog = []


# Client function
# Client = socket client
def client_handle(client):
    while 1:

        # 2048 max size of message 
        # data sent in bit form utf just changes it to english

        username = client.recv(2048).decode('utf-8')
        if username != ' ':
            current_clients.append((username, client))
            newUser = "SERVER ~" +f"{username} has joined the chat"
            send_messages_to_all(newUser)
            
            break
        else:
            print("client username is empty")

    threading.Thread(target= listen_for_messages, args=(client,username, )).start()

# Server message to all clients  
def send_messages_to_all(message):

    for user in current_clients:
        send_msg_client(user[1], message)

# Send message to indivdiual 
def send_msg_client(client, message):

    # sends the encoded message
    client.sendall(message.encode())

# Listening for messages from client
# If not empty will create a message and send to all the clients connected
def listen_for_messages(client, username):
    while 1:
        response = client.recv(2048).decode('utf-8')
        if response != '':
            final_msg = username + '~' + response
            send_messages_to_all(final_msg)
            chatlog.append(final_msg)
        else:
            print(f"The message from client {username} is empty") 


root = tk.tk()

root.title("SwiftChat Server Client")

root.resizable(False,False)

root

#    
def main():
    # creating a socket object
    # AF_INET = IPV4         Sock_stream = TCP protocol 
    # eventually change to ipv6
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    try:
        # bind needs a tuple which has the host address and port number  
        server.bind((HOST,PORT))
        print(f"Running server on {HOST} {PORT}")
    except:
        print("Cant bind " + HOST + " and port " + str(PORT))


    # listening server limit
    server.listen(LISTEN_LIMIT)


    # infity loop to listen for client connection 
    while 1:

        # client = socket of client
        # address = address of client

        client, address = server.accept()
        # address 0 = ip address     address 1 = port
        print(f"connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handle, args=(client, )).start()

if __name__ == '__main__':
    main()