#!/bin/bash
type python3 || echo "Is python3 installed?";
python3 main.py || echo "Non-Zero exit status.";

echo "Program quit." # finally: this will always happen
