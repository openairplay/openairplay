{ # your 'try' block
    python3 main.py
} || { # your 'catch' block
    echo "Non-Zero exit status."
}

echo "Program quit." # finally: this will always happen
