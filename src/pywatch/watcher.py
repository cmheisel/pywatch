import os
import time

class Watcher(object):
    def __init__(self, files=None, cmds=None):
        self.files = [] 
        self.cmds = []
        self.num_runs = 0
        self.mtimes = {}

        if files: self.add_files(*files)
        if cmds: self.add_cmds(*cmds)

    def monitor(self):
        while True:
            try:
                self.monitor_once()
                time.sleep(1)
            except KeyboardInterrupt:
                return True

    def monitor_once(self, execute=True):
        for f in self.files:
            mtime = os.stat(f).st_mtime
            if f not in self.mtimes.keys():
                self.mtimes[f] = mtime
                continue
            
            if mtime > self.mtimes[f]:
                self.mtimes[f] = mtime
                if execute:
                    self.execute()
                    break

    def execute(self):
        [ os.system(cmd) for cmd in self.cmds ]
        self.num_runs += 1
        return self.num_runs

    def add_files(self, *files):
        valid_files = [ os.path.realpath(f) for f in files if os.path.exists(f) and os.path.isfile(f) ]
        unique_files = [ f for f in valid_files if f not in self.files ]
        self.files = self.files + unique_files
        self.monitor_once(execute=False)

    def add_cmds(self, *cmds):
        unique_cmds = [ c for c in cmds if c not in self.cmds ]
        self.cmds = self.cmds + unique_cmds
