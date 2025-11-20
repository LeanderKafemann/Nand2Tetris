// push constant 787
@787
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 787
@787
D=A
@SP
A=M
M=D
@SP
M=M+1
// arithmetic add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
// push constant 787
@787
D=A
@SP
A=M
M=D
@SP
M=M+1
// arithmetic and
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M&D
@SP
M=M+1
// push constant 787
@787
D=A
@SP
A=M
M=D
@SP
M=M+1
// arithmetic sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
// pop static 4
@SP
AM=M-1
D=M
@Test.4
M=D
// push constant 6969
@6969
D=A
@SP
A=M
M=D
@SP
M=M+1
// push static 4
@Test.4
D=M
@SP
A=M
M=D
@SP
M=M+1
// arithmetic sub
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
// pop static 3
@SP
AM=M-1
D=M
@Test.3
M=D
// push constant 787
@787
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop static 3
@SP
AM=M-1
D=M
@Test.3
M=D
// push static 3
@Test.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// push static 4
@Test.4
D=M
@SP
A=M
M=D
@SP
M=M+1
// arithmetic add
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
// push constant 787
@787
D=A
@SP
A=M
M=D
@SP
M=M+1
// arithmetic eq
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@EQ_TRUE$0
D;JEQ
@SP
A=M
M=0
@EQ_END$1
0;JMP
(EQ_TRUE$0)
@SP
A=M
M=-1
(EQ_END$1)
@SP
M=M+1
// pop temp 0
@SP
AM=M-1
D=M
@R5
M=D
// push constant 13187
@13187
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop temp 7
@SP
AM=M-1
D=M
@R12
M=D
