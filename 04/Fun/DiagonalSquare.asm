//creates a 45 degrees rotated square
//Outercircleradius in R0(1-128)

//clear screen
@8192
D=A
@clear
M=D
@SCREEN
D=A
@cleara
M=D
(CLEAR)
@clear
D=M
@GO
D;JEQ
@cleara
A=M
M=0
@cleara
M=M+1
@clear
M=M-1
@CLEAR
0;JMP

(GO)
//save radius in RAM[m], RAM[l], RAM[o]
@R0
D=M
@END
D;JLE
@128
D=D-A
@END
D;JLE
@R0
D=M
@m
M=D
@l
M=D
@o
M=D

//save middlepoint in RAM[n]
@SCREEN
D=A
@4111
D=D+A
@n
M=D






(END)
@END
0;JMP
