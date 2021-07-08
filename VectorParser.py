#!/usr/bin/env python

####
#### Copyright (c) Rodney Lee Jones Jr. All Rights Reserved.
####

sUsageStatement = """
USAGE: python VectorParser.py [parseableStreamsFilePath]
parseableStreamsFilePath = path to file containing streams to parse, line by line; 

If there is no argument passed when running the program, then script will wait for user
to enter encoded strings from stdin and output the parsed result. Entering the string 'EXIT' 
will simply end the program.
"""

import sys, os, string

import EncodedInputParser as eip                                

def main(argv):
    argLength = len(argv)
    parser = eip.EncodedInputParser()
    if (argLength > 1):
        if(2 != argLength):
            print sUsageStatement
            exit(0)
        else:
            try:
                parser.ParseFileInput(argv[1])
            except:
                print "Unexpected error: ", sys.exc_info()[0]
                raise    
    else:
        parser.WaitForInput()       


if __name__ == "__main__":
    main(sys.argv)
