"""
 Author:
Created:
Purpose:
 Course:

  Notes:

History:

"""


# ------------------------------------------------ STEP 1: PRELIMINARIES  / ENVIRONMENT SETUP
# import the libraries we'll need
import ply.lex as lex               # lexical analysis / tokenization
import ply.yacc as yacc             # parser
from ASTNODE import ASTNODE         # simple class for creating nodes for an Abstract Syntax Tree (AST)
from Common import Common           # a useful class and method for getting the type of an object
from ReadFile import ReadFile       # a simple but a useful read file class


# ------------------------------------------------ STEP 2: SET UP LEXER

"""
    See Section 4 of https://www.dabeaz.com/ply/ply.html. Sections 4 through 4.4.

    To handle reserved words, you should write a single rule to match an identifier and do a special name lookup
    in a function like this:

    reserved = {
       'if' : 'IF',
       'then' : 'THEN',
       'else' : 'ELSE',
       'while' : 'WHILE',
       ...
    }
    
    Note:
            * t_ definitions with regular expressions do not need to be created for reserved words
            * reserved words represent concrete syntax in the source language of your compiler
"""
reserved = {}

"""
    Tokens are elements of your grammar that are not reserved words, for example an ID for an identifier,
    or DQ_STRING for a string wrapped with double quotes. A list of tokens is required.
    
    Example: tokens = ['ID', 'NUMBER', ... ]
"""
# noinspection SpellCheckingInspection
tokens = [
    'NUMBER'
]

tokens += list(reserved.values())

"""
    See Section 4.8 of https://www.dabeaz.com/ply/ply.html.
    
    Literals are single characters that you will use in your language's concrete syntax but do not need
    t_ definitions created for them.
    
    Example: literals = ['(', ')', "+", "-", "%", "*", "/", "=", ";"]
"""
literals = []


# helper function create a Python int or float as needed
def string_to_number(s):
    try:
        ans = (int(s), "integer")
    except ValueError:
        ans = (float(s), "float")

    return ans


# noinspection PyPep8Naming
# noinspection PySingleQuotedDocstring
def t_NUMBER(t):
    r'[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'  # 2024-02-14, DMW, we'll save floating point for later
    # https://www.regular-expressions.info/floatingpoint.html
    # r'\d+'  # original regular expression -- allow integers only

    t.value = string_to_number(t.value) # int(t.value)

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


# See sections 4.10 - EOF Handling- https://www.dabeaz.com/ply/ply.html
# Note: This method is not required and may not be necessary
# EOF handling rule
# def t_eof(t):
#     # Get more input (Example)
#     more = raw_input('... ')
#     if more:
#         self.lexer.input(more)
#         return self.lexer.token()
#     return None


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
