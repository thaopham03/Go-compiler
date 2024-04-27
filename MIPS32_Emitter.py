"""
Author: Thao Pham
Created: 2024-04-21
Purpose: Go programming language compiler using PLY, emit AST using MIPS32.
Course: CSC 486 - Compilers Design and Implementation

Notes:
  - BASE compiler: Prof. Deanna Wilborne
  - The Go Programming Language Specification: https://go.dev/ref/spec 

"""
# import the libraries we'll need
from ASTNODE import ASTNODE
import datetime as dt 

class MIPS32Emitter:
    def __init__(self, source_ast: ASTNODE = None, target_file: str = ""):
        self.source_ast = source_ast
        self.target_file = target_file
        self.output_asm = None
        self.exit_status = 0
        self.start_compile = None
        self.end_compile = None
        self.elapsed_compile = None 

    def set_source_ast(self, source_ast: ASTNODE = None):
        self.source_ast = source_ast
    
    def set_target_file(self, target_file: str = "") -> None:
        self.target_file = target_file
    
    def emit_preamble(self, program_name: str = "NONE") -> None:
        self.start_compile = dt.datetime.now()
        self.output_asm = "# PROGRAM: " + program_name + "\n# Compile Start: {}".format(self.start_compile) + "\n.text\n"
        # 2024-03-27, DMW, updated emitter final output to compute elapsed compilation time
    
    def emit_postamble(self) -> None:
        # 2024-04-15, DMW, TODO: here is where we output external functions we're going to include
        # self.emit_asm(".include ipow.asm")  # 2024-04-15, DMW,
        self.end_compile = dt.datetime.now()
        self.elapsed_compile = self.end_compile - self.start_compile
        self.output_asm += "li $a0, {}\n".format(self.exit_status) + "li $v0, 17\n" + "syscall\n\n"
        self.output_asm += "# Compile End Time: {}\n".format(self.end_compile)
        self.output_asm += "# Compile Elapsed Time: {}\n\n".format(self.elapsed_compile)

    def emit_asm(self, asm_text: str) -> None:
        self.output_asm += asm_text + "\n"

    def emit_ast(self) -> None:
        if self.source_ast is None:
            print("No Abstract Syntax Tree provided.")
            return
        
        # self.emit_preamble()  # 2024-03-27, DMW, moved to emitter
        self.emitter(self.source_ast)
        self.emit_postamble()

    def emitter(self, _node: ASTNODE) -> None:
        # print(_node)  # 2024-04-13, DMW, good old-fashioned and simple debugging
        if _node is None:
            return

        def process_children(_node):
            for child in _node.children:
                self.emitter(child)

        if _node.name == "program":  # 2024-03-27, DMW, handle start of program
            self.emit_preamble(_node.value['name'])  # 2024-04-13, DMW, TODO: handle program name in emitter
            # self.emit_asm("# {}".format(_node.value['name']))
            process_children(_node)

        elif _node.name in ["statement_list", "block_statement"]:
            process_children(_node)

        elif _node.name == "print":
            process_children(_node)
            self.emit_asm("li $a0, 17")
            self.emit_asm("li $v0, 1")
            self.emit_asm("syscall")
            self.emit_asm("li $a0, 0x0A")
            self.emit_asm("li $v0, 11")
            self.emit_asm("syscall")
            self.emit_asm("li $v0, 10")
            self.emit_asm("syscall")
            
        elif _node.name == "expression":
            self.emit_asm("# expression")
            if len(_node.children) == 0:  # 2024-04-13, DMW, no children means immediate value
                self.emit_asm("li $t0, {}".format(_node.value['value'][0]))
                self.emit_asm("addi $sp, $sp, -4")
                self.emit_asm("sw $t0, 4($sp)")
        
        elif _node.name == "name": 
            self.emit_asm("# name")
        else:
            pass  # 2024-04-13, DMW, TODO: This should cause a syntax error