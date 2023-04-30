import socket
import threading
import os
from datetime import datetime


# Function to handle connection request
def handle_request(client_connection):
    f = open("log_file.txt", 'a+')

    # Get the client request
    request = client_connection.recv(1024).decode()
    if len(request) == 0:
        client_connection.close()

    f.write('Client Request:  ')

    # Extract and parse HTTP headers, fields and request_type
    headers = request.split('\n')

    if len(headers) > 1:
        fields = headers[0].split()
        print(fields)
        request_type = fields[0]

        if len(fields) > 1:
            filename = fields[1]
            if filename == '/':
                filename = '.html'

            server_name = SERVER_HOST + ":" + str(SERVER_PORT)
            # Condition if "GET" as request type
            if request_type == 'HEAD' or 'GET':
                # Get the content of the file
                file_path = 'htdocs' + filename
                file_format = filename.split(".")
                file_supported = ['html', 'jpeg', 'jpg']

                # Get the last modified time
                if os.path.exists(file_path):

                    new_page_flag = True
                    last_modified_time = os.path.getmtime('htdocs' + filename)
                    last_modified_time_string = datetime.fromtimestamp(last_modified_time).strftime(
                        '%a, %d %b %Y %H:%M:%S GMT')

                    # Check If-Modified-Since is present in header
                    if 'If-Modified-Since:' in request:
                        if_modified_since_time = request.split('If-Modified-Since: ')[1].split('\r\n')[0]
                        if last_modified_time_string == if_modified_since_time:
                            new_page_flag = False

                    if file_format[1] in file_supported:

                        # Check if file is picture (format: jpeg/jpg)
                        if ".jpeg" in filename or ".jpg" in filename:
                            fin = open('htdocs' + filename, 'rb')
                            content = fin.read()
                            fin.close()
                            length = str(len(content)).encode()
                            time_now = str(datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')).encode()

                            if new_page_flag:
                                response_status = "HTTP/1.1 200 OK"
                            else:
                                response_status = "HTTP/1.1 304 Not Modified"

                            response_get = b'\r\n' + response_status.encode() + b'\r\n' + "Server: ".encode() + server_name.encode() + b'\r\n' + "Date: ".encode() + time_now + b'\r\nContent-Type: image/jpeg\r\nContent-Length: ' + length + b'\r\nCache-Control: public, max-age=3600\r\nLast-Modified: ' + last_modified_time_string.encode() + b'\r\n\r\n' + content
                            response_header = b'\r\n' + response_status.encode() + b'\r\n' + "\nServer: ".encode() + server_name.encode() + "Date: ".encode() + time_now + b'\r\nContent-Type: image/jpeg\r\nContent-Length: ' + length + b'\r\nCache-Control: public, max-age=3600\r\nLast-Modified: ' + last_modified_time_string.encode() + b'\r\n\r\n'

                            f.write(str(headers[1][:21]) + " Access Time: " + str(datetime.now().strftime(
                                '%a, %d %b %Y %H:%M:%S GMT')) + " Request Filename: " + filename + '\n')
                            f.write(
                                "Server Return: " + "http://" + server_name + '/' + file_path + ' ' + "Server Response: " + response_status + '\n')

                        else:
                            # Open file in embedded folder
                            fin = open('htdocs' + filename)
                            content = fin.read().encode()
                            fin.close()
                            length = str(len(content)).encode()
                            time_now = str(datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')).encode()

                            # Check if file has been modified
                            if new_page_flag:
                                response_status = "HTTP/1.1 200 OK"
                            else:
                                response_status = "HTTP/1.1 304 Not Modified"

                            response_get = b'\r\n' + response_status.encode() + b'\r\n' + "Server: ".encode() + server_name.encode() + b'\r\n' + "Date: ".encode() + time_now + b'\r\nContent-Type: text/html\r\nContent-Length: ' + length + b'\r\nConnection: Keep-Alive\r\nKeep-Alive: timeout=5, max=100\r\nCache-Control: public\r\nLast-Modified: ' + last_modified_time_string.encode() + b'\r\n\r\n' + content
                            response_header = b'\r\n' + response_status.encode() + b'\r\n' + "Server: ".encode() + server_name.encode() + b'\r\n' + "Date: ".encode() + time_now + b'\r\nContent-Type: text/html\r\nContent-Length: ' + length + b'\r\nConnection: Keep-Alive\r\nKeep-Alive: timeout=5, max=100\r\nCache-Control: public\r\nLast-Modified: ' + last_modified_time_string.encode() + b'\r\n\r\n'

                            f.write(str(headers[1][:21]) + " Access Time: " + str(datetime.now().strftime(
                                '%a, %d %b %Y %H:%M:%S GMT')) + " Request Filename: " + filename + '\n')
                            f.write(
                                "Server Return: " + "http://" + server_name + '/' + file_path + ' ' + "Server Response: " + response_status + '\n')

                        # Send response according to request type
                        if request_type == 'GET':
                            client_connection.sendall(response_get)

                        elif request_type == 'HEAD':
                            client_connection.sendall(response_header)

                    else:
                        response = b'\nHTTP/1.1 400 Bad Request\n\nRequest Not Supported'
                        f.write("Access Time: " + str(datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')) + '\n')
                        f.write("Server Return: HTTP/1.1 400 Bad Request \n")

                        client_connection.send(response)


                else:
                    response = b'\nHTTP/1.1 404 Not Found\n\nWeb Page Not Found'
                    client_connection.sendall(response)
                    f.write(str(headers[1][:21]) + " Access Time: " + str(
                        datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')) + " Request Filename: " + filename + '\n')
                    f.write(
                        "Server Return: " + "http://" + server_name + '/' + file_path + ' ' + "Server Response: HTTP/1.1 404 Not Found" + '\n')

    f.close()
    client_connection.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(128)
    # Establish connection
    while True:
        # Wait for client connections
        client_connection, client_address = server_socket.accept()
        # Start client thread
        print("Connected to server! ")
        thread = threading.Thread(target=handle_request(client_connection))
        thread.start()


# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 34568
# Create socket
print("Please use this link to access the remaining content in the server: 'http://127.0.0.1:34568'")
start_server()
