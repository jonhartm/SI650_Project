import time
import sys

# try to parse a string to an int.
# returns None if it failed
def tryParseInt(s):
    try:
        return (int(s))
    except Exception:
        return None

# class for starting and stopping a timer, then reporting the elapsed time
class Timer():
    def start(self):
        self.start = time.time()

    def stop(self):
        self.end = time.time()
        self.elapsed = self.end-self.start

    def __str__(self):
        return '{:.3}s'.format(self.elapsed)

def super_print(s):
    sys.stdout.write(s+"\n")
    sys.stdout.flush()
