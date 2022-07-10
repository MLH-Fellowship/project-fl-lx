#!/bin/bash

cd project-fl-lx
git fetch && git reset origin/main --hard 
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml -d --build
