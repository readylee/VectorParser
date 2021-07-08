#!/usr/bin/env python

from __future__ import division

class OutputFormatter:
    minCoord, maxCoord = 0, 0
    opcodeCommandPairs, paramRules, staticOutputs = {}, {}, {}
    penUp = True
    currentLoc = [0,0] 
    previousLoc = [0,0]
    currentColorSet = [0,0,0,255]
    outOfRangeLoc = []
    output = ''
    
    def __init__(self, borderMin, borderMax):
        self.minCoord = borderMin
        self.maxCoord = borderMax
        self.__InitparamRules()
        self.__InitStatics()
        self.__ResetAll() 
        
    def HandleClr(self):
        self.__ResetAll()
        self.SetOutput("CLR","default")         
    
    #custom handle method defnitions begin here
    def HandlePen(self, decoded=[]):
        if(0 != decoded[0]):
            self.penUp = False
            self.SetOutput("PEN", "default")
        else:
            self.penUp = True
            self.SetOutput("PEN", "0")

    def HandleCo(self, decoded=[]):
        currentColorSet = decoded
        self.SetOutput("CO", "", decoded)
	
    ## TODO: fix coord pairs to acknowledge edge (use minCoord, maxCoord)
    def HandleMv(self, decodedPairs=[]):
        mvOutput = ""
        while decodedPairs:
            newCoords = decodedPairs[:2]      
            mvOutput += str(self.__doMvLogic(newCoords))  
            decodedPairs = decodedPairs[2:]
        self.SetOutput("MV", mvOutput)        
    
    def __doMvLogic(self,coords=[]):
        xCoord = coords[0]+self.currentLoc[0]
        yCoord = coords[1]+self.currentLoc[1]
        if not self.CoordsInRange(xCoord, yCoord):
            return self.__LeaveRangeAtPoint(xCoord,yCoord)
        elif not self.CoordsInRange(self.currentLoc[0], self.currentLoc[1]):
            self.penUp = True
            return self.__ReEnterRangeAtPoint(xCoord, yCoord) 
        else:
            self.previousLoc = self.currentLoc
            self.currentLoc = [xCoord, yCoord]
            return format(str(tuple(self.currentLoc)))    
        
    def __ReEnterRangeAtPoint(self, xVal, yVal):
        xEntryCoord, yEntryCoord = self.currentLoc[0], self.currentLoc[1]
        entryLocOutput = ''
        self.previousLoc = self.currentLoc    
        self.currentLoc = [xVal, yVal]
        currentSlope = CalcSlope(self.previousLoc,self.currentLoc)
        yIntercept = CalcIntercept(self.previousLoc,currentSlope)
        if (self.previousLoc[0] > self.maxCoord):
            xEntryCoord = self.maxCoord
            y = currentSlope * xEntryCoord + yIntercept
            entryLoc = [xEntryCoord, y]          
            entryLocOutput += self.MvCustomOutput(str(tuple(entryLoc)))
            entryLocOutput += self.staticOutputs["PEN"]["default"]+";\n"
            entryLocOutput += self.MvCustomOutput(str(tuple(self.currentLoc)),True)
            self.penUP = False
        elif (self.previousLoc[0] < self.minCoord):
            xEntryCoord = self.minCoord
            y = currentSlope * xEntryCoord + yIntercept
            newLoc = [xEntryPoint, y]          
            entryLocOutput += str(tuple(newLoc))
            entryLocOutput += ";\n"
            entryLocOutput += self.staticOutputs["PEN"]["default"]
            self.penUP = False 
        return entryLocOutput
              
    def CoordsInRange(self,x,y):
        return (self.minCoord <= x <= self.maxCoord and self.minCoord <= y <= self.maxCoord)
    
    def __LeaveRangeAtPoint(self, xVal, yVal):
        outOfRangeLoc = [xVal, yVal]
        xExitCoord, yExitCoord = 0, 0
        exitLocOutput = ''
        self.previousLoc = self.currentLoc    
        self.currentLoc = outOfRangeLoc
        currentSlope = CalcSlope(self.previousLoc,self.currentLoc)
        yIntercept = CalcIntercept(self.previousLoc,currentSlope)
        if (xVal > self.maxCoord):
            xExitCoord = self.maxCoord
            y = currentSlope * xExitCoord + yIntercept
            newLoc = [xExitCoord, y]
            exitLocOutput += str(tuple(newLoc))
            exitLocOutput += ";\n"
            exitLocOutput += self.staticOutputs["PEN"]["0"]+";\n"
            self.penUP = True
        elif (xVal < self.minCoord):
            xExitCoord = self.minCoord
            y = currentSlope * xExitCoord + yIntercept
            newLoc = [xExitCoord, y]
            exitLocOutput += str(tuple(newLoc))
            exitLocOutput += ";\n"
            exitLocOutput += self.staticOutputs["PEN"]["0"]
            self.penUp = True
        if (yVal > self.maxCoord):
            yExitCoord = self.maxCoord        
        elif (yVal < self.minCoord):
            yExitCoord = self.minCoord      
        return exitLocOutput                     

    def CoCustomOutput(self, rgba=[]):
        return "CO {} {} {} {};\n".format(rgba[0],rgba[1],rgba[2],rgba[3])
    
    def MvCustomOutput(self, valStr='', withoutEnding=False):
        if withoutEnding:
            return "MV {}".format(valStr)
        return "MV {};\n".format(valStr)
        
    def opcodes(self):
        return self.opcodeCommandPairs.keys()         
    
    def SetOutput(self, command="", val="", valSet=[]):
        if("" == command):
            self.output = ''
        elif("CO" == command):
            self.output += self.CoCustomOutput(valSet)
        elif("MV" == command):
            self.output += self.MvCustomOutput(val)
        else:
            self.output += self.staticOutputs[command][val]+";\n"        
          
    def __InitparamRules(self):
        self.opcodeCommandPairs = {'F0':"CLR", '80':"PEN", 'A0':"CO", 'C0':"MV"}
        self.paramRules["CLR"] = { "size" : 0, "handle" : self.HandleClr }
        self.paramRules["PEN"] = { "size" : 1, "handle" : self.HandlePen }
        self.paramRules["CO"] = { "size" : 4, "handle" : self.HandleCo }
        self.paramRules["MV"] = { "size" : -1, "handle" : self.HandleMv }       

    # static output "templates" for non-dynamic command outputs
    def __InitStatics(self):
        self.staticOutputs["CLR"] = { "default" : "CLR" }
        self.staticOutputs["PEN"] = { "0" : "PEN UP", "default" : "PEN DOWN" }
        
    def __ResetAll(self):
        self.currentLoc = [0,0]
        self.penUp = True
        self.currentColorSet = [0,0,0,255]
        self.outOfRangeLoc = []
        self.output = ''                          
    
def CalcSlope(pointA=[],pointB=[]):
    try:
        return (pointA[1] - pointB[1])/(pointA[0] - pointB[0])
    except ZeroDivisionError:
        return 0    
    
def CalcIntercept(myLoc=[],slope=0.0):
    return int(myLoc[1]) - (slope * int(myLoc[0]))    
