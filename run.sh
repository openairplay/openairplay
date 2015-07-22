{ # your 'try' block
    python3 main.py
} || { # your 'catch' block
    echo "The program has crashed, please report the error."
}

echo "Program quit." # finally: this will always happen
