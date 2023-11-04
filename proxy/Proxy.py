import socket
import threading
import re

def update_request(request, path):
    # Remove the host part and update the request with only the path
    modified_request = re.sub(b'GET http://(.*?)/', b'GET /', request)
    modified_request = re.sub(b'GET /(.*?) HTTP/1.1', b'GET ' + path + b' HTTP/1.1', modified_request)
    modified_request = re.sub(b'GET /(.*?) HTTP/1.0', b'GET ' + path + b' HTTP/1.0', modified_request)

    return modified_request

def handle_client(client_socket):

    request = client_socket.recv(4096)

    print(f"\n\nRequest:{request}\n\n")
    
    # Extract the destination host and port from the HTTP request line's path
    destination_host, destination_port,path = extract_destination(request)

    print(destination_host, destination_port,path)
    
    if destination_host:

        # Create a socket to connect to the destination server
        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.settimeout(50) 
        destination_socket.connect((destination_host.decode(), destination_port))
        modified_request = update_request(request, path)
        
        http_version = "1.1" if b'HTTP/1.1' in modified_request else "1.0"

        if b'Host: 127.0.0.1:12000' in request:
            modified_request = modified_request.split(b'\r\n')[0] + b'\r\nHost: ' + destination_host + b'\r\n\r\n'
        
        print(f"HEADER:{modified_request}")

        # Forward the client's request to the destination server
        destination_socket.send(modified_request)


        while True:
            try:
                # Receive data from the destination server and forward it to the client
                destination_data = destination_socket.recv(4096)
                # print(f"\nDATA:{destination_data}\n")
                if len(destination_data) > 0:
                    client_socket.send(destination_data)
                else:
                    break

            except socket.timeout:
                break

    if http_version == "1.0":
        client_socket.close()


def extract_destination(request):

    first_line = request.split(b'\r\n')[0]
    url = first_line.split(b' ')[1].lstrip(b'/')
    http_pos = url.find(b'://')
    if(http_pos==-1):
        temp = url
    else:
        temp = url[http_pos+3:]
    
    path = b""
    webserver_pos = temp.find(b'/')
    if webserver_pos == -1:
        webserver_pos = len(temp)
        path = b'/'
    else:
        path = temp[webserver_pos:]

    webserver = b"" 
    port = b""
    port_pos = temp.find(b':')
    if (port_pos==-1 or webserver_pos < port_pos): 
        # default port 
        port = int((b'80').decode()) 
        webserver = temp[:webserver_pos] 

    else: # specific port 
        port = int(((temp[(port_pos+1):])[:webserver_pos-port_pos-1]).decode())
        webserver = temp[:port_pos]  
   
    return webserver,port,path


def main():
    proxy_host = '127.0.0.1'
    proxy_port = 12000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((proxy_host, proxy_port))
    server.listen()
    print(f"[*] Listening on {proxy_host}:{proxy_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    main()