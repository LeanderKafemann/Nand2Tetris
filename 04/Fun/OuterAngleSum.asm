//Tells you the outer angle sum of an polygon with n sides
//n in R0
//anglesum in R1

@R1
M=0
@R0
D=M
D=D-1
D=D-1
@END
D;JLE

@n
M=D
@R0
D=M
@m
M=D
(LOOP1)
@m
M=M-1
@360
D=A
@R1
M=D+M
@m
D=M
@LOOP1
D;JGT

(LOOP2)
@n
M=M-1
@180
D=A
@R1
M=M-D
@n
D=M
@LOOP2
D;JGT

(END)
@END
0;JMP
