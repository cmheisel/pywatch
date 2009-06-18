import sys

from optparse import OptionParser

from pywatch.watcher import Watcher

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
    options, args = parser.parse_args(args)

    cmds = [args[0], ]
    files = args[1:]
    w = Watcher(cmds=cmds, files=files, verbose=options.verbose)
    w.run_monitor()
