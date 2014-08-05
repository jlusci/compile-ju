Compile - JU
==========

A compiler for my language, JU! 

## Quick start with "Hello, world!":
* Main python lexer and parser: PLYex.py and drjb_parser.py * 
* Input JU files include the .ju extension

To run and evaluate the compiler, first clone the repo, navigate to the main directory and type the following into the terminal:

	python drjb_parser.py hello.ju 
	(or any other .ju file if you are bored with "Hello, world!")
Congrats! You have compiled your first JU program! Now let's go through how it all works.

## Syntax and grammar rules for JU language:
You may have noticed some similarities between JU and Python and Javascript. This is no accident! I took parts of both languages that I liked and mashed them together. Here is an easy guide with examples to how to create your code. Note that all expressions must end with a semicolon.

* define functions: function main(){ \<block\> }
* declare variables: var y = 2;
     (in place of 2 you can also define strings, ints, floats, math expressions, lists, and dictionaries)
* reassign variables: y = y + 1;
* call functions previously defined with parameters: new\_fun(2);
* if statements: if ( \<expression\> ) { \<block\> } else { \<block\> }
* for loops: for(\<var\_def\>; \<expression\>; \<var\_assign\> ) { \<block\> }
* while loops: while( \<expression\> ) { \<block\> }
* print statements: print \<expression\>
