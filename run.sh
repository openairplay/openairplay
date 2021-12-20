#!/bin/bash

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

if [ ! -d "env" ]
then
    echo -e "${RED}Python3 virtual environment DOES NOT exists.${ENDCOLOR}"
    python3 --version
    echo -e "${GREEN}Creating Python3 virtual environment.${ENDCOLOR}"
    python3 -m venv env
    echo -e "${GREEN}Sourcing Python3 virtual environment.${ENDCOLOR}"
    source ./env/bin/activate
    echo -e "${GREEN}Installing Python3 packages that are required to run OpenAirPlay.${ENDCOLOR}"
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt 
else
    echo -e "${GREEN}Sourcing Python3 virtual environment.${ENDCOLOR}"
    source ./env/bin/activate
    type python3 || echo "Is python3 installed?";
    echo -e "${GREEN}Starting Open Air Play.${ENDCOLOR}"
    python3 -m openairplay.gui_main
fi



