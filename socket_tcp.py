import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_address = ('localhost', 8050)
print(f'Starting up on {server_address[0]} port {server_address[1]}')
server_socket.bind(server_address)

# Listen for incoming connections (up to 5)
server_socket.listen(5)

while True:
    # Wait for a connection
    print('Waiting for a connection')
    client_socket, client_address = server_socket.accept()
    print(f"{client_address[0]}:{client_address[1]} is connected")
    try:
        # Receive the data (1024 bytes) and retransmit it
        data = client_socket.recv(1024)
        if data:
            print(f'Client sent: {data}')
            print('Sending data back to client')
            client_socket.sendall(data)
            break
    finally:
        # Clean up the connection
        client_socket.close()