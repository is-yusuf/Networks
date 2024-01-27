# Import required libraries
import socket
import _thread
import ssl
import re

# Constants
BACKLOG = 50            # Number of incoming connections that can be queued
BUFFER_SIZE = 4096      # Size of buffer for receiving data
PORT = 8080             # Port to listen on

# Function to handle client requests
def handle_client(client_socket):
    try:
        # Receive the client request
        request = client_socket.recv(BUFFER_SIZE).decode()
        first_line = request.split('\n')[0]

        # Extract the URL
        url = first_line.split(' ')[1]
        # Check if the URL is for https://yusuf.com
        if "yusuf.com" in url:
            # Redirect to google.com
            redirect_response = "HTTP/1.1 302 Found\r\nLocation: https://142.250.191.110\r\n\r\n"
            client_socket.sendall(redirect_response.encode())
            print("redirected")
        else:
            # Connect to the original server
            http_pos = url.find("://")  # find the position of ://
            if http_pos == -1:
                temp = url
            else:
                temp = url[(http_pos+3):]  # get the rest of the URL

            port_pos = temp.find(":")  # find the port position (if any)

            # Default port
            server_port = 80
            if port_pos == -1:
                port_pos = temp.find("/")

            # Get the server
            webserver = ""
            if port_pos == -1 or temp[port_pos] == '/':
                port = 80
                webserver = temp[:port_pos]
            else:
                port = int((temp[(port_pos+1):])[:temp[(port_pos+1):].find('/')])
                webserver = temp[:port_pos]

            # Create a socket to connect to the web server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, server_port))
            s.sendall(request.encode())

            while True:
                # Receive data from web server
                data = s.recv(BUFFER_SIZE)

                if len(data) > 0:
                    # Send to browser
                    client_socket.send(data)
                else:
                    break
            s.close()
    except Exception as e:
        print(e)
    finally:
        # Close the client connection
        client_socket.close()

# Main function to start the server
def start_server():
    try:
        # Create a socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', PORT))
        server_socket.listen(BACKLOG)

        print(f"Proxy Server Running on port {PORT}")

        while True:
            # Accept connections from outside
            (client_socket, address) = server_socket.accept()
            _thread.start_new_thread(handle_client, (client_socket,))
    except Exception as e:
        print("Exception:", e)
        server_socket.close()

if __name__ == "__main__":
    start_server()
