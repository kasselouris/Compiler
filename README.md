# **Minimal++ Compiler**

Minimal++ is a minimalistic programming language developed for the Compilers course of [cs.uoi.gr](https://www.cs.uoi.gr/?lang=en). It includes some interesting features that few languages support such as nested functions. It also includes pass by value and by reference, recursive calls, functions and procedures and many more. On the other hand Mininal++ is not supporting basic programmer tools such as for-loops or strings.

> For more details about Minimal++ check **doc** folder.

## Goal of the Project
I had to develop in Python language a fully functional compiler for Minimal++. Final language derived from compiler ready to assemble using MARS 4.5 [MIPS Assembler and Runtime Simulator](http://courses.missouristate.edu/KenVollmar/mars/)

The project was developed in 4 phases:
1) lexical and syntax analysis
2) intermediate code (and its equivalent in C)
3) semantic analysis and symbol table
4) Final code and report

## File extensions

### `.min`
Minimal++ files.

### `.int`
Intermediate code files.

### `.c`
Minimal++ code equivalent in C (doesn't support minimal++ programs with declared functions).

### `.asm`
Final code in assembly MIPS.

> To see examples of this files check **tests** folder.

## Symbol table
Here is an example output of symbol table(in our case the terminal output for test3.min)

<img src="https://github.com/kasselouris/Compiler/blob/main/assets/symbol_table.gif" height="600" />


## Python version
`3.6.9`

## Run
`python compiler.py *.min`
