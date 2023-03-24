#!/bin/bash

# Get enviroment variables
source .env

# Create Database
sudo -u postgres psql -c "CREATE DATABASE $DB_DATABASE;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';" 
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_DATABASE TO $DB_USER;"

# Create Product Table
sudo -u postgres psql -d $DB_DATABASE -c << EOF "CREATE TABLE $DB_TABLE( id text not null,
  purchasePrice real,
  salePrice real,
  description text,
  PRIMARY KEY( id ));"
EOF
sudo -u postgres psql -d $DB_DATABASE -c "GRANT SELECT, UPDATE ON TABLE $DB_TABLE TO $DB_USER;"

# Start service
echo "Start PostgreSql service..." 
sudo service postgresql start
