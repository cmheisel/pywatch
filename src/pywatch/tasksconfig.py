import sys
import os
import json

from pywatch.commandexecutor import CommandExecutor
from pywatch.filematcher import FileMatcher
from pywatch.watcher import Watcher


class TasksConfig( object ):
    def __init__( self, configDic, verbose = False ):
        self.ready = False
        self.verbose = verbose
        self.watchdir = configDic[ 'watchdir' ]
        self.cmds = {}
        self.matchers = []

        commands = configDic[ 'commands' ]
        matchers = configDic[ 'matchers' ]

        if commands is None:
            return

        for c in commands:
            self.cmds.update( { c : CommandExecutor( commands[c] ) } )

        for m in matchers:
            matcher = FileMatcher( m[ 're' ] )
            for mc in m[ 'commands' ]:
                if mc in self.cmds:
                    matcher.addCmd( self.cmds[ mc ] )
            self.matchers.append( matcher )

    def run( self ):
        w = Watcher( files=[ self.watchdir ], cmds=self.matchers, verbose=self.verbose )
        w.run_monitor()


