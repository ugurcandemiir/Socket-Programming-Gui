
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import json
import os

def accept_connections():

    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Welcome to the Remote Quiz App! Now type your name and press enter!", "utf8"))
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(buffer_size).decode("utf8")
    welcome = ('\n \nWelcome %s! If you ever want to quit, type {quit} to exit. ' % name + " \n"
    + "You have 60 seconds for answering each question ! \n \n")
    client.send(bytes(welcome, "utf8"))
    grades = 0
    number_of_question = 1
    while True:
        try:
            tmp = " "
            for k,v in questions[number_of_question].items():
                if k == "question" or k=="content":
                    tmp = tmp +(str(k)+ "  "+ str(number_of_question) +': '  + str(v)) + '\n'

                else:
                    tmp = tmp+'\t' + (str(k)+': '  + str(v)) + '\n'
            client.send(bytes(tmp, "utf8"))
            answer = client.recv(buffer_size).decode("utf8")
            if answer != "":
                print("%s says: " %name,"%s "%answer,"for question : %s " %number_of_question ,"total grades : %s" %grades)
                if answer == answers[number_of_question]:
                    grades += 3
                else:
                    grades += 0


        except:
            try:
                finish_message = "\nTest is finished!\nYour Result is showing on the screen. You can close the window ! \n "
                point_message = "Points from test: %s" % grades
                client.send(bytes(point_message+finish_message,"utf-8"))
                print("%s Total Points: " %name,"%s "%grades )
                client.close()
                break
            except:
                interrupted = "%s  interrupted itself" %name
                print(interrupted)
                exit(1)
        number_of_question += 1

HOST = ''
PORT = 33000
buffer_size = 1024
ADDR = (HOST, PORT)

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)
# Opening JSON file
f = open('ServerCode_data_questions.json',)
# returns JSON object as a dictionary
data = json.load(f)
tmp_data = data.copy()
index = 1
questions ={}
answers ={}
for i in tmp_data:
    answers[index] = i.get("answer")
    i.pop("answer")
    questions[index] = i
    index = index+1
f.close()


if __name__ == "__main__":
    server.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()
