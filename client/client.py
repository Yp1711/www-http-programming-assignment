import socket
from bs4 import BeautifulSoup
import sys
import webbrowser
import os
import re

status_prase = {404:'Not found',501: 'Not Implemented'}

# Function to send an HTTP GET request to a server
def send_get_request(server_ip,server_port,proxy_ip,proxy_port,path):

    pattern = r'[a-zA-Z!@#$%^&*()]'

    if re.search(pattern, server_ip):
        server_address = server_ip
    else:
        server_address = f"{server_ip}:{server_port}"

    if path == '/':
        request_path = '/'
    else:
        request_path = '/' + path

    if not proxy_ip:
        server = server_ip
        port = server_port
        http_request = f"GET {request_path} HTTP/1.0\r\nHost: {server_address}\r\n\r\n"
    else:
        server = proxy_ip
        port = proxy_port
        http_request = f"GET http://{server_address}{request_path} HTTP/1.0\r\nHost: {server_address}\r\n\r\n"

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server or proxy
    client_socket.connect((server, int(port)))

    # Send the HTTP request12030
    client_socket.send(http_request.encode())

    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    
     # Close the socket
    client_socket.close()

    return response

# Function to parse HTML for references to other objects
def parse_html_for_references(html_content):

    resource_url=[]
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(['link', 'script', 'img','audio','video','iframe','object','embed']):
    # Check if the tag has a 'src' or 'href' attribute
        if 'src' in tag.attrs:
            resource_url.append(tag['src'])
        elif 'href' in tag.attrs:
            resource_url.append(tag['href'])
        elif 'data' in tag.attrs:
            resource_url.append(tag['data'])
        elif 'rel' in tag.attrs:
            resource_url.append(tag['rel'])
        else:
            continue
    return resource_url

def store_the_file(response,server_ip,server_port,proxy_ip,proxy_port,path):

    start_index = response.find(b'\r\n\r\n')
    response_line = response[:start_index].decode().split("\r\n")[0]
    version, status_code, *_  = response_line.split(" ")

    if status_code == "200":

        body = response[start_index+4:]

        if not body:
            print("Empty response received.")

        else:
            extension = path.split('.')[-1]
            if b'Content-Type: text/html' in response:
                
                # Decode the received bytes as UTF-8 (assuming the HTML content is in UTF-8 encoding)
                html_content = body.decode('utf-8')

                if path == '/':
                    path = 'root.html'

                # Save the received HTML content to a file
                with open(path, 'w') as file:
                    file.write(html_content)

                # parse for references
                references = parse_html_for_references(html_content)
                for reference in references:
                    response = send_get_request(server_ip,server_port,proxy_ip,proxy_port,reference)
                    store_the_file(response,server_ip,server_port,proxy_ip,proxy_port,reference)
         
            else:

                with open(path, 'wb') as image_file:
                    image_file.write(body)
    else:
        print(f"{status_code}: {status_prase[int(status_code)]}")
        sys.exit()


# Main function
def main():

    server_ip = input("Enter Server IP:")
    server_port = input("Enter Server Port:") 
    proxy_ip = input("Enter Proxy IP (else hit enter for direct communication):")
    proxy_port = input("Enter Proxy Port (else hit enter for direct communication):")
    path = input("Enter Path:")

    # Send an initial GET request to the web server or proxy

    response = send_get_request(server_ip,server_port,proxy_ip,proxy_port,path)
    store_the_file(response,server_ip,server_port,proxy_ip,proxy_port,path)
    print("files downloaded.")
    if path == '/':
        path = 'root.html'
    wants_to_open = input("Do you want to open the file in browser(Y/n):")
    if wants_to_open.lower() == 'y':
        webbrowser.open('file://' + os.getcwd()+ '/' + path)
    else:
        wants_to_read = input("Do you want to print the recieved raw content(Y/n):")
        if wants_to_read.lower() == 'y':
            if path.split('.')[-1].lower() in ['html','htm','xhtml']:
                with open(path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()
                    print(html_content)
            else:
                print("Its not an HTML File. Thank You")
        else:
            print("Thank You")
    
if __name__ == "__main__":
    main()