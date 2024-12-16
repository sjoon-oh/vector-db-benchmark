#!/bin/bash

PGPASSWORD=passwd psql -h localhost -p 5432 -U postgres -f $1