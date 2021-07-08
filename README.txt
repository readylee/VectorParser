
******** ABOUT THIS PROGRAM *******

To run the program (from the command line):

USAGE: python VectorParser.py [parseableStreamsFilePath]
parseableStreamsFilePath = path to file containing streams to parse, line by line; 

If there is no argument passed when running the program, then script will wait for user
to enter encoded strings on the command line and output the processed result. Entering the string 'EXIT' 
will simply end the program.

This program has been tested on Python 2.7

-Rodney Lee Jones Jr.

This module processes encoded data streams.
The data will describe some set of basic commands for a vector based drawing application/system. 
This system employs a pen based model, where the pen can be moved, raised, or lowered. 
If the pen is moved while lowered, it draws along the line of motion, with the current color. 
If the pen is moved while raised, then no drawing occurs. 

The basic commands supported in this system/language are: 

Clear the drawing (and reset all parameters) 
Raise (Up) or lower (Down) the pen
Change current color/transparency
Move the pen

Commands are represented in the data stream by a single (un-encoded) op-code byte, 
which can be identified by always having its most significant bit set, 
and a command will be followed by 0 or more bytes containing encoded data values. 

Any unrecognized commands encountered in the input stream shall be ignored. 

With this module, the encoded stream is merely converted to simple text command output...

Sample input (to draw a blue square):
F090400047684F5057384000A040004000417F417FC040004000804001C05F204000400001400140400040007E405B2C4000804000

Expected Output:
CLR;
CO 0 0 255 255;
MV (0, 0);
PEN DOWN;
MV (4000, 0)(4000, -8000)(-4000, -8000)(-4000, 0)(-500, 0);
PEN UP; 


Extended Command Reference:

1. Clear 

Command: CLR
Op-code:  F0
Parameters: (none)
Output CLR;\n


2. Pen Up/Down 

Command: PEN
Op-code: 80
Parameters: 0 = pen raised up; any other value = pen is lowered down 
Output: either PEN UP;\n or PEN DOWN;\n


3. Set Color 

Command: CO
Op-code: A0
Parameters: R G B A 
			Red, Green, Blue, Alpha values, each in the range 0..255. 
			All four values required.
Output: CO {r} {g} {b} {a};\n (where each r/g/b/a value formatted as integer 0 - 255

Changes the color or transparency (alpha) of the pen. Color change takes effect next time the pen is moved. 
After clearing a drawing with the CLR; command, the current color is reset to black (0,0,0,255). 


4. Move Pen 

Command: MV
Op-code: C0
Parameters: dx0 dy0 [dx1 dy1 .. dxn dyn] 
			Any number of (dx,dy) pairs.
Output: If pen's up, move pen to the final coordinate's position  
		If pen's down: MV (xo, y0) (x1, y1) [... (xn, yn)];\n

