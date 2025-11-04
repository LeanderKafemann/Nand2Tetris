//Tells you the inner angle sum of an polygon with n sides
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
(LOOP)
@n
M=M-1
@180
D=A
@R1
M=D+M
@n
D=M
@LOOP
D;JGT

(END)
@END
0;JMP
