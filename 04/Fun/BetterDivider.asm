//Devides R0 by R1 and saves result in R2 and rest in R3

@R2
M=0
@R3
M=0
@R0
D=M
@n
M=D
@R1
D=M
@END
D;JEQ
@m
M=D
@n
D=M
@NEG1
D;JLT
@m
D=M
@NEG2
D;JLT
(LOOP)
@m
D=M
@n
D=D-M
@REST
D;JGT
@m
D=M
@n
M=M-D
@R2
M=M+1
@LOOP
0;JMP



(REST)
@n
D=M
@R3
M=D
(END)
@END
0;JMP
