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

"""

# ------------------------------------------------ STEP 1: PRELIMINARIES  / ENVIRONMENT SETUP
# import the libraries we'll need
import ply.lex as lex               # lexical analysis / tokenization
import ply.yacc as yacc             # parser
from ASTNODE import ASTNODE         # simple class for creating nodes for an Abstract Syntax Tree (AST)
from Common import Common           # a useful class and method for getting the type of an object
from ReadFile import ReadFile       # a simple but a useful read file class
