// R0 = n 
//Computes the nth Fibonacci number and saves it in R1

@R0
D=M
@n
M=D
@R1
M=1
@m
M=1
(LOOP)
@n
D=M
@Done
D;JLE
@n
M=M-1
@m
D=M
@R1
M=D+M
D=M
@m
M=D-M
@LOOP
0;JMP
(Done)
@Done
0;JMP
