#!/bin/bash
echo "Stopping app ..."
docker stop web redis 2>/dev/null
docker rm web redis 2>/dev/null
echo "App stopped. Data is preserved in the redis-data volume."
