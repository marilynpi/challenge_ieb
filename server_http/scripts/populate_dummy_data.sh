#!/bin/bash

# Get enviroment variables
source ../.env

# Populate Product Table
echo "Populate product table..." 

sudo -u postgres psql -d $DB_DATABASE -c << EOF "INSERT INTO products ( id, purchasePrice, salePrice, description )
  VALUES ('1', 200, 212, 'Dummy Product 1'),
  ('2', 355, 345, 'Dummy Product 2'),
  ('3', 45, 48, 'Dummy Product 3'),
  ('4', 568, 600, 'Dummy Product 4'),
  ('5', 435, 430, 'Dummy Product 5');"
EOF