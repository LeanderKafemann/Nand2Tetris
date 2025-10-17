//Devides R0 by R1 and saves result in R2 and rest in R3
//Also works for any combination of negative and positive numbers

@R2
M=0
@R3
M=0
@o
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

(LOOP1)
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
@LOOP1
0;JMP

(NEG1)
@m
D=M
@DNEG
D;JLT

(LOOP2)
@m
D=M
@n
D=D+M
@REST
D;JGT
@m
D=M
@n
M=D+M
@R2
M=M-1
@LOOP2
0;JMP

(NEG2)
@n
M=-M
@m
M=-M
@o
M=1
@LOOP2
0;JMP

(DNEG)
@n
M=-M
@m
M=-M
@o
M=1
@LOOP1
0;JMP

(REST)
@o
D=M
@REVERSE
D;JGT
@n
D=M
@R3
M=D
@END
0;JMP

(REVERSE)
@n
D=M
@R3
M=-D

(END)
@END
0;JMP
