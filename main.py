from socket import *
import threading 

def thread_function(clientsocket):
    request = clientsocket.recv(1024)
    print(request)

    return

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen(5)
    print("The Server is Ready to Receive")

    while True:
        (clientsocket, address) = serverSocket.accept()
        client_thread = threading.Thread(target=thread_function, args=(clientsocket,))
        client_thread.start()


if __name__ == '__main__':
    main()