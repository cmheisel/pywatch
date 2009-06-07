import os

import sys
import datetime

def run_tests():
    os.system("clear")
    print "Running tests at %s" % datetime.datetime.now()
    os.system("python tests.py")

if __name__ == "__main__":
    import autoreload
    autoreload.reloadFiles = ["tests.py", "watcher.py"]
    autoreload.main(run_tests)
