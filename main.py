from socket import *
import threading
import os




def thread_function(clientsocket):
    request = clientsocket.recv(1024).decode()
    print(request)
    syntax = True #400 error
    request = request.split('\r\n')
    request_line = request[0]

    request_line_split = request_line.split(' ')
    if(len(request_line_split) >= 3):
        method = request_line_split[0]
        target_resource = request_line_split[1]
        target_resource = target_resource[1::]
        http_ver = request_line_split[2]
        if http_ver != 'HTTP/1.1':
            syntax = False
    else:
        syntax = False
    
    if (method == 'GET'):
        try:
            html_file = open(target_resource, "r")
            html_body = html_file.read()
           
            response = 'HTTP/1.1 200 OK\r\n'
            response += 'Content-Type: text/html; charset=UTF-8\r\n'
            response += f"Content-Length: {len(html_body)}\r\n"
            response += html_body
            print(response)
        except FileNotFoundError:
            print("blablabla")
            return 

    return

def main():
    serverPort = 8080
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', serverPort))
    serverSocket.listen(5)
    print("The Server is Ready to Receive")

    while True:
        (clientsocket, address) = serverSocket.accept()
        client_thread = threading.Thread(target=thread_function, args=(clientsocket,))
        client_thread.start()


if __name__ == '__main__':
    main()