import re 

class FileMatcher(object): 
    """ Uses a regex to match a file (with the full path),
        and run commands on it in case it matches the regex """ 
    
    def __init__( self, matchRE ): 
        """ matchRE must be a re string """ 
        self.matchRE = re.compile( matchRE ) 
        if self.matchRE is None:
            print( "Non valid regex: %s" % matchRE )
        self.cmds = [] 

    def addCmd( self, cmd ):
        """ adds a CommandExecutor to run when a file matches """ 
        self.cmds.append( cmd ) 

    def runCmds( self, filePath ): 
        """ checks if a filePath matches the regex and if so it runs
            the commands with the filePath as a parameter """ 
        m = self.matchRE.match( filePath )
        if m is not None: 
            for c in self.cmds: 
                c.execute( filePath ) 
            return True
        return False 
