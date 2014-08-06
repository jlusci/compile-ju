Compile - JU
==========

A compiler for my language, JU, including a web interface to demonstrate the evaluation.

## Quick start with "Hello, world!":
* Main Python lexer and parser: PLYex.py and drjb_parser.py (note - you must make sure you have the ply.lex python module installed) 
* Input JU files include the .ju extension

To run and evaluate the compiler, first clone the repo, navigate to the main directory and type the following into the terminal:

	python drjb_parser.py hello.ju 
	(or any other .ju file if you are bored with "Hello, world!")
Congrats! You have compiled your first JU program! Now let's go through how it all works.

## Syntax and grammar rules for JU language:
You may have noticed some similarities between JU and Python and JavaScript. This is no accident! I took parts of both languages that I liked and mashed them together. Here is an easy guide with examples to how to create your code. Note that expressions must end with a semicolon.

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
Any language is made up of "tokens" where a token can be thought of as the smallest individual unit of your language. Lexical analysis involves scanning through an input script and recognizing these tokens. To create the token stream from your input program, the lexer uses the Python module PLY (Python Lex-Yacc) in PLYex.py file. In PLYex.py, the token names and reserved words for the language are defined and the lexer is built. The special characters are defined using regular expressions and all of the functions starting with 't\_' indicate tokens where special action is taken. For example, in the JU language, comments are defined the same way they are in JavaScript by the token '\\' and I have written a function in PLYex.py that looks for this special token and discards it when it is found, since comments are not a part of the functionality of the input file. Once your tokens and any special actions for your tokens are defined, you can then build the lexer using the lex() method in the PLY module. Once the lexer is built, the lexer is then able to read in your input script and tokenize it, creating token objects that carry information about the type and value of the token (as well as line number and character positions for error reporting). PLYex then passes this token list to the parser, drjb_parser.py.

### Parsing:
This is where the magic happens! During the parsing step, the compiler checks your code to ensure that all language syntactical rules have been obeyed. The end result of this step is the creation of the abstract syntax tree (AST) representation of your JU program which can then be evaluated (in Python at the interpreter stage) or compiled through to assembly code. Let's look in more detail at the parsing process.

My JU language is parsed using a technique called recursive descent. This is a top-down process that relies on mutually recursive functions where each one parses a specific grammar rule. Traditionally, it is difficult to preserve order of operations using recursive descent processes and many techniques exist where such precedence is preserved. The technique that I implemented is what is known as a "classic" solution. In this method, order of precedence is defined through recursive calls to the parsing functions, starting with parse\_expression(). The level of precedence is built into this function such that function calls and list indexing occur with the highest precedence, followed by multiplication, division, and modulus at the next level, addition and subtraction next, and finally comparison operators. This is also where lists, dictionaries, and strings are defined. The way that the functions are structured, all expressions in your JU code will recursively go through parse\_expression(). Each parsing step creates and returns a node in the AST which will later be evaluated. The parsing was the trickiest part of the compiler-writing process. Each time higher-order precedence rules were introduced, parse\_expression() was modified to account for these changes, while still maintaining its previous functionality. 

### Evaluation and Emission of Results:
My compiler includes an interpreter that evaluates the AST recursively, starting with the top program node. This was implemented to ensure that the parsing techniques were producing what was expected through the JU language as an intermediate step in the compilation process. My parser and evaluation maintain proper scoping rules inside of different functions and function calls of previously defined functions. No variables exist outside of their defined scope. Currently, the evaluation process can occur the following ways:

1. Directly to the terminal, as before with the hello.ju example: python drjb_parser.py hello.ju
2. To an output file with a .out extension: python drjb_parser.py hello.ju --out
3. To a template assembly file with a .asm extension: python drjb_parser.py hello.ju --asm (NOTE - will be implemented for other input .ju files in the future)
4. Through the webapp application (installation and use described soon).
