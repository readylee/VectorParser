#!/usr/bin/env python

import StreamProcessor as spp


class EncodedInputParser:
    
    streamProcessor = spp.StreamProcessor()    

    def ParseFileInput(self, dataFile):
        f = open(dataFile)
        for line in iter(f):
            self.__read(str(line))
        f.close()
                

    def WaitForInput(self):
        while True:
            try:
                # Note: Python 2.x can use raw_input, but 3.x only has input
                parseable = str(raw_input("Please enter encoded command string(s) to parse: "))
            except NameError:
                parseable = str(input("Please enter encoded command string(s) to parse: "))   
            except ValueError:
                print("Sorry, please enter a valid encoded string.")
                continue
            
            self.__HandleEncode(parseable)
            
    def __read(self, parseableStream=''):
        if('' != parseableStream):
            self.streamProcessor.ProcessStream(parseableStream) 
            
    def __HandleEncode(self, encodedString):
        if ('EXIT' == encodedString.upper()):
            exit(0)
        else:
            self.__read(str(encodedString))                               
