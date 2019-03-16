import datetime
import sys


def debug_print(message, file=sys.stderr):
    print(f"[{datetime.datetime.now()}] {message}", file=file)
