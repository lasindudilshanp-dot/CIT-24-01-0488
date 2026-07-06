#!/bin/bash
echo "Running app ..."

docker run -d \
  --name redis \
  --network app-net \
  --restart unless-stopped \
  -v redis-data:/data \
  redis:7 redis-server --appendonly yes

docker run -d \
  --name web \
  --network app-net \
  --restart unless-stopped \
  -p 5000:5000 \
  my-flask-app

echo "The app is available at http://localhost:5000"
