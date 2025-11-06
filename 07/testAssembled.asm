// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// add
@SP
AM=M-1    // SP = SP - 1; A = SP
D=M       // D = y (top)
@SP
AM=M-1    // SP = SP - 1; A = SP
M=M+D     // *SP = x + y
@SP
M=M+1     // SP = SP + 1