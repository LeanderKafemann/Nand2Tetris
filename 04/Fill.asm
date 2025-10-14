// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.


(LOOP)

@SCREEN
D=A
@0
M=D

//KBD-Inputs


@KBD           
D=M
@TRUE
D;JGT
@FALSE
D;JLE

(TRUE)
(SHORTLOOP1)
D=-1
@0
A=M
M=D
@KBD
D=M
@LOOP
D;JEQ
@0
M=M+1
@SHORTLOOP1
0;JMP

(FALSE)
(SHORTLOOP2)
D=0
@0
A=M
M=D
@KBD
D=M
@LOOP
D;JGT
@0
M=M+1
@SHORTLOOP2
0;JMP





