#!/bin/bash

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
OPENAIRPLAY_VIRTUALENV="$SCRIPT_DIR/venv"
cd $SCRIPT_DIR

if [ -d "$VIRTUAL_ENV" ]; then
    echo -e "${GREEN}Running from virtualenv ${VIRTUAL_ENV}${ENDCOLOR}"
elif [ -d "$OPENAIRPLAY_VIRTUALENV" ]; then
    echo -e "${GREEN}Sourcing Python3 virtual environment.${ENDCOLOR}"
    source "${OPENAIRPLAY_VIRTUALENV}/bin/activate"
else
    echo -e "${RED}Python3 virtual environment DOES NOT exist.${ENDCOLOR}"
    python3 --version
    echo -e "${GREEN}Creating a virtual environment at ${OPENAIRPLAY_VIRTUALENV}${ENDCOLOR}"
    python3 -m venv "$OPENAIRPLAY_VIRTUALENV"
    echo -e "${GREEN}Sourcing Python3 virtual environment.${ENDCOLOR}"
    source "${OPENAIRPLAY_VIRTUALENV}/bin/activate"
    echo -e "${GREEN}Installing Python3 packages that are required to run OpenAirPlay.${ENDCOLOR}"
    python3 -m pip install --upgrade pip
    python3 -m pip install -r "${SCRIPT_DIR}/requirements.txt"
fi

type python3 || echo "Is python3 installed?"
python3 -m openairplay.gui_main
