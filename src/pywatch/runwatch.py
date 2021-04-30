import os
import sys
import json
from optparse import OptionParser
from watcher import Watcher
from tasksconfig import TasksConfig

def main(args=None):
    """
    Used by the pywatch script to handle command-line
    args.
    """

    if not args:
        args = sys.argv[1:]

    usage = 'usage: %prog [options] "command" file1 file2 ...'
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="Output timestamp when commands are run.")
    parser.add_option("--version",
                      action="store_true",
                      dest="version",
                      default=False,
                      help="Output verion number and exit.")
    parser.add_option("--jsonconf",
                      dest="jsonconf",
                      help="Use advance JSON configuration file to run commands" )
    options, args = parser.parse_args(args)

    if options.version:
        print("pywatch {}".format(VERSION))
        sys.exit(0)

    confile = None
    if options.jsonconf is not None:
        # Uses the JSON file to configure the main dir and actions to take
        if not os.path.isfile( options.jsonconf ):
            print( "Not valid jsonconf file name" );
        else:
            confile = options.jsonconf
    elif os.path.isfile( ".tasksconfig.json" ):
        confile = ".tasksconfig.json"

    if confile is not None:
        cf = open( confile )
        try:
            jconf = json.load( cf )
        except ValueError:
            print("Invalid JSON")
            cf.close()
            exit()
        cf.close()
        tc = TasksConfig( jconf )
        tc.run()
    elif len(args) >= 2:
        # "Classic" operation mode
        cmds = [args[0], ]
        files = args[1:]
        w = Watcher(cmds=cmds, files=files, verbose=options.verbose)
        w.run_monitor()
        sys.exit(0)
    else:
        print(parser.error("You must provide a shell command and at least one file."))

if __name__ == "__main__":
    main()
