def resolve_destination(destination):
    print(destination)
    try:
        # Check if the destination is an IP address (in the format "xxx.xxx.xxx.xxx")
        if re.match(r'\d+\.\d+\.\d+\.\d+', destination):
            return destination

        # If not an IP address, resolve the domain to an IP
        ip = socket.gethostbyname(destination)
        return ip
    except Exception as e:
        print(f"Error resolving destination: {e}")
        return None



       while True:
            try:
                destination_data = destination_socket.recv(4096)
                if not destination_data:
                    break

                headers, content = separate_headers(destination_data)

                if content_type is None and b'Content-Type: text/html' in headers:
                    # If content type is not known and this packet is HTML, set the content type
                    content_type = "text/html"

                if content_type == "text/html":
                    # Translate only if content type is HTML
                    content = translate_html_content(content)
                # Reconstruct the response with translated content and original headers

                if content_type:
                    translated_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}"
                    client_socket.send(translated_response.encode())
                else:
                    # Forward non-HTML content as is
                    client_socket.send(destination_data)

            except socket.timeout:
                break


                 if b'Content-Type: text/html' in headers:
            # Translate only the textual content, not the HTML tags
            content = translate_html_content(content)
        # Reconstruct the response with translated content and original headers

        translated_response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}"
        print(f"Content:{content}\n")
        print(f"\n\nTranslation:{translated_response}")
        # Send the translated response back to the client
        client_socket.send(translated_response.encode())