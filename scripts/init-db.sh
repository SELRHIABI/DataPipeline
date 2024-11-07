#!/bin/bash
set -e

# Define the connection parameters
PGHOST="localhost"
PGPORT="5432"
PGUSER="airflow"
PGPASSWORD="airflow"

export PGPASSWORD="$PGPASSWORD"

# Function to create a database if it does not exist
create_db_if_not_exists() {
    local dbname=$1
    psql -v ON_ERROR_STOP=1 --host="$PGHOST" --port="$PGPORT" --username="$PGUSER" <<-EOSQL
        SELECT 'CREATE DATABASE $dbname'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$dbname')\gexec
        GRANT ALL PRIVILEGES ON DATABASE $dbname TO $PGUSER;
EOSQL
}

# Create dbt_database if it does not exist
create_db_if_not_exists "dbt_database"

# Create metabase if it does not exist
create_db_if_not_exists "metabase"