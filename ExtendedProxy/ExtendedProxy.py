import socket
import threading
import re
from translate import Translator      
from bs4 import BeautifulSoup

user_requests={}

translator = Translator(to_lang="hi")

import csv
from datetime import datetime

def store_data(client_ip, server_ip):
    # Get the current date
    current_date = datetime.now()
    
    # Extract year, month, week, and day
    year = current_date.year
    month = current_date.month
    week = current_date.isocalendar()[1]  # Get the ISO week number (1 to 52)
    day = current_date.day

    # Define the path to the CSV file
    file_path = 'web_usage_data.csv'

    # Writing data to the CSV file
    with open(file_path, 'a', newline='') as file:
        fieldnames = ['Client_IP', 'Server_IP', 'Date', 'Month', 'Week', 'Count']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Check if the file is empty, if so, write header row
        if file.tell() == 0:
            writer.writeheader()

        # Read the existing data to check for the same client and server IP
        existing_data = []
        try:
            with open(file_path, 'r', newline='') as read_file:
                reader = csv.DictReader(read_file)
                existing_data = list(reader)
        except FileNotFoundError:
            pass

        found = False
        for row in existing_data:
            if row['Client_IP'] == client_ip and row['Server_IP'] == server_ip:
                row['Count'] = int(row['Count']) + 1
                found = True
                break

        # If the combination of client and server IP is not found, add a new row
        if not found:
            writer.writerow({
                'Client_IP': client_ip,
                'Server_IP': server_ip,
                'Date': f'{year}-{month:02d}-{day:02d}',
                'Month': month,
                'Week': week,
                'Count': 1  # Starting count for a new combination
            })

        # Write updated data back to the file
        if existing_data:
            with open(file_path, 'w', newline='') as write_file:
                writer = csv.DictWriter(write_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(existing_data)


def separate_headers(response_data):
    # Find the index of the first occurrence of '\r\n\r\n' which separates headers from content
    header_end = response_data.find(b'\r\n\r\n')
    if header_end != -1:
        headers = response_data[:header_end + 4]  # Include '\r\n\r\n' in the headers
        content = response_data[header_end + 4:]
    else:
        headers = b''  # If '\r\n\r\n' is not found, treat everything as headers
        content = response_data

    return headers, content

def update_request(request, path):
    # Remove the host part and update the request with only the path
    modified_request = re.sub(b'GET http://(.*?)/', b'GET /', request)
    modified_request = re.sub(b'GET /(.*?) HTTP/1.1', b'GET ' + path + b' HTTP/1.1', modified_request)
    modified_request = re.sub(b'GET /(.*?) HTTP/1.0', b'GET ' + path + b' HTTP/1.0', modified_request)
    return modified_request

def handle_client(client_socket, client_address):

    request = client_socket.recv(4096)
    print(request)
    print("\n")
    # Extract the destination host and port from the HTTP request line's path
    destination_host, destination_port,path = extract_destination(request)
    store_data(client_address,destination_host.decode())
    # if client_address not in user_requests:
    #     user_requests[client_address] = {}  # Initialize a dictionary for each client's IP address

    # if destination_host.decode() not in user_requests[client_address]:
    #     user_requests[client_address][destination_host.decode()] =  1
    # else:
    #     user_requests[client_address][destination_host.decode()] += 1
    
    if destination_host:

        # Create a socket to connect to the destination server
        destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        destination_socket.settimeout(5) 
        destination_socket.connect((destination_host.decode(), destination_port))
        modified_request = update_request(request, path)

        http_version = "1.1" if b'HTTP/1.1' in modified_request else "1.0"
        content_type = None

        if b'Host: 127.0.0.1:13000' in request:
            modified_request = modified_request.split(b'\r\n')[0] + b'\r\nHost: ' + destination_host + b'\r\n\r\n'

        print(f"HEADER:{modified_request}")

        # Forward the client's request to the destination server
        destination_socket.send(modified_request)
        response = b""
        while True:
            try:
                # Receive data from the destination server and forward it to the client
                destination_data = destination_socket.recv(4096)
                # print(f"Destination Data:{destination_data}\n")
                if not destination_data:
                    break
                response += destination_data
            except socket.timeout:
                break   
        print("\n\n")

        print(f"\nresponse:{response}\n")
        header,content = separate_headers(response)

        if b'Content-Type: text/html' in header:
            # Translate only the textual content, not the HTML tags
            content = translate_html_content(content)
            header = re.sub(b'Content-Length: \\d+', f'Content-Length: {len(content)}'.encode(), header)
        # Reconstruct the response with translated content and original headers

        # print(f"\ncontent:{content}\n")
        translated_response = header + content

        # Send the translated response back to the client
        client_socket.sendall(translated_response)

    # print(user_requests)
    if http_version == "1.0":
        client_socket.close()

def is_translatable(element):

    # Elements that should be translated
    translatable_tags = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'a','title']
    
    if element.parent.name in ['script', 'style']:
        return False  # Exclude content within script and style tags
    if element.startswith("<!doctype html>"):
        return False  # Exclude "<!doctype html>" and similar declarations
    if element.parent.name == 'img':
        return False  # Exclude content within image tags
    if element.parent.name == 'audio':
        return False  # Exclude content within audio tags
    if element.parent.name == 'video':
        return False  # Exclude content within video tags
    if element.parent.name in translatable_tags:
        return True  # Translate content within specified tags
    return False  # Default to exclude other content

def translate_html_content(content):

    soup = BeautifulSoup(content, 'html.parser')
    
    for element in soup.find_all(string=is_translatable):
            
            translated_text = translator.translate(element)
            print(translated_text)
            element.replace_with(translated_text)
    
    body_tag = soup.body
    for element in body_tag.children:
        
        if element.name is None:
            # Translate plain text within the <body> tag
            translated_text = translator.translate(element)
            element.replace_with(translated_text)

    return str(soup).encode()

def extract_destination(request):

    first_line = request.split(b'\r\n')[0]
    url = first_line.split(b' ')[1].lstrip(b'/')
    http_pos = url.find(b'://')
    if(http_pos==-1):
        temp = url
    else:
        temp = url[http_pos+3:]
    
    port_pos = temp.find(b':')

    path = b""
    webserver_pos = temp.find(b'/')
    if webserver_pos == -1:
        webserver_pos = len(temp)
        path = b'/'
    else:
        path = temp[webserver_pos:]

    webserver = b"" 
    port = b""
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
    proxy_port = 13000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((proxy_host, proxy_port))
    server.listen()
    print(f"[*] Listening on {proxy_host}:{proxy_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,addr[0],))
        client_handler.start()
        

if __name__ == '__main__':
    main()