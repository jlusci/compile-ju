Compile - JU
==========

A compiler for my language, JU, including a web interface to demonstrate the evaluation.

## Quick start with "Hello, world!":
* Main python lexer and parser: PLYex.py and drjb_parser.py (note - you must make sure you have the ply.lex python module installed) 
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
* reassign variables (preserving math order of operations): y = y + 1;
* call functions previously defined with parameters: new\_fun(2);
* if statements: if ( \<expression\> ) { \<block\> } else { \<block\> }
* for loops: for(\<var\_def\>; \<expression\>; \<var\_assign\> ) { \<block\> }
* while loops: while( \<expression\> ) { \<block\> }
* print statements: print \<expression\>
 
## Let the compiling begin:
The main components of my compiler consists of a lexer and a parser. Here I will go through the main features of each.
### Lexing:
Any language is made up of "tokens" where a token can be thought of as the smallest individual unit of your language. Lexical analysis involves scanning through an input script and recognizing these tokens. To create the token stream from your input program, the lexer uses the Python module PLY (Python Lex-Yacc) in PLYex.py file. In PLYex.py, the token names and reserved words for the language are defined and the lexer is built. The special characters are defined using regular expressions and all of the functions starting with 't\_' indicate tokens where special action is taken. For example, in the JU language, comments are defined the same way they are in JavaScript by the token '\\' and I have written a function in PLYex.py that looks for this special token and discards it when it is found, since comments are not a part of the functionality of the input file. Once your tokens and any special actions for your tokens are defined, you can then build the lexer using the lex() method in the PLY module.
Once the lexer is built, the lexer is then able to read in your input script and tokenize it, creating token objects that carry information about the type and value of the token (as well as line number and character positions for error reporting). PLYex 
