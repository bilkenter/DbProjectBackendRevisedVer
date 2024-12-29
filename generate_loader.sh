#!/bin/bash

LOADER_FILE="schemas/loader.sql"

echo "-- Load main schema" > $LOADER_FILE
echo "\\i '/docker-entrypoint-initdb.d/schema.sql'" >> $LOADER_FILE

echo -e "\n-- Load views" >> $LOADER_FILE
for file in schemas/views/*.sql; do
  echo "\\i '/docker-entrypoint-initdb.d/${file#schemas/}'" >> $LOADER_FILE
done

echo -e "\n-- Load triggers" >> $LOADER_FILE
for file in schemas/triggers/*.sql; do
  echo "\\i '/docker-entrypoint-initdb.d/${file#schemas/}'" >> $LOADER_FILE
done
