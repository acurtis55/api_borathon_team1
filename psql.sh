#!/usr/bin/env bash

PGUSER=postgres
PGPORT=5432

AWS_REGION=us-east-1
RDSHOST=
PGPASSWORD="$(aws rds generate-db-auth-token --hostname $RDSHOST --port $PGPORT --region $AWS_REGION --username $PGUSER )"

# echo $PGPASSWORD

SSL_CERT_DIR="/Users/takayamaa/Desktop/cloud-workshop/api_borathon_team1/us-east-1-bundle(1).pem"
echo "host=$RDSHOST port=$PGPORT sslmode=verify-full sslrootcert=$SSL_CERT_DIR dbname=postgres user=$PGUSER password=$PGPASSWORD"
psql "host=$RDSHOST port=$PGPORT sslmode=verify-full sslrootcert=$SSL_CERT_DIR dbname=postgres user=$PGUSER password=$PGPASSWORD"
