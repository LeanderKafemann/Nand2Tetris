//Just a checkboard on the screen

@SCREEN
D=A
@n
M=D


@256
D=A
@m
M=D
@n
M=M-1

(BIGLOOP)
@m
D=M
@REALBOARD
D;JLE
@m
M=M-1


@2
D=A
@q
M=D

(TINYLOOP)
@8
D=A
@p
M=D

(SMALLLOOP)
@p
D=M
@MEDIUMLOOP
D;JLE
@n
A=M
M=-1
@n
M=M+1
@p
M=M-1
@SMALLLOOP
0;JMP

(MEDIUMLOOP)
@q
M=M-1
D=M
@BIGLOOP
D;JLE
@16
D=A
@n
M=D+M
@TINYLOOP
0;JMP


(REALBOARD)
@REALBOARD
0;JMP
