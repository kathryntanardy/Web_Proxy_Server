import socket
import threading

cache = {}

def client_request(clientSocket):
    request = clientSocket.recv(1024).decode()
    
    request_split = request.split('\r\n')
    request_line = request_split[0]
    print(request_line)
    

    # Check if in cache
    if request in cache:
        print('Cache Hit!\n')
        clientSocket.send(cache[request].encode())

    else:
        print('Cache Miss!\n')
        
        clientSocketOrigin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocketOrigin.connect(('127.0.0.1', 1200))
        clientSocketOrigin.send(request.encode())
        replyFromOrigin = clientSocketOrigin.recv(1024).decode()

        cache[request] = replyFromOrigin
        
        clientSocket.sendall(replyFromOrigin.encode())
        clientSocketOrigin.close()
    
    clientSocket.close()


def initiate_proxy():
    serverPort = 8080
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen(5)
    print(f"Proxy server is running.")

    while True:
        (clientSocket, address) = serverSocket.accept()
        thread = threading.Thread(target=client_request, args=(clientSocket,))
        thread.start()

if __name__ == '__main__':
    initiate_proxy()