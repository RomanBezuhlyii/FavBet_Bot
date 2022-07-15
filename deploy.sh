#!/bin/bash

PROJECT_PATH="/opt/deployer/FavBet_Bot"
GIT_BRANCH="master"

LAST_PATH=$(pwd)

echo -e "Entring project directory: ${PROJECT_PATH}"
cd ${PROJECT_PATH}

echo -e "Configuring git client"
git config --global user.email "bot-rletka-02@digitalocen.com"
git config --global user.name "DigitalOcean FavBet"

echo -e "Pulling latest code from github.com"
git pull origin ${GIT_BRANCH}

echo -e "Stopping application"
docker-compose down

echo -e "Build latest application version"
docker-compose build --no-cache

echo -e "Running up application"
docker-compose up --force-recreate --build  --detach

echo -e "Restoring cli context"
cd ${LAST_PATH}
