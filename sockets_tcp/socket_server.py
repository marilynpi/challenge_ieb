import socket
import requests
from threading import Thread
import os
import time
import signal
import sys
from dotenv import load_dotenv

# Find .env files in the directory and load environment variables
load_dotenv()


class SocketServer:
    """
    A class used to represent a SocketServer that listens Clients and handles it with Threads. When a Client is connected a new Client Thread starts. 
    ...

    Attributes:
    server (Socket Object): A socket
    address (tuple (str, int)): Address to connect whit the SocketServer (host, port)

    Is needed set up a .env file with the following environment variables:
    SOCKET_HOST: host address where server socket will be create
    SOCKET_PORT: port number where server socket will be create

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

        signal.signal(signal.SIGINT, self.signal_handler)

    def set_address(self):
        """ 
        Sets Socket address with environment variables.
        """
        try:
            self.address = (os.environ['SOCKET_HOST'],
                            int(os.environ['SOCKET_PORT']))
        except Exception as e:
            print(f'Error with environment variables: {e}')
            exit()

    def start(self):
        """ 
        Bind and enable socket server to accept connections. 
        """
        self.set_address()
        try:
            self.server.bind(self.address)
            self.server.listen()
            print('Socket is listening..')
            self.handle_clients()
            self.server.close()

        except socket.error as e:
            print(str(e))

    def handle_clients(self):
        """ 
        When a client connects, starts a Client Thread.
        """
        while True:
            client_connection, client_address = self.server.accept()

            print(
                f'{client_address[0]}:{client_address[1]} is connected')

            Client(client_connection, client_address).start()

    def signal_handler(self, signal, frame):
        """ 
        Handle a Ctrl+C signal. When Ctrl+C is pressed, close and shutdown  Server.
        """
        print('Closing Server')
        self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        sys.exit(0)


class Client(Thread):
    """
    A class used to represent a Client Thread. Client inherits from Thread class. When a Client Thread starts, takes the Product ID sent by socket client, watchs for prices updates in a REST API Server and responds when prices been updated.
    ...

    Attributes:
    connection (Socket Object): Client connected to SocketServer
    address (tuple (str, int)): Client connected address (host, port)
    http_address (tuple (str, int)): Address to connect whit REST API Server (host, port)

    Is needed set up a .env file with the following environment variables:
    REST_API_HOST: host address where rest api is served
    REST_API_PORT: port number where server socket is served

    Usage example:

    Client(client_connection, client_address).start()

    """

    def __init__(self, client_connection, client_address):
        """
        Initializes a instance of Client Thread.
        """

        Thread.__init__(self)

        self.connection = client_connection
        self.address = client_address
        self.http_address = ''

        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        """ 
        Handle a Ctrl+C signal. When Ctrl+C is pressed, close and shutdown  Server.
        """

        print('Closing Client')
        # self.connection.close()
        sys.exit(0)

    def set_http_address(self):
        """ 
        Sets http address with environment variables.
        """

        try:
            self.http_address = (
                os.environ['REST_API_HOST'], os.environ['REST_API_PORT'])
        except Exception as e:
            print(f'Error with environment variables: {e}')
            exit()

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
        While a socket client is connected and REST API responds, requests for prices and checks if prices has been updated in 10 seconds intervals. If any price is updated, sends it to client.

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
                        self.connection.sendall(request.content)
                    except TimeoutError:
                        print(f'Client connection closed')
                        break
                else:
                    print(
                        f'No new price from http server for product {product_id}')
                time.sleep(10)
            else:
                raise Exception()

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

            self.connection.sendall(error)

            print('HTTP Server Error')
            print(errh.args)
            return False

        except requests.exceptions.ConnectionError:
            print(
                f'HTTP Server not rechable http://{self.http_address[0]}:{self.http_address[1]}')
            return False

    def run(self):
        """ 
        While a Client Thread runs, gets the product_id sent by socket client and validate it. If is a product_id valid, requests prices to REST API and watchs for updates, else closes client connection and keeps listening for a new connection.
        """

        while True:
            try:
                product_id = self.connection.recv(
                    16).decode('utf-8').strip()
                print('Received id {!r}'.format(product_id))

                if self.validate(product_id):
                    handle_prices_updates = self.handle_prices_updates(
                        product_id)

                else:
                    print(
                        f'No data from {self.address[0]}:{self.address[1]}')
                    self.connection.close()
                    break

            except Exception as e:
                self.connection.sendall(b'Socket Server Error')
                self.connection.close()
                return False


socket_server = SocketServer()
socket_server.start()
