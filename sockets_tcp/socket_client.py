import socket
import os
import sys
from dotenv import load_dotenv

# Find .env files in the directory and load environment variables
load_dotenv()


class SocketClient:
    """
    A class used to represent a SocketClient that sends a product_id received as parameter to a SocketServer, then wait for prices and updates.
    ...

    Attributes:
    server (Socket Object): A socket
    server_address (tuple (str, int)): Address to connect whit a SocketServer (host, port)
    product_id (str): Product ID received as parameter

    Is needed set up a .env file with the following environment variables:
    SOCKET_HOST: SocketServer host address
    SOCKET_PORT: SocketServer port number

    Usage example:
    s = SocketClient(product_id)
    s.start()
    """

    def __init__(self, product_id):
        """
        Initializes a instance of SocketClient.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ''
        self.product_id = product_id

    def set_server_address(self):
        """ 
        Sets server_address with environment variables.
        """
        try:
            self.server_address = (
                os.environ['SOCKET_HOST'], int(os.environ['SOCKET_PORT']))
        except Exception as e:
            print(f'Error with environment variables: {e}')
            exit()

    def handle_request(self):
        """ 
        Sends a product_id to SocketServer and wait for prices and updates.
        """
        try:
            print('Sending ProductID {!r}'.format(self.product_id))
            self.server.sendall(self.product_id.encode('utf-8'))

            while True:
                try:
                    data = self.server.recv(1024)
                    if (data.decode('utf-8') != ''):
                        print('Received {!r}'.format(data.decode('utf-8')))
                    else:
                        self.server.close()
                        break
                except Exception as e:
                    print(f'Error: {e}')
                    self.server.close()

        except Exception as e:
            print(f'Error: {e}')
            self.server.close()

        finally:
            print('Closing socket')
            self.server.close()

    def start(self):
        """ 
        Start connection to SocketServer and wait for prices updates
        """
        self.set_server_address()
        try:
            self.server.connect(self.server_address)
            self.handle_request()

        except Exception as e:
            print(f'Error: {e}')


# Validate parameters, create SocketClient and starts connection with
if len(sys.argv) == 2 and sys.argv[1].isnumeric():
    socket_client = SocketClient(sys.argv[1])
    socket_client.start()
else:
    print('Please enter a valid product ID (must be a number)')
    print('Example: socket_client.py 5')
