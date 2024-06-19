from socket import *
import threading
import os
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

def modifiable_files(path):
    restricted_dir = "restricted/"
    return not path.startswith(restricted_dir)

def thread_function(clientsocket):
    request = clientsocket.recv(1024).decode()

    wrong_syntax = False #400 error
    file_not_found_error = False #404 error
    request_split = request.split('\r\n')

    request_line = request_split[0]
    print(request_line, '\n')
    request_line_split = request_line.split(' ')

    # Check if request line have 3 or more fields
    if(len(request_line_split) >= 3):
        method = request_line_split[0]
        target_resource = request_line_split[1]
        target_resource = target_resource[1::]
        http_ver = request_line_split[2]
        if http_ver != 'HTTP/1.1':
            wrong_syntax = True

    #If the request line is not valid: 400 error     
    else: 
        wrong_syntax = True
        
    print("REQUEST")
    print("-----------------")
    print(request)

    # Check if there's "If-Modified-Since" header
    have_modified_since_header = False
    for header in request_split:
        if header.startswith("If-Modified-Since:"):
            have_modified_since_header = True
            condition_time = header.split(":", 1)
            condition_time = condition_time[1].strip()
            break

    if (method == 'GET'):
        try:
            if target_resource == "favicon.ico":
                return
            else:
                # Check if there's a "If-Modified-Since" header
                if have_modified_since_header:
                    # Get HTML file last modified time
                    file_modified_time = os.path.getmtime(target_resource)
                    file_modified_time_dt = datetime.fromtimestamp(file_modified_time)

                    # Compare if modified condition passes or not
                    condition_time_dt = datetime.strptime(condition_time, '%a, %d %b %Y %H:%M:%S GMT')

                    #TODO: HELP ME
                    condition_time_dt = condition_time_dt.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None) 

                    if file_modified_time_dt <= condition_time_dt:
                        response = 'HTTP/1.1 304 Not Modified\r\n'
                        clientsocket.sendall(response.encode())
                
                # Read the html file
                html_file = open(target_resource, "r")
                html_body = html_file.read()

                # Create and send response
                response = 'HTTP/1.1 200 OK\r\n'
                response += '\r\n'
                response += html_body
                clientsocket.sendall(response.encode())

        except FileNotFoundError:
            print("HELLO")
            file_not_found_error = True


    elif(method == 'DELETE'):
        try:
            os.remove(target_resource)
            response = "HTTP/1.1 204 No Content\r\n"
            clientsocket.sendall(response.encode())
        except FileNotFoundError:
            file_not_found_error = True
        except Exception as e:
            response_header = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
            clientsocket.sendall(response_header.encode())
    

    elif(method == 'PUT'):
        if not modifiable_files(target_resource):
            response =  "HTTP/1.1 403 Forbidden\r\n" 
            clientsocket.sendall(response.encode())
        else:
            try:
                if os.path.exists(target_resource):
                    with open(file_path, 'w') as file:
                    file.write(target_resource)
                    response_header = "HTTP/1.1 200 OK\r\n\r\n"
                else:
                    with open(target_resource, 'w') as file:
                        file.write(request_body)
                        response_header = (
                        "HTTP/1.1 201 Created\r\n"
                        "Location: {}\r\n\r\n"
                     ).format(path)
                    client_socket.sendall(response_header.encode())
                except Exception as e:
                    response_header = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
                        client_socket.sendall(response_header.encode())
   
        
    # 404 error
    if(file_not_found_error):
        response = 'HTTP/1.1 404 Not Found\r\n'
        clientsocket.sendall(response.encode())
    elif(wrong_syntax):
        response = 'HTTP/1.1 400 Bad Request'
        clientsocket.sendall(response.encode())
        
    clientsocket.close()


def main():
    serverPort = 1200
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