import socket
import select
import sys
import time
import pickle
import os
import threading
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer

model = pickle.load(open("C:\\Users\\neema\\Downloads\\anti cyberbully chat\\anti cyberbully chat\\Safe_Chat\\LinearSVC.pkl", 'rb'))
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_address = "192.168.31.146"
port = 58306

server.connect((IP_address, port))
print("Connected To server")

user_id = input("Type user id: ")
room_id = input("Type room id: ")

server.send(str.encode(user_id))
time.sleep(0.1)
server.send(str.encode(room_id))

def prettyPrinter(data_1):
    my_file = open("C:\\Users\\neema\\Downloads\\anti cyberbully chat\\anti cyberbully chat\\Safe_Chat\\stopwords.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    tfidf_vector =  TfidfVectorizer(stop_words = content_list, lowercase = True,vocabulary=pickle.load(open("C:\\Users\\neema\\Downloads\\anti cyberbully chat\\anti cyberbully chat\\Safe_Chat\\tfidf_vector_vocabulary.pkl", "rb")))
    data_2=tfidf_vector.fit_transform([data_1])
    print(data_2)
    pred = model.predict(data_2)
    print(pred)
    if pred==0:
        print('Non bullying')
        return pred
    else: 
        print("Bullying message detected it has been hidden")
        return pred

def handle_user_input():
    while True:
        message = input()
        if message == "FILE":
            file_name = input("Enter the file name : ")
            server.send("FILE".encode())
            time.sleep(0.1)
            server.send(str("client_" + file_name).encode())
            time.sleep(0.1)
            server.send(str(os.path.getsize(file_name)).encode())
            time.sleep(0.1)

            file = open(file_name, "rb")
            data = file.read(1024)
            while data:
                server.send(data)
                data = file.read(1024)
            print("<You> File sent successfully")
        else:
            pred = prettyPrinter(message)
            if pred == 0:
                server.send(message.encode())
                print("<You> " + message)
            else:
                print("Bullying message detected it has been hidden")

threading.Thread(target=handle_user_input).start()

while True:
    read_socket, write_socket, error_socket = select.select([server], [], [])

    for socks in read_socket:
        message = socks.recv(1024)
        print(str(message.decode()))

        if str(message.decode()) == "FILE":
            file_name = socks.recv(1024).decode()
            lenOfFile = socks.recv(1024).decode()
            send_user = socks.recv(1024).decode()

            if os.path.exists(file_name):
                os.remove(file_name)

            print(file_name, lenOfFile, send_user)

            total = 0
            with open(file_name, 'wb') as file:
                while str(total) != lenOfFile:
                    data = socks.recv(1024)
                    total = total + len(data)     
                    file.write(data)
            print("<" + str(send_user) + "> " + file_name + " sent")
        else:
            pred = prettyPrinter(str(message.decode()))
            if pred == 0:
                print(message.decode())
            else:
                print("Bullying message detected it has been hidden")

server.close()