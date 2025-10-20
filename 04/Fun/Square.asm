// can create from 32*32(radius=16) up to an 256*256(radius=128) Square in the middle of the Screen
//Inner circle radius in R0 

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
//save startingpoint/top left middlepoint in RAM[n]
@R0
D=M
@15
D=D-A
@END
D;JLE
@SCREEN
D=A
@3632
D=D+A
@n
M=D

//create startingsquare(32x32(radius=16))
@32
D=A
@count
M=D

(START)
@count
D=M
@STOP
D;JLE
@n
A=M
M=-1
@n
M=M+1
A=M
M=-1
@31
D=A
@n
M=D+M
@count
M=M-1
@START
0;JMP

(STOP)
@SCREEN
D=A
@n
M=D
@4112
D=A
@n
M=D+M
//save radius in RAM[m],RAM[l],RAM[l2],RAM[m2]
@R0
D=M
@m
M=D-1
D=M
@l
M=D
@m2
M=D
M=D+M

//Fallunterscheidung für link-rechts-Bewegung
@16
D=A
@x
M=D
@l
D=M
@y
M=D
@l
M=0
(LOOPF)
@x
D=M
@y
M=M-D
@l
M=M+1
@y
D=M
@LOOPF
D;JGT
@l
D=M
@l2
M=D
M=D+M
@y
D=M
@rest
M=D

//einzelne Fälle
@rest
D=M
@REST0
D;JEQ

@rest
M=M-1
D=M
@REST1
D;JEQ

@rest
M=M-1
D=M
@REST2
D;JEQ

@rest
M=M-1
D=M
@REST3
D;JEQ

@rest
M=M-1
D=M
@REST4
D;JEQ

@rest
M=M-1
D=M
@REST5
D;JEQ

@rest
M=M-1
D=M
@REST6
D;JEQ

@rest
M=M-1
D=M
@REST7
D;JEQ

@rest
M=M-1
D=M
@REST8
D;JEQ

@rest
M=M-1
D=M
@REST9
D;JEQ

@rest
M=M-1
D=M
@REST10
D;JEQ

@rest
M=M-1
D=M
@REST11
D;JEQ

@rest
M=M-1
D=M
@REST12
D;JEQ

@rest
M=M-1
D=M
@REST13
D;JEQ

@rest
M=M-1
D=M
@REST14
D;JEQ

@rest
M=M-1
D=M
@REST15
D;JEQ

(REST0)
@0
D=A
@leftrest
M=D
@0
D=A
@rightrest
M=D
@CONTINUE
0;JMP

(REST1)
@1
D=A
@leftrest
M=D
@16384
D=-A
D=D-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST2)
@3
D=A
@leftrest
M=D
@16384
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST3)
@7
D=A
@leftrest
M=D
@8192
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST4)
@15
D=A
@leftrest
M=D
@4096
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST5)
@31
D=A
@leftrest
M=D
@2048
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST6)
@63
D=A
@leftrest
M=D
@1024
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST7)
@127
D=A
@leftrest
M=D
@512
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST8)
@255
D=A
@leftrest
M=D
@256
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST9)
@511
D=A
@leftrest
M=D
@128
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST10)
@1023
D=A
@leftrest
M=D
@64
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST11)
@2047
D=A
@leftrest
M=D
@32
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST12)
@4095
D=A
@leftrest
M=D
@16
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST13)
@8191
D=A
@leftrest
M=D
@8
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST14)
@16383
D=A
@leftrest
M=D
@4
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(REST15)
@32767
D=A
@leftrest
M=D
@2
D=-A
@rightrest
M=D
@CONTINUE
0;JMP

(CONTINUE)
//Move to top left corner of square
//Up
(LOOP1)
@m
D=M
@LOOP2
D;JLE
@32
D=A
@n
M=M-D
@m
M=M-1
@LOOP1
0;JMP

//Left
(LOOP2)
@l
D=M
@DRAW
D;JLE
@n
M=M-1
@l
M=M-1
@LOOP2
0;JMP

(DRAW)
@n
M=M-1
@m2
D=M
@m3
M=D

(LOOP3)
@m3
D=M
@AEND
D;JLE
@leftrest
D=M
@n
A=M
M=D
@32
D=A
@n
M=D+M
@m3
M=M-1
@LOOP3
0;JMP

(AEND)
@n
M=M+1
@l2
D=M
@FINAL
D;JLE
@m2
D=M
@m3
M=D
@m4
M=D
@2
D=A
@l2
M=M-D


(LOOP4)
@m3
D=M
@LOOP5
D;JLE
@n
A=M
M=-1
@32
D=A
@n
M=M-D
@m3
M=M-1
@LOOP4
0;JMP

(LOOP5)
@m4
D=M
@AEND
D;JLE
@n
A=M
M=-1
@32
D=A
@n
M=D+M
@m4
M=M-1
@LOOP5
0;JMP

(FINAL)
@m2
D=M
@END
D;JLE
@rightrest
D=M
@n
A=M
M=D
@32
D=A
@n
M=M-D
@m2
M=M-1
@FINAL
0;JMP

(END)
@END
0;JMP
