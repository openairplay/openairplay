#!/bin/bash
type python3 || echo "Is python3 installed?";
python3 -m openairplay.gui_main || echo "Non-Zero exit status.";
