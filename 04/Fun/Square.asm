// can create up to an 256*256(radius=128) Square in the middle of the Screen
//Inner circle radius in R0 

//save startingpoint/top left middlepoint in RAM[n]
@R0
D=M
@END
D;JLE
@SCREEN
D=A
@4112
D=D+A
@n
M=D
//create startingsquare(2x2(radius=1))
A=D
M=-1
D=D+1
A=D
M=-1
@31
D=D+A
A=D
M=-1
D=D+1
A=D
M=-1
//save radius in RAM[m],RAM[l],RAM[o],RAM[p]
@R0
D=M
@m
M=D-1
D=M
@l
M=D
@o
M=D
M=D+M

//Fallunterscheidung für link-rechts-Bewegung
@16
D=A
@x
M=D
@l
D=M
@y
M=D
@l
M=0
(LOOPF)
@x
D=M
@y
M=M-D
@l
M=M+1

@LOOPF
D;JGT







@l
D=M
@p
M=D
M=D+M

//Move to top left corner of square
//Up
(LOOP1)
@m
D=M
@LOOP2
D;JLE
@32
D=A
@n
M=M-D
@m
M=M-1
@LOOP1
0;JMP

//Left
(LOOP2)





(END)
@END
0;JMP
