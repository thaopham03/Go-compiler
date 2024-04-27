"""
Author: Thao Pham
Created: 2024-04-22
Purpose: Symbol Table class for Go programming language compiler using PLY.
Course: CSC 486 - Compilers Design and Implementation

Notes:
  - BASE compiler: Prof. Deanna Wilborne
  - The Go Programming Language Specification: https://go.dev/ref/spec 

"""

class Symbol:
    def __init__(self, name, type, scope_level, attributes=None):
        # name: the identifier's name, variable name, function name, etc.
        # type: the type of the symbol, e.g., int, float, string, etc.
        # scope_level: an integer indicating the depth of the scope in which the symbol is declared
        # attributes: a dictionary of additional attributes for the symbol, such as its values, parameters, etc.
        self.name = name
        self.type = type
        self.scope_level = scope_level
        self.attributes = attributes if attributes is not None else {}

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_level = 0

    def add(self, name, symbol_type, attributes=None):
        symbol = Symbol(name, symbol_type, self.scope_level, attributes)
        self.symbols[name] = symbol
    
    def lookup(self, name):
        return self.symbols.get(name, None)
    
    def enter_scope(self):
        self.scope_level += 1

    def exit_scope(self):
        to_delete = [name for name, sym in self.symbols.items() if sym.scope_level == self.scope_level]
        for name in to_delete:
            del self.symbols[name]
        self.scope_level -= 1