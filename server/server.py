import socket
import os
import threading
import mimetypes

# Define the port to listen on
PORT = 6789

# Define the base directory for serving files
BASE_DIR = os.getcwd()

# Function to parse HTTP request
def parse_request(client_socket):
    request_data = b""
    while True:
        chunk = client_socket.recv(1024)
        request_data += chunk
        if b"\r\n\r\n" in request_data:
            break
    return request_data.decode("utf-8")

# Function to send an HTTP response
def send_response(client_socket, status_code, content_type, content):
    response = b""
    response = str.encode(f"HTTP/1.1 {status_code}\r\n")
    response += str.encode(f"Content-Type: {content_type}\r\n")
    response += str.encode(f"Content-Length: {len(content)}\r\n")
    response += b"\r\n"
    response += content
    client_socket.send(response)

# Function to handle an HTTP request
def handle_request(client_socket):
    request_data = parse_request(client_socket)
    request_lines = request_data.split("\r\n")
    request_line = request_lines[0]

    method, path, _ = request_line.split(" ")

    if method == "GET":
        file_path = os.path.join(BASE_DIR, path.lstrip("/"))
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                content = file.read()
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream' 
            send_response(client_socket, "200 OK", content_type, content)
        else:
            send_response(client_socket, "404 Not Found", "text/html", str.encode("404 Not Found"))
    else:
        send_response(client_socket, "501 Not Implemented", "text/html", str.encode("501 Not Implemented"))
    
    client_socket.close()

# Create the socket and start listening for connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", PORT))
server_socket.listen()
print(f"Server listening on port {PORT}")
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    request_thread = threading.Thread(target=handle_request, args=(client_socket,))
    request_thread.start()
