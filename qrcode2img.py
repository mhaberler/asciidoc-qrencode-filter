#!/usr/bin/env python2
"""Qrcode filter script to generate QRCode images from ascii
Requirement: 
- qrencode needs to be installed http://fukuchi.org/works/qrencode/index.en.html

Tested on Archlinux. You might have to change the first line of this program to make it work under other
distribs. (python2)

Copyright (C) 2011 Jean-Marc Temmos. Free use of this software is
granted under the terms of the GNU General Public License (GPL).
"""

usage = "%prog [options] inputfile"
__version__ = '0.1'

import os, sys, tempfile
from optparse import *


#
# Configuration constants
#

#
# Global data
#
verbose = False


#
# Helper functions and classes
#
class AppError(Exception):
    """Application specific exception."""
    pass


def print_verbose(line):
    if verbose:
        sys.stderr.write(line + os.linesep)


def systemcmd(cmd):
    if not verbose:
        cmd += " 2>%s" % os.devnull
    cmd += " >&2" # redirect verbose output to stderr
    print_verbose("Exec: %s" % cmd)
    if os.system(cmd):
        raise AppError, "failed command: %s" % cmd


#
# Application init and logic
#
class Application():
    """Application class"""

    def __init__(self):
        """Process commandline arguments"""
        global verbose
        parser = OptionParser(usage, version="%%prog %s" % __version__)
        parser.add_option("-o", "--outfile", help="Output file name")
        parser.add_option("-s", "--size", type=float, help="Image pixel size. default = 3")
        self.options, args = parser.parse_args()
        print_verbose("Runing filter script %s" % os.path.realpath(sys.argv[0]))
        if len(args) != 1:
            parser.error("Invalid number of arguments")
        self.infile = args[0]
        if self.options.outfile is None:
            if self.infile == '-':
                parser.error("OUTFILE option must be specified")
            self.options.outfile = "%s.png" % os.path.splitext(self.infile)[0]
            print_verbose("Output file is %s" % self.options.outfile)


    def run(self):
        """Core logic of the application"""
        outfile = os.path.abspath(self.options.outfile)
        outdir = os.path.dirname(outfile)
        if not os.path.isdir(outdir):
            raise AppError, 'directory does not exist: %s' % outdir
        temp = None
        try:
            if self.infile == '-':
                source = sys.stdin.read()
                temp = tempfile.NamedTemporaryFile(delete=False)
                infile = temp.name
                print_verbose("Temporary input file is %s" % infile)
                temp.write(source)
                temp.close()
            else:
                infile = self.infile
            options = ""
            if self.options.size:
                options += " -s %f" % self.options.size
            #systemcmd('zint -b 58 -i "%s" -o "%s" %s' % (
            #          infile, outfile, options))

            systemcmd('qrencode %s -o "%s" < "%s" ' % (
                      options,outfile,infile))
                      
        finally:
            if temp:
                os.remove(temp.name)
        # To suppress asciidoc 'no output from filter' warnings.
        if self.infile == '-':
            sys.stdout.write(' ')


#
# Main program
#
if __name__ == "__main__":
    """Main program, called when run as a script."""
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        sys.exit("Ouch!")
    except Exception, e:
        sys.exit("%s: %s\n" % (os.path.basename(sys.argv[0]), e))

