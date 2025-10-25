//creates a 45 degrees rotated square
//Outercircleradius in R0(1-128)

//clear screen
@8192
D=A
@clear
M=D
@SCREEN
D=A
@cleara
M=D
(CLEAR)
@clear
D=M
@GO
D;JEQ
@cleara
A=M
M=0
@cleara
M=M+1
@clear
M=M-1
@CLEAR
0;JMP

(GO)
//save radius in RAM[m], RAM[l], RAM[o]
@R0
D=M
@END
D;JLE
@128
D=D-A
@END
D;JLE
@R0
D=M
@m
M=D
@l
M=D
@o
M=D

//save middlepoint in RAM[n]
@SCREEN
D=A
@4111
D=D+A
@n
M=D

//Go to top middlepoint
(LOOP1)
@m
M=M-1
@32
D=A
@n
M=M-D
@m
D=M
@LOOP1
D;JLE

//define 32(16 left and 16 right) seperate types of lines 
@16384
D=-A
D=D-A
@LR1
M=D

@16384
D=-A
@LR2
M=D

@8192
D=-A
@LR3
M=D

@4096
D=-A
@LR4
M=D

@2048
D=-A
@LR5
M=D

@1024
D=-A
@LR6
M=D

@512
D=-A
@LR7
M=D

@256
D=-A
@LR8
M=D

@128
D=-A
@LR9
M=D

@64
D=-A
@LR10
M=D

@32
D=-A
@LR11
M=D

@16
D=-A
@LR12
M=D

@8
D=-A
@LR13
M=D

@4
D=-A
@LR14
M=D

@2
D=-A
@LR15
M=D

@LR16
M=-1

@RR1
M=1

@3
D=A
@RR2
M=D

@7
D=A
@RR3
M=D

@15
D=A
@RR4
M=D

@31
D=A
@RR5
M=D

@63
D=A
@RR6
M=D

@127
D=A
@RR7
M=D

@255
D=A
@RR8
M=D

@511
D=A
@RR9
M=D

@1023
D=A
@RR10
M=D

@2047
D=A
@RR11
M=D

@4095
D=A
@RR12
M=D

@8191
D=A
@RR13
M=D

@16383
D=A
@RR14
M=D

@32767
D=A
@RR15
M=D

@RR16
M=-1

//Draw upper half
(TOP)
@16
D=A
@Q1
M=D
@Q2
M=D
@Q3
M=D
@Q4
M=D
@Q5
M=D
@Q6
M=D
@Q7
M=D
@Q8
M=D

//Jump Algorithm
@LR1
D=M
@n
A=M
M=D
@n
M=M+1
@RR1
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR2
D=M
@n
A=M
M=D
@n
M=M+1
@RR2
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR3
D=M
@n
A=M
M=D
@n
M=M+1
@RR3
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR4
D=M
@n
A=M
M=D
@n
M=M+1
@RR4
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR5
D=M
@n
A=M
M=D
@n
M=M+1
@RR5
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR6
D=M
@n
A=M
M=D
@n
M=M+1
@RR6
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR7
D=M
@n
A=M
M=D
@n
M=M+1
@RR7
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR8
D=M
@n
A=M
M=D
@n
M=M+1
@RR8
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR9
D=M
@n
A=M
M=D
@n
M=M+1
@RR9
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR10
D=M
@n
A=M
M=D
@n
M=M+1
@RR10
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR11
D=M
@n
A=M
M=D
@n
M=M+1
@RR11
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR12
D=M
@n
A=M
M=D
@n
M=M+1
@RR12
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR13
D=M
@n
A=M
M=D
@n
M=M+1
@RR13
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR14
D=M
@n
A=M
M=D
@n
M=M+1
@RR14
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR15
D=M
@n
A=M
M=D
@n
M=M+1
@RR15
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

@LR16
D=M
@n
A=M
M=D
@n
M=M+1
@RR16
D=M
@n
A=M
M=D
@l
M=M-1
D=M
@BOTTOM
D;JLE

(BOTTOM)

(END)
@END
0;JMP
