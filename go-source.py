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
  - 2024-04-03: Thao Pham edited this file. Keep working on the core functionality of the compiler.

"""

# ------------------------------------------------ STEP 1: PRELIMINARIES  / ENVIRONMENT SETUP
# import the libraries we'll need
import ply.lex as lex               # lexical analysis / tokenization
import ply.yacc as yacc             # parser
from ASTNODE import ASTNODE         # simple class for creating nodes for an Abstract Syntax Tree (AST)
from Common import Common           # a useful class and method for getting the type of an object
from ReadFile import ReadFile       # a simple but a useful read file class
from Stack import Stack             # a simple stack class

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
    'FLOAT',
    'STRING', # Interpreted string literals are character sequences between double quotes, as in "bar". Within the quotes, any character may appear except newline and unescaped double quote. 
    'RUNE', 
    'HEX',
    'RAWSTRING', # character sequences between back quotes, such as 'foo'.
    'OCTAL',
    'PLUS', # binary operator expression PLUS
    'MINUS', # binary operator expression MINUS
    'TIMES', # binary operator expression TIMES
    'DIVIDE', # binary operator expression DIVIDE
    'MOD', # # binary operator expression MOD
    'NUMBER',
    'LT', 'LE', 'EQ', 'NEQ', 'GE', 'GT', 'UMINUS'
]

tokens += list(reserved.values())

literals = ["(", ")", "+", "-", "*", "/", "%", "=",
            ";", "{", "}", "<", ">"] 

# helper function create a Python int or float as needed
def string_to_number(s):
    try:
        ans = (int(s), "integer")
    except ValueError:
        ans = (float(s), "float")

    return ans

# DEFINE TOKENS PATTERNS

# integer literals:

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# floating points literals:

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
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

def t_HEX(t):
    r'0[xX][0-9a-fA-F]+'
    t.value = int(t.value, 16)  # Convert to integer from hex
    return t

def t_OCTAL(t):
    r'0[oO][0-7]+'
    t.value = int(t.value, 8)  # Convert to integer from octal
    return t

def t_RUNE(t):
    r'\'(\\[abfnrtv\\\'"]|\\[0-7]{1,3}|\\x[0-9a-fA-F]{1,2}|\\u[0-9a-fA-F]{4}|\\U[0-9a-fA-F]{8}|[^\\\'\n])\''
    t.value = t.value[1:-1]  # Strip the single quotes
    return t

def t_PLUS(t):
    r'\+'
    return t

def t_MINUS(t):
    r'\-'
    return t

def t_TIMES(t):
    r'\*'
    return t

def t_DIVIDE(t):
    r'/'
    return t

def t_MOD(t):
    r'%'
    return t

def t_LT(t):
    r'<'
    return t

def t_LE(t):
    r'<='
    return t

def t_EQ(t):
    r'=='
    return t

def t_NEQ(t):
    r'!='
    return t

def t_GE(t):
    r'>='
    return t

def t_GT(t):
    r'>'
    return t

def t_UMINUS(t):
    r'-'
    return t

# characters to ignore as whitespace
t_ignore = " \t\v\f"

# noinspection PySingleQuotedDocstring
def t_newline(t):
   r'\n+'
   t.lexer.lineno += t.value.count("\n")

def t_error(t):
   print("Illegal character '%s'" % t.value[0])
   t.lexer.skip(1)

# See sections 4.11 - Building and using the lexer - https://www.dabeaz.com/ply/ply.html
# Build the lexer
lexer = lex.lex()

# ------------------------------------------------ STEP 3: SET UP THE PARSER

# Note: example precedence shown, setting precedence helps with binary operators
# noinspection SpellCheckingInspection

precedence = (
    ('left', 'LT', 'LE', 'EQ', 'NEQ', 'GE', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'),
)

program = None

start = "program"  # set the start production, even though the first production is the start by default


# noinspection PyPep8Naming
# noinspection PySingleQuotedDocstring
def p_PROGRAM(p):
    "program : statements"
    global program
    program = ASTNODE("program", children=[p[1]])

def p_STATEMENTS(p):
    """
    statements : statements statement 
                | statement
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_STATEMENT(p):
    """statement : expression"""
    p[0] = ASTNODE("statement", children=[p[1]])

def p_EXPRESSION(p):
    """
    expression : number
                | expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
                | expression MOD expression
                | expression LT expression
                | expression LE expression
                | expression EQ expression
                | expression NEQ expression
                | expression GE expression
                | expression GT expression
    """
    if len(p) == 4:
        p[0] = ASTNODE("expression", children=[p[1], p[3]])
    else:
        p[0] = ASTNODE("expression", children=[p[1]])

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

ast_stack = Stack()


def interpret_ast(_node: ASTNODE) -> None:
   global ast_stack
   if _node.name == "program":
       for child in _node.children:
           interpret_ast(child)
   elif _node.name == "statement":
       for child in _node.children:
           interpret_ast(child)
   elif _node.name == "print":
       for child in _node.children:
           interpret_ast(child)
       print(ast_stack.pop())
   elif _node.name == "expression":
       for child in _node.children:
           interpret_ast(child)
   elif _node.name == "number":
       ast_stack.push(_node.value)
   else:
       raise "Unknown node name {}".format(_node.name)
   

if __name__ == "__main__":
    source_program = "17"
    ast = parser.parse(source_program)

    print(program)
    ASTNODE.render_tree(program)
