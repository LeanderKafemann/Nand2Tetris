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

@n
M=M+1

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
@q
D=M
@BIGLOOP
D;JLE
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
@16
D=A
@n
M=D+M
@q
M=M-1
@TINYLOOP
0;JMP


(REALBOARD)
@REALBOARD
0;JMP
