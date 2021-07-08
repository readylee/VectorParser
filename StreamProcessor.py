#!/usr/bin/env python

import MultiTermSearch as mtSearch
import OutputFormatter as oViews

## @var sOffsetVal
## Shared value for customEncode, customDecode in this module.
## Added to raw value before encoding, 
## subtracted during decoding.
sOffsetVal = 8192   

## Encodable/field range is
## between sMinEncodable and sMaxEncodable.
sMinEncodable = -8192
sMaxEncodable = 8191

sUnexpectedErrorMsg = "Unexpected exception!"

class StreamProcessor: 
    byteSize = 4
    currentStream, viewsObj = '', ''
    
    def __init__(self):
        self.viewsObj = oViews.OutputFormatter(sMinEncodable, sMaxEncodable)
        mtSearch.initSearch(self.viewsObj.opcodes())
        
    def ProcessStream(self, dataStream=''):
        self.currentStream = dataStream
        self.viewsObj.SetOutput('')
        # resultsList = list of dicts
        # containing indices where commands appear in the stream, and each command
        # ex. {"index":0,"term":F0}
        resultsList = mtSearch.findTerms(dataStream)
        resultsListLength = len(resultsList)
        if (0 < resultsListLength):
            print self.__ParseResults(resultsList, resultsListLength)
        else:
            print "no commands found in stream"
    
    def __ParseResults(self, results={}, resultsLength=0):
        for x in range(resultsLength):
            currentIndex = results[x]["index"]
            currentOpcode = results[x]["term"]
            paramStart = currentIndex + len(currentOpcode)
            if (x < (resultsLength - 1)):
                nextIndex = results[x+1]["index"]
            else:
                nextIndex = None    
            self.__SetOutput(currentOpcode, self.currentStream[paramStart:nextIndex])
        return self.viewsObj.output 
    
    def __SetOutput(self, opcode='', paramString=''):
        commandName = self.viewsObj.opcodeCommandPairs[opcode.upper()]    
        self.__ParseParams(commandName, paramString)       
        
    def __ParseParams(self, currentCommand='', encodedParams=''):
        expectedAmtParams = self.viewsObj.paramRules[currentCommand]["size"]
        if (expectedAmtParams > 0):
            decodedParams = []
            for y in range(expectedAmtParams):
                myByte = encodedParams[:self.byteSize]
                decodedParams.append(customDecode(myByte[2:], myByte[:2]))
                encodedParams = encodedParams[self.byteSize:]
            self.__HandleParams(currentCommand, decodedParams)       
        elif (expectedAmtParams < 0):
            decodedParams = []
            # if expectedAmtParams less than 0
            # this means amount of params can vary
            # so we divide param string (encoded bytes) 
            # by byteSize to determine list length
            paramListLength = len(encodedParams)/self.byteSize
            for z in range(paramListLength):
                myByte = encodedParams[:self.byteSize]
                decodedParams.append(customDecode(myByte[2:], myByte[:2]))
                encodedParams = encodedParams[self.byteSize:]
            self.__HandleParams(currentCommand, decodedParams)
        elif (0 == expectedAmtParams):
            self.viewsObj.paramRules[currentCommand]["handle"]()      
        else:
            pass                                
        
    def __HandleParams(self, currentName='', decoded=''):
        self.viewsObj.paramRules[currentName]["handle"](decoded)


## Returns a hex value for a given input string 
def hex2int(hexString):
    return int(hexString,16)

## @fn customDecode(lBits,hBits) 
## Decoding function to reverse an encoded result of the customEncode function in this module 
## using the 2 segments of the encoded/4-digit hex value string
## @param lowBits The low(rightmost) byte segment, 2 digits long (range: 00 - ff)
## @param hiBits The high(leftmost) byte segment, 2 digits long (range: 00 - ff)
## @returns an integer value
def customDecode(lowBits,hiBits):
    if (len(lowBits) != 2 or len(hiBits) != 2):
        return "Invalid decode argument(s) provided: '{}','{}'".format(lowBits,hiBits)
    try:
        hBits = hex2int(hiBits.ljust(4,'0'))
        lBits = hex2int(lowBits.rjust(4,'0'))
        intermediateVal = lBits + (hBits >> 1)
    except (TypeError, ValueError):
        return "Invalid decode argument(s) provided: '{}','{}'".format(lowBits,hiBits)
    except:
        return sUnexpectedErrorMsg
    return intermediateVal - sOffsetVal
    
## @fn customEncode(inputVal)
## Creates a custom encoding of the input
## @param inputVal an integer value between -8192 and +8192
## @returns a 4-digit hex value string 
def customEncode(inputVal):
    ## max hex values for byte segments
    lowBitsRange = 0x007F
    hiBitsRange = 0x3F80
    try:
        myVal = int(inputVal)
    except ValueError:
        return "Invalid input: {}. Must be an integer between {} & {}.".format(inputVal,sMinEncodable,sMaxEncodable)
    except:
        return sUnexpectedErrorMsg
    if (myVal > sMaxEncodable or myVal < sMinEncodable):
        return "Invalid input: {}. Must be an integer between {} & {}.".format(inputVal,sMinEncodable,sMaxEncodable)
    myVal = int(myVal + sOffsetVal)
    hBits = myVal & hiBitsRange
    lBits = myVal & lowBitsRange
    resVal = lBits + (hBits << 1)
    return format(resVal, '04x')                          
