import datetime
import os
import threading
import time

class WatchNode( object ):
    def __init__( self, fentry ): 
        if not os.path.exists( fentry ): 
            raise IOError( "Filesystem node does not exists" ) 
        else:
            self.name = os.path.abspath( fentry ) 
            self.mtime = None 
            self.children = None 

            self.updateMTime()
            if os.path.isdir( fentry ):
                self.children = [] 
                self.checkChildrenDiff()
                
    def updateMTime( self ):
        mtime = None 
        try:
            mtime = os.stat( self.name ).st_mtime
        except OSError:
            #The file might be right in the middle of being written so sleep
            time.sleep(1)
            mtime = os.stat( self.name ).st_mtime

        if self.mtime is not None and self.mtime == mtime:
            return False

        self.mtime = mtime
        return True

    def checkChildrenDiff( self ): 
        children = os.listdir( self.name )
        added = [ child for child in children if child not in self.children]
        removed = [ child for child in self.children if child not in children] 
        self.children = children
        return (added,removed)


class Watcher(object):
    def __init__(self, files=None, cmds=None, verbose=False):
        self.files = [] 
        self.dirs = { } 
        self.cmds = []
        self.num_runs = 0
        self._monitor_continously = False 
        self._monitor_thread = None
        self.verbose = verbose
    
        if files: self.add_files(*files)
        if cmds: self.add_cmds(*cmds)

    def monitor(self):
        #We only want one thread, dear god
        self.stop_monitor()

        self._monitor_continously = True
        self._monitor_thread = threading.Thread(target=self._monitor_till_stopped)
        self._monitor_thread.start()

    def run_monitor(self):
        """Called by main thread methods like __main__ so Ctrl-C works"""
        self.monitor()
        try:
            while self._monitor_continously:
                time.sleep(.02)
        except KeyboardInterrupt:
            self.stop_monitor()

    def stop_monitor(self):
        if self._monitor_thread and self._monitor_thread.isAlive():
            self._monitor_continously = False
            self._monitor_thread.join(0.05)

    def _monitor_till_stopped(self):
        while self._monitor_continously:
            self.monitor_once()
            time.sleep(1)

    def monitor_once(self):
        for f in self.files:
            if not os.path.exists( f.name ): 
                self.fileRemoved( f.name )    
            elif f.updateMTime():
                if f.children is None: 
                    self.fileChanged( f.name ) 
                else: 
                    added, removed = f.checkChildrenDiff() 
                    for a in added: 
                        self.fileAdded( os.path.join( f.name, a) ) 
                    for r in removed: 
                        self.fileRemoved( os.path.join( f.name, r ) ) 

    def fileChanged( self, fname ): 
        if self.verbose: print("---> File changed: %s" % fname ) 
        self.execute( fname ) 

    def fileAdded( self, fname ): 
        if self.verbose: print("---> File added %s" % fname ) 
        self.execute( fname ) 
        n = WatchNode( fname ) 
        self.files.append( n ) 

    def fileRemoved( self, fname ): 
        if self.verbose: print("---> File removed %s" % fname ) 
        # TODO: Make some action on removal 
        for x in self.files: 
            if x.name == fname: 
                self.files.remove( x ) 
                return
        
    def execute(self, targetFile ):
        if self.verbose: print( "---> Running commands at %s" % datetime.datetime.now() )
        for cmd in self.cmds: 
            # for backward compat 
            if cmd.__class__ == 'str':
                os.system( cmd ) 
            else: 
                cmd.runCmds( targetFile ) 
        
        self.num_runs += 1
        return self.num_runs

    def addNode( self, fname ):
        # check it doesn't exists 
        for x in self.files: 
            if x.name == fname:
                return 
        n = WatchNode( fname ) 
        self.files.append( n ) 

    def addDirs(self, dirnames):
        for dirname in dirnames:
            for path, dirs, files in os.walk(dirname):
                for f in files:
                    self.addNode( os.path.join( path, f) )   
                for d in dirs: 
                    self.addNode( os.path.join( path, d) ) 

    def add_files(self, *files):
        onlyfiles = [ os.path.realpath(f) for f in files if os.path.exists(f) and os.path.isfile(f) ]
        for f in onlyfiles: 
            self.addNode( f ) 
        
        onlydirs = [ os.path.realpath(f) for f in files if os.path.exists(f) and os.path.isdir(f) ]
        self.addDirs(onlydirs)


    def add_cmds(self, *cmds):
        unique_cmds = [ c for c in cmds if c not in self.cmds ]
        self.cmds = self.cmds + unique_cmds
