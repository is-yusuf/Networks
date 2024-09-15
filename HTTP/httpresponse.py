import socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = "10.133.15.12"
port = 80
clientsocket.connect((host, port))
send_data = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Fake Response</h1></body></html>"
clientsocket.sendall(send_data)
recv_data = clientsocket.recv(1024)
print(recv_data.decode('ascii'))
