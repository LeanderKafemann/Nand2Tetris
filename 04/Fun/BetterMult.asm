//Multiplicates R0 and R1 and saves the product in R2.
//Can also multiplicate any combination of negative and positive Numbers.

//Set RAM[2] to 0

@2
M=0

//Check if RAM[0] or RAM[1] are 0

@R0
D=M
@End
D;JEQ

@R1
D=M
@End
D;JEQ

@R0
D=M
@R_0
M=D
@R1
D=M
@R_1
M=D

//Check if inputs are negative
@R_0
D=M
@NEG1
D;JLT
@R_1
D=M
@NEG2
D;JLT
@SPEED1
0;JMP

(NEG1)
@R_1
D=M
@DNEG
D;JLT
@R_0
M=-M
@o
M=1
@SPEED
0;JMP

(NEG2)
@R_1
M=-M
@o
M=1
@SPEED
0;JMP

(DNEG)
@R_0
M=-M
@R_1
M=-M


//Check which one is bigger for less Time on the Additions and save that one on RAM[n]
(SPEED1)
@o
M=0
(SPEED)
@R_0
D=M
@R_1
D=D-M
@Right1
D;JGE

@R_1
D=M
@big
M=D
@R_0
D=M
@small
M=D
@Wrong1
0;JMP

(Right1)
@_R0
D=M
@big
M=D
@R_1
D=M
@small
M=D

(Wrong1)
//Do the Multiplication(Addition(LOOPED))
(LOOP1)

@big
D=M
@R2
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
@o
D=M
@LOOP
D;JLE
@R2
M=-M
(LOOP)
@LOOP
0;JMP
