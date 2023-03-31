import socket
import requests
import os
import time
from dotenv import load_dotenv

# Find .env files in the directory and load environment variables
load_dotenv()


class SocketServer:
    """
    A class used to represent a SocketServer that listens a SocketClient and responds with a product prices and his updates.
    While a SocketClient is connected, SocketServer watchs for prices updates in a REST API Server and responds when prices been updated.
    ...

    Attributes:
    server (Socket Object): A socket
    address (tuple (str, int)): Address to connect whit the SocketServer (host, port)
    client_address (tuple (str, int)): SocketClient connected address (host, port)
    client_connection : A SocketClient connected to SocketServer
    http_address (tuple (str, int)): Address to connect whit REST API Server (host, port)

    Is needed set up a .env file with the following environment variables:
    SOCKET_HOST: host address where server socket will be create
    SOCKET_PORT: port number where server socket will be create
    REST_API_HOST: host address where rest api is served
    REST_API_PORT: port number where server socket is served

    Usage example:
    s = SocketServer
    s.start()
    """

    def __init__(self):
        """
        Initializes a instance of SocketServer.
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ''
        self.client_address = ''
        self.client_connection = ''
        self.http_address = ''

    def set_address(self):
        """ 
        Sets SocketServer address with environment variables.
        """
        try:
            self.address = (os.environ['SOCKET_HOST'],
                            int(os.environ['SOCKET_PORT']))
        except Exception as e:
            print(f'Error with environment variables: {e}')
            exit()

    def set_http_address(self):
        """ 
        Sets REST API Server address with environment variables.
        """
        try:
            self.http_address = (
                os.environ['REST_API_HOST'], os.environ['REST_API_PORT'])
        except Exception as e:
            print(f'Error with environment variables: {e}')
            exit()

    def start_listening(self):
        """ 
        Bind and enable SocketServer to accept a connection. 
        """
        self.set_address()
        self.server.bind(self.address)
        self.server.listen(1)

    def request_prices(self, product_id):
        """ 
        Requests prices for a product to REST API server.
        Args:
            product_id (str): Product ID
        Returns:
            response object | False: If request returns 200 return response, else return False.
        """
        self.set_http_address()
        try:
            r = requests.get(
                f'http://{self.http_address[0]}:{self.http_address[1]}/product/{product_id}')
            r.raise_for_status()

            if r.status_code == 200:
                return r
            else:
                return False

        except requests.exceptions.HTTPError as errh:
            if (r.json().get('message')):
                error = r.json().get('message').encode('utf-8')
            else:
                error = b'HTTP Server Error'

            self.client_connection.sendall(error)
            self.client_connection.close()

            print('HTTP Server Error')
            print(errh.args)
            return False

    def validate(self, product_id):
        """ 
        Checks if the product_id sent by client is valid
        Args:
            product_id (str): Product ID
        Returns:
            boolean: If is valid returns True, else False.
        """
        if product_id and product_id.isnumeric():
            return True
        else:
            return False

    def handle_prices_updates(self, product_id):
        """ 
        Request for prices to REST API and if it responds, checks if prices has been updated in 10 seconds intervals and sends prices updated to client
        Args:
            product_id (str): Product ID
        """
        purchase_price = 0
        sale_price = 0
        while True:
            request = self.request_prices(product_id)
            if request:
                new_purchase_price = request.json()['purchaseprice']
                new_sale_price = request.json()['saleprice']
                if purchase_price != new_purchase_price or sale_price != new_sale_price:
                    purchase_price = new_purchase_price
                    sale_price = new_sale_price
                    try:
                        print(request.text)
                        self.client_connection.sendall(request.content)
                    except TimeoutError:
                        print(f'Client connection closed')
                        break
                else:
                    print(f'No new price from http server')
                time.sleep(10)
            else:
                self.client_connection.close()
                return False

    def handle_client(self):
        """ 
        SocketServer starts listening for a connection. When a client connects, gets the product_id parameter and validate it. If is a product_id valid, requests prices to REST API, else closes client connection and keeps listening for a new connection.
        """
        while True:
            print('Waiting for a connection')
            self.client_connection, self.client_address = self.server.accept()
            print(
                f'{self.client_address[0]}:{self.client_address[1]} is connected')
            try:
                product_id = self.client_connection.recv(
                    16).decode('utf-8').strip()
                print('Received id {!r}'.format(product_id))
                print(self.validate(product_id))
                if self.validate(product_id):
                    self.handle_prices_updates(product_id)
                else:
                    print(
                        f'No data from {self.client_address[0]}:{self.client_address[1]}')
                    self.client_connection.close()
                    break
            except Exception as e:
                self.client_connection.sendall(b'Socket Server Error')
                print(f'Error: {e}')
                self.client_connection.close()

    def start(self):
        """ 
        Start Socket Server
        """
        self.start_listening()
        self.handle_client()


socket_server = SocketServer()
socket_server.start()
