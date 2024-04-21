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

import sys
import math 
from anytree import Node, RenderTree

sys.path.insert(0, "../..")

# ------------------------------------------------ STEP 2: SET UP LEXER

reserved = {
    "if" : "IF",
    "else" : "ELSE",
    "for" : "FOR",
    "Println" : "PRINTLN", # reserved word to print to standard output with a newline
    "Printf" : "PRINTF", # reserved word to print to standard output with format
    "Print" : "PRINT", # reserved word to print to standard output
    "fmt.Println" : "FMT_PRINTLN", # reserved word to print to standard output with format and a newline
    "fmt.Printf" : "FMT_PRINTF", # reserved word to print to standard output with format
    "fmt.Print" : "FMT_PRINT", # reserved word to print to standard output with format
    'true': 'TRUE',  
    'false': 'FALSE',  
    'sin': 'SIN',    
    'cos': 'COS',   
    'tan': 'TAN',    
    'abs': 'ABS', 
    'min': 'MIN',
    'max': 'MAX'  
    }

tokens = [
    'SQ_STRING', # single quoted string
    'DQ_STRING', # double quoted string
    'NUMBER', # number literals
    'NAME', # identifiers
    'PLUS', # binary operator expression PLUS
    'MINUS', # binary operator expression MINUS
    'TIMES', # binary operator expression TIMES
    'DIVIDE', # binary operator expression DIVIDE
    'MOD', # # binary operator expression MOD
    'LT', 'LE', 'EQ', 'NEQ', 'GE', 'GT', 'UMINUS' # PEMAS operators
]

tokens += list(reserved.values())

literals = ["(", ")", "+", "-", "*", "/", "%", "=",
            ";", "{", "}", "<", ">", ","] 

# helper function create a Python int or float as needed
def string_to_number(s):
    try:
        ans = (int(s), "integer")
    except ValueError:
        ans = (float(s), "float")

    return ans

# DEFINE TOKENS PATTERNS

def t_PRINTLN(t):
    r'Println'
    return t

def t_PRINTF(t):
    r'Printf'
    return t 

def t_PRINT(t):
    r'Print'
    return t

def t_FMT_PRINTLN(t):
    r'fmt\.Println'
    return t

def t_FMT_PRINTF(t):
    r'fmt\.Printf'
    return t

def t_FMT_PRINT(t):
    r'fmt\.Print'
    return t

def t_FOR(t):
    r'for'
    return t

# floating points literals:

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# string literals:

# single quoted string:
def t_SQ_STRING(t):
   r"'[^'\\]*(?:\\.[^'\\]*)*'"
   return t

# double quoted string:
def t_DQ_STRING(t):
   # noinspection PySingleQuotedDocstring
   r'"[^"\\]*(?:\\.[^"\\]*)*"'
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

def t_VAR(t):
    r'var'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t 

def t_TRUE(t):  
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_SIN(t):
    r'sin'
    return t

def t_COS(t):
    r'cos'
    return t

def t_TAN(t):
    r'tan'
    return t

def t_ABS(t):
    r'abs'
    return t

def t_MIN(t):
    r'min'
    return t

def t_MAX(t):
    r'max'
    return t

# noinspection PyPep8Naming
# noinspection PySingleQuotedDocstring
def t_NUMBER(t):
    r'[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'  # 2024-02-14, DMW, we'll save floating point for later
    # https://www.regular-expressions.info/floatingpoint.html
    # r'\d+'  # original regular expression -- allow integers only

    t.value = string_to_number(t.value) # int(t.value)

    return t

# name identifiers:
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t

# See section 4.5 - https://www.dabeaz.com/ply/ply.html - Lexer rules for ignoring text for tokenization
# noinspection PyPep8Naming
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded


# See sections 4.6, 4.7 - https://www.dabeaz.com/ply/ply.html
# characters to ignore as whitespace, space, tab, vertical tab, form feed
t_ignore = " \t\v\f"


# noinspection PySingleQuotedDocstring
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input_text, token):
    line_start = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# See sections 4.9 - Error Handling - https://www.dabeaz.com/ply/ply.html
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# See sections 4.11 - Building and using the lexer - https://www.dabeaz.com/ply/ply.html
# Build the lexer
lexer = lex.lex(debug=0)

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
    "program : statement_list"
    global program
    program = ASTNODE("program", children=[p[1]])

def p_STATEMENTS(p):
    """
    statement_list : statement_list statement 
                | statement
    """
    if len(p) == 3:
        # p[0] = p[1] + [p[2]]
        p[0] = ASTNODE("statement_list", children=[p[1], p[2]])
    else:
        # p[0] = [p[1]]
        p[0] = ASTNODE("statement_list", children=[p[1]])
    # print("*****************************************************************\n",p[0],"**********************************************")
    # ASTNODE.render_tree(p[0])

def p_BLOCK_STATEMENT(p):
    """
    block_statement : '{' statement_list '}'
    """
    p[0] = ASTNODE("block_statement", children=[p[2]])

def p_STATEMENT(p):
    """statement : all_prints
                | assign
                | if_statement
                | for
                | expression"""
    p[0] = ASTNODE("statement", children=[p[1]])

def p_all_prints(p):
    """
    all_prints : print
                | println
                | printf
                | fmt_print
                | fmt_println
                | fmt_printf
    """
    p[0] = p[1]

def p_if_statement(p):
    """
    if_statement : IF assign block_statement ELSE block_statement
    """
    p[0] = ASTNODE("if_statement", children=[p[2], p[3], p[5]])

def p_for(p):
    """
    for : FOR assign block_statement
    """
    p[0] = ASTNODE("for", children=[p[2], p[3]])

def p_EXPRESSION(p):
    """
    expression : number
                | name  
                | assign 
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
                | expression ',' expression
    """
    if len(p) == 4:
        p[0] = ASTNODE("expression", children=[p[1], p[3]])
    else:
        p[0] = ASTNODE("expression", children=[p[1]])

def p_GROUP(p):
    """ 
    expression : '(' expression ')'
    """
    p[0] = p[2]

def p_expression_UMINUS(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = -p[2]

def p_number(p):
    "number : NUMBER"
    p[0] = ASTNODE("number", value=p[1])

def p_NAME(p):
    "name : NAME"
    p[0] = ASTNODE('name', value=p[1])

def p_ASSIGN(p):
    """ 
    assign : name '=' expression
            | name GT expression
            | name LT expression
    """
    p[0] = ASTNODE("assign", value=p[2], children=[p[1], p[3]])

def p_STRING(p):
    """expression : string"""
    p[0] = p[1]

def p_EXPRESSION_STRINGS(p):
   """string : SQ_STRING
             | DQ_STRING
   """
   p[0] = ASTNODE("expression", value=p[1])

# PRINT STATEMENTS:

def p_PRINT(p):
    "print : PRINT '(' expression ')'"
    p[0] = ASTNODE("print", children=[p[3]])

def p_PRINTLN(p):
    "println : PRINTLN '(' expression ')'"
    p[0] = ASTNODE("print", children=[p[3]])

def p_PRINTF(p):
    "printf : PRINTF '(' expression ')'"
    p[0] = ASTNODE("print", children=[p[3]])

def p_FMT_PRINT(p):
    "fmt_print : FMT_PRINT '(' expression ')'"
    p[0] = ASTNODE("print", children=[p[3]])

def p_FMT_PRINTLN(p):
    "fmt_println : FMT_PRINTLN '(' expression ')'"
    p[0] = ASTNODE("print", children=[p[3]])

def p_FMT_PRINTF(p):
    "fmt_printf : FMT_PRINTF '(' expression ')'"
    p[0] = ASTNODE("print", children=p[3])

# Intrinsic functions

def p_ABS(p):
    "expression : ABS '(' expression ')'"
    p[0] = math.abs(p[3])

def p_SIN(p):
    "expression : SIN '(' expression ')'"
    p[0] = math.sin(p[3])

def p_COS(p):
    "expression : COS '(' expression ')'"
    p[0] = math.cos(p[3])

def p_TAN(p):
    "expression : TAN '(' expression ')'"
    p[0] = math.tan(p[3])

def p_MIN(p):
    "expression : MIN '(' expression ',' expression ')'"
    p[0] = math.min(p[3], p[5])

def p_MAX(p):
    "expression : MAX '(' expression ',' expression ')'"
    p[0] = math.max(p[3], p[5])

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
    elif _node.name == "string":
        ast_stack.push(_node.value)
    else:
        raise "Unknown node name {}".format(_node.name)
   

if __name__ == "__main__":
    
    # Write to console an integer:
    # prg1 = "17"
    # yacc.parse(prg1)

    # Write to console a string:
    # prg2 = "Println(\"Hello, World!\")"
    # yacc.parse(prg2)

    # if-else support:
    # prg3 = "if x > 5 { fmt.Println(\"Greater than 5\") } else { fmt.Println(\"Not greater than 5\") }"
    # yacc.parse(prg3, debug=1)

    # While/for loops:
    # loop = "for i < 10 { fmt.Println(\"Number: \", i) i = i + 1 }"
    # yacc.parse(loop, debug=0)

    # Intrinsic functions:
    abs_val = "abs(5)"
    yacc.parse(abs_val)
   
    if program is None:
        print("No AST")
   
    ASTNODE.render_tree(program)
    quit(0)
