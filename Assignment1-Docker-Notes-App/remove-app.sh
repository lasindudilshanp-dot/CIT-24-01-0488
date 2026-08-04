#!/bin/bash
echo "Removed app."
docker stop web redis 2>/dev/null
docker rm web redis 2>/dev/null
docker rmi my-flask-app 2>/dev/null
docker network rm app-net 2>/dev/null
docker volume rm redis-data 2>/dev/null
echo "All resources removed."
