{ # your 'try' block
    python3 main.py
} || { # your 'catch' block
    python main.py
}

rm tmp # finally: this will always happen
