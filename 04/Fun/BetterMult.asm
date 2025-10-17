//Multiplicates R0 and R1 and saves the product in R2.
//Can also multiplicate any combination of negative and positive Numbers.

//Set RAM[2] to 0

@2
M=0

//Check if RAM[0] or RAM[1] are 0

@0
D=M
@End
D;JEQ

@1
D=M
@End
D;JEQ

//Check which one is bigger for less Time on the Additions and save that one on RAM[n]

@0
D=M
@1
D=D-M
@Right1
D;JGE

@1
D=M
@big
M=D
@0
D=M
@small
M=D
@Wrong1
0;JMP

(Right1)
@0
D=M
@big
M=D
@1
D=M
@small
M=D

(Wrong1)
//Do the Multiplication(Addition(LOOPED))
(LOOP1)

@big
D=M
@2
M=D+M
@small
M=M-1
@small
D=M
@End
D;JLE
@LOOP1
0;JMP

(End)
(LOOP)
@LOOP
0;JMP
