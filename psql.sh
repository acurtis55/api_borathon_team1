#!/usr/bin/env bash

PGPORT=5432
PGUSER=
PGPASSWORD=

AWS_REGION=us-east-1
RDSHOST=

SSL_CERT_DIR="/Users/takayamaa/Desktop/cloud-workshop/api_borathon_team1/us-east-1-bundle(1).pem"

psql "host=$RDSHOST port=$PGPORT sslmode=verify-full sslrootcert=$SSL_CERT_DIR user=$PGUSER password=$PGPASSWORD"
