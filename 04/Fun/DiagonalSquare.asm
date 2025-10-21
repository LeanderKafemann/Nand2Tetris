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
