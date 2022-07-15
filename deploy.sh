#!/bin/bash

GIT_BRANCH="master"

echo -e "Configuring git client"
git config --global user.email "bot-rletka-02@digitalocen.com"
git config --global user.name "DigitalOcean FavBet"

echo -e "Pulling latest code from github.com"
git pull origin ${GIT_BRANCH}
