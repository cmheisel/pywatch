import os
import sys

class CommandExecutor(object):
    """
        Executes a command having a file as a paramer.

        An environment variable can be referred with : %(ENV_VAR_NAME)s

        A dictionary with custom variables can be added and it
        generates shortcuts for easy substitution in the command string
        from the target File / Directory name

        %(P)s -> the Path for the file
        %(F)s -> the File name alone
        %(FF)s -> the Fullpath and File name
        %(SF)s -> Striped File name without file extension
        %(EXT)s -> file EXTension
        %(FSF)s -> Fullpath Striped File ( without extension )


        %(BPC0)s -> (Backward Path Component)last path component
        %(BPC1)s -> previous one
                    ...
        %(PC0)s ->  first path component
        %(PC1)s ->  next one
                    ...

        %(P2PBC0) -> (Path To Patch Backward Component 0 )
                    ...

        %(P2PC0) -> (Path To Patch Component 0)

    """
    def __init__( self, cmd, customenv = {}, verbose = True ):
        self.verbose = verbose
        self.cmd = cmd
        self.customenv = {}
        self.customenv.update( os.environ )
        self.customenv.update( customenv )

    def constructDictionary( self, fullPath ):
        vdic = {}
        vdic.update( self.customenv )
        vdic[ 'FF' ] = fullPath

        # fill the basic file info
        if os.path.isdir( fullPath ):
            vdic['F'] = ''
            vdic['EXT'] = ''
            vdic['SF'] = ''
            vdic['P'] = fullPath
        else:
            vdic['F'] = os.path.basename( fullPath )
            spext = os.path.splitext( vdic['F'] )
            if len( spext ) >= 2:
                vdic['EXT'] = spext[-1]
            else:
                vdic['EXT'] = ''
            vdic['SF'] = vdic['F'][:-len( vdic['EXT'])]
            vdic['P'] = os.path.split( fullPath )[0]

        vdic['FSF'] = os.path.sep.join( [ vdic['P'], vdic['SF'] ] )

        comps = vdic['P'].split( os.path.sep )
        n = len( comps )
        idx = 0


        if os.path.sep == '/':
            accumC = ['']
        else:
            accumC = []

        for c in comps:
            accumC.append( c )

            k = 'PC' + str( idx )
            bk = 'BPC' + str( n - idx -1 )
            fk = 'P2' + k
            fbk = 'P2' + bk
            vdic[ k ] = vdic[ bk ] = c
            vdic[ fk ] = vdic[ fbk ] = os.path.sep.join( accumC )
            idx = idx + 1
        return vdic

    def pathToPrefix( self, fullPath, levels = 2 ):
        components = fullPath.split( '/' )
        components = components[-levels:]
        return '_'.join( components )

    def execute( self, filePath ):
        filePath = os.path.abspath( filePath )
        s = self.constructDictionary( filePath )
        print(self.cmd)
        c = self.cmd % s
        if self.verbose :
            print(c)
        os.system( c )

