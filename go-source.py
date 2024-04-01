"""
Author: Thao Pham
Created: 2024-03-25
Purpose: Go programming language compiler using PLY.
Course: CSC 486 - Compilers Design and Implementation

Notes:
  - BASE compiler: Prof. Deanna Wilborne
  - The Go Programming Language Specification: https://go.dev/ref/spec 

History:
  - 2024-3-25: Thao Pham created this file.
  - 2024-04-01: Thao Pham edited this file. Working on the core functionality of the compiler. 

"""

# ------------------------------------------------ STEP 1: PRELIMINARIES  / ENVIRONMENT SETUP
# import the libraries we'll need
import ply.lex as lex               # lexical analysis / tokenization
import ply.yacc as yacc             # parser
from ASTNODE import ASTNODE         # simple class for creating nodes for an Abstract Syntax Tree (AST)
from Common import Common           # a useful class and method for getting the type of an object
from ReadFile import ReadFile       # a simple but a useful read file class

# ------------------------------------------------ STEP 2: SET UP LEXER

reserved = {
    "package" : "PACKAGE", # reserved word to define the package name
    "import" : "IMPORT",   # reserved word to import packages
    "if" : "IF",
    "else" : "ELSE",
    "for" : "FOR",
    "goto" : "GOTO", # reserved word to jump to a label
    "Print" : "PRINT", # reserved word to print to standard output
    "Println" : "PRINTLN", # reserved word to print to standard output with a newline
    "Printf" : "PRINTF", # reserved word to print to standard output with format
    "int" : "INT", # reserved word to declare an integer type
    "string" : "STRING", # reserved word to declare a string type
    "float" : "FLOAT", # reserved word to declare a floating-point type
}

tokens = [
    'INTEGER',
    'FLOAT',
    'STRING', # Interpreted string literals are character sequences between double quotes, as in "bar". Within the quotes, any character may appear except newline and unescaped double quote. 
    'RUNE', 
    'HEX',
    'RAWSTRING', # character sequences between back quotes, such as 'foo'.
    'OCTAL'
]

tokens += list(reserved.values())

literals = ["(", ")", "+", "-", "*", "/", "%", "=",
            ";", "{", "}", "<", ">"] # I am not sure if I need all of these literals, might edit later. 

# DEFINE TOKENS PATTERNS

# integer literals:

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# string literals:

def t_STRING(t):
    r'"(\\.|[^\\"])*"'
    t.value = t.value[1:-1] # remove the double quotes
    return t

# raw string literals:

def t_RAWSTRING(t):
    r'`[^`]*`'
    t.value = t.value[1:-1] # remove the back quotes
    return t


# See sections 4.11 - Building and using the lexer - https://www.dabeaz.com/ply/ply.html
# Build the lexer
lexer = lex.lex()

# ------------------------------------------------ STEP 3: SET UP THE PARSER

# Note: example precedence shown, setting precedence helps with binary operators
# noinspection SpellCheckingInspection
# precedence = (
#     ('left', 'LT', 'LE', 'EQ', 'NEQ', 'GE', 'GT'),
#     ('left', '+', '-'),
#     ('left', '*', '/', '%'),
#     ('right', 'UMINUS'),
# )

program = None

start = "program"  # set the start production, even though the first production is the start by default


# noinspection PyPep8Naming
# noinspection PySingleQuotedDocstring
def p_PROGRAM(p):
    "program : number"
    global program
    program = ASTNODE("program", children=[p[1]])


# noinspection PyPep8Naming
def p_NUMBER(p):
    "number : NUMBER"
    p[0] = ASTNODE("number", value=p[1])
    # print(p[1])  # debugging


# a p_error(p) rule is required
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

# ------------------------------------------------ STEP 4: USE THE PARSER

if __name__ == "__main__":
    source_program = "17"
    ast = parser.parse(source_program)

    print(program)
    ASTNODE.render_tree(program)
