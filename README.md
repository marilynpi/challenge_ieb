# Challenge Ieb

A technical challenge that implements a socket TCP server and client in Python, and a REST API in Node.js.

## Requeriments

- PostgreSQL
- Node.js v18.15.0
- Python 3.8.10


## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file in directory root.

`SOCKET_HOST`
`SOCKET_PORT`
`REST_API_HOST`
`REST_API_PORT`
`DB_USER`
`DB_PASSWORD`
`DB_HOST`
`DB_PORT`
`DB_DATABASE`
`DB_TABLE` 

Example: 
```bash
  SOCKET_HOST=localhost
  SOCKET_PORT=8052
  REST_API_HOST=localhost
  REST_API_PORT=4000
  DB_USER=dummy_user
  DB_PASSWORD=dummy_password
  DB_HOST=localhost
  DB_PORT=5432
  DB_DATABASE=db_name
  DB_TABLE=products
```

## Installation

Clone the project

```bash
  git clone git@github.com:marilynpi/challenge_ieb.git
```

Go to the project directory

```bash
  cd challenge_ieb
```

Install Python dependencies:

```bash
  cd sockets_tcp/
  pip install -r requirements.txt
```
Install Node.js dependencies:
```bash
  cd server_http/
  npm install
```

Run the following scripts to create and populate PostgreSQL database. 

```bash
  ./server_http/scripts/set_up_db.sh
  ./server_http/scripts/populate_dummy_data.sh
```

## Run Locally

Start http server:

```bash
  cd server_http/
  npm start
```

Start Socket Server TCP:

```bash
  cd sockets_tcp/
  python3 sockets_tcp/socket_server.py
```

Start Socket Client: receives as parameter a number as product id

```bash
  cd sockets_tcp/
  python3 sockets_tcp/socket_client.py 2

```
## Next steps

- Add [logging](https://docs.python.org/3/howto/logging.html) in sockets implementation
- Add testing with [pytest](https://docs.pytest.org/en/7.2.x/) and [mocha](https://mochajs.org/)
- Dockerize
- Add monitoring with Sentry or Errbit