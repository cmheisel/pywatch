import os
import sys
import datetime

def run_tests():
    os.system("clear")
    print "Running tests at %s" % datetime.datetime.now()
    os.system("../../bin/test")

if __name__ == "__main__":
    import autoreload
    autoreload.reloadFiles = ["tests.py", "models.py", "urls.py", "admin.py"]
    autoreload.main(run_tests)
