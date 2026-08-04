#!/bin/bash
echo "Preparing app ..."
docker build -t my-flask-app .
docker network create app-net 2>/dev/null || echo "Network app-net already exists"
docker volume create redis-data 2>/dev/null || echo "Volume redis-data already exists"
echo "Preparation complete."
