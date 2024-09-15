import socket

# Specify an IPv4 TCP socket
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = "stearns.mathcs.carleton.edu"
port = 5221
clientsocket.connect((host, port))

# The data to send is a sequence of bytes
send_data = bytearray()

# version number is 1
send_data.append(1)
send_data.append(3)
send_data.append(0)
send_data.append(0)

# message type is 1
# send_data.append(7)

# flags are safely ignored

# the length of the payload
# send_data.append(1)
# send_data.append(1)

# send_data.append(25)

# send_data.append(len(b"nunu is a very cute kitty"))

# send_data += b'nunu is a '
# send_data += b"very cute kitty"

clientsocket.sendall(send_data)
recv_data = clientsocket.recv(1024)

# Print one byte at a time
for b in recv_data:
    print(b)

# print blank line
print()
    
# Print just the payload    
print(recv_data[4:].decode('ascii'))
# You should always close your TCP sockets when you are done with them
clientsocket.close()
