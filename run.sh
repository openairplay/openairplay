{ #'try' block
    type python3 || { echo "Is python3 installed?"; exit }
    python3 main.py
} || { #'catch' block
    echo "Non-Zero exit status."
}

echo "Program quit." # finally: this will always happen
