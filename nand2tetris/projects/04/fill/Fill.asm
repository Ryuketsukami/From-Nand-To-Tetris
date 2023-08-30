// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

@8192
D=A
@finish
M=D

(Start)

@KBD
D=M

@White
D; JEQ

@temp
M=0

(BLoop)
@SCREEN
D=A
@temp
D=D+M

A=D
M=-1

@1
D=A
@temp
M=D+M

D=M
@finish
D=D-M
@BLoop
D; JNE

@Start
0; JMP


(White)

@temp
M=0

(Loop)
@SCREEN
D=A
@temp
D=D+M

A=D
M=0

@1
D=A
@temp
M=D+M

D=M
@finish
D=D-M
@Loop
D; JNE

@Start
0; JMP



