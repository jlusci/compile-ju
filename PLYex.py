# ------------------------------------------------------------
# PLYex.py
#
# new tokenizer that uses PLY for lexing instead of splitting 
# on whitespace - use from drjb_parser.py and ju_webapp_parser.py
# ------------------------------------------------------------
import ply.lex as lex
import sys

tokenlist = []

# List of reserved words
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'for' : 'FOR',
   'while': 'WHILE',
   'var' : 'VAR',
   'print': 'PRINT',
   'return': 'RETURN'
   }

# List of token names.   
tokens = [
   'EOLCOMMENT',
   'STRING',
   'FLOAT',
   'NUMBER',
   'ID',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'POWER',
   'MODULO',
   'ISEQ',
   'ASSIGN',
   'LESS',
   'GREATER',
   'LESSEQ',
   'GREATEQ',
   'NOTEQ',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
   'LBRACK',
   'RBRACK',
   'SEMICOLON',
   'COLON',
   'DOT',
   'COMMA'
] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_POWER   = r'\^'
t_MODULO  = r'%'

t_ISEQ    = r'=='
t_ASSIGN  = r'='
t_LESS      = r'<'
t_GREATER   = r'>'
t_LESSEQ    = r'<='
t_GREATEQ   = r'>='
t_NOTEQ     = r'!='

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_SEMICOLON = r';'
t_COLON   = r':'
t_DOT     = r'\.'
t_COMMA   = r','

def t_EOLCOMMENT(t):
    r'//[^\n]*'     # from https://www.udacity.com/wiki/cs262/unit-2#lexical-analyzer
    # r'//.*'
    pass
    # No return value. Token discarded

# A regular expression rule with some action code
def t_STRING(t):
    # r'["\'][a-zA-Z0-9]*["\']'     add more special characters to string tokens?
    # r'["\'][\s\w\,\.\(\)\?]*["\']'
    r'["\'].*?["\']'
    t.value = t.value.strip('"\'')
    return t

def t_FLOAT(t):
    r'-?\d+\.\d*(e-?\d+)?'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'-?\d+'
    t.value = int(t.value)    
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \r\t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
# lexer = lex.lex(optimize=1,lextab="test1")   #builds lexer and file 
# lexer = lex.lex(debug=1)                     #debug on
lexer = lex.lex()


# *********************************************
# moved lexical analysis to parser file
# *********************************************
# Give the lexer some input - from sys.argv[1]
# infile = open(sys.argv[1])
# filename = sys.argv[1]

# # From webapp
# infile = open("test.ju")
# filename = "test.ju"
 
# infile = infile.read()
# lexer.input(infile)

# while True:
#     tok = lexer.token()
#     if not tok: break      # No more input
#     tokenlist.append(tok)


# lex.py comes with a simple main function - use this to get tuples list
# if __name__ == '__main__':
#      lex.runmain()


