# ------------------------------------------------------------
# PLYex.py
#
# new tokenizer that uses PLY for lexing instead of splitting 
# on whitespace - will use in combination with drj_parser.py
# ------------------------------------------------------------
import ply.lex as lex
import sys

tokenlist = []

# List of reserved words
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'for' : 'FOR',
   'var' : 'VAR'
   }

# List of token names.   
tokens = [
   'EOLCOMMENT',
   'STRING',
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
    # r'["\'][a-zA-Z0-9]*["\']'
    r'["\'][\s\w]*["\']'
    t.value = t.value.strip('"\'')
    return t

def t_NUMBER(t):
    r'\d+'
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
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
#lexer = lex.lex(optimize=1,lextab="test1") #builds lexer and file 
#"test1" containing all regular expressions, disables most error checking
lexer = lex.lex(debug=1)

# Test it out
data = '''
3 + 4 * 10 ("hello there") 
for (var x = 10) {
  'hello';
}
// here is a comment
  + -20 *2;
'''

# Give the lexer some input - from sys.argv[1]
infile = open(sys.argv[1])
infile = infile.read()
lexer.input(infile)

# use the following for testing
# lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    # print tok.type, tok.value, tok.lineno, tok.lexpos
    tokenlist.append(tok)
    # print tok, type(tok)
token = tokenlist[-1].value
print tokenlist, len(tokenlist), tokenlist[-1], "HERE IS THE LAST TOKEN:", token

# lex.py comes with a simple main function - use this to get tuples list
# if __name__ == '__main__':
#      lex.runmain()


