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
    def emit_ast(self, _node):
        if _node.name in ["program", "block_statement", "statements"]:
            for child in _node.children:
                self.emit_ast(child)
        elif _node.name == "statement_list":
            for child in _node.children:
                self.emit_ast(child)
        elif _node.name == "statement":
            for child in _node.children:
                self.emit_ast(child)
        elif _node.name == "print":
            for child in _node.children:
                self.emit_ast(child)
            # print(ast_stack.pop())
            print("lw $a0, 4($sp)")  # 2024-02-14, DMW, my emitter was missing this line of assembly!
            print("addi $sp, $sp, 4")
            print("li $v0, 1")
            print("syscall")
            print("li $a0, 10")
            print("li $v0, 11")
            print("syscall")
        elif _node.name == "assign":
            self.emit_ast(_node.children[1])  # evaluate the expression and place result on stack
            var_address = f"{_node.children[0].value}_000000"  # assuming variable naming follows a convention
            print("lw $t0, 4($sp)")  # load the result of the expression
            print("sw $t0, " + var_address)  # store it in the variable's address
            print("addi $sp, $sp, 4")  # adjust stack pointer
        elif _node.name == "expression":
            if len(_node.children) == 1:
                self.emit_ast(_node.children[0])
            else:
                for child in _node.children:
                    self.emit_ast(child)
                    if len(_node.children) == 3:
                        print("lw $t0, 8($sp)")  # get the previously saved LHS value off the stack
                        print("lw $t1, 4($sp)")  # get the previously saved RHS value off the stack
                        if _node.value == "+":
                            print("add $t0, $t0, $t1")  # add the values: $t0 = $t0 + $t1
                        elif _node.value == "-":
                            self.emit_ast("sub $t0, $t0, $t1")
                        elif _node.value == "*":
                            self.emit_asm("mul $t0, $t0, $t1")
                    #fix this for other binop
                    print("addi $sp, $sp, 4")  # deallocate space where $t1 was saved on the stack
                    print("sw $t0, 4($sp)")
                else:
                    print("li, $t0, {}".format(_node.value[0]))
                    # allocate then push - for current output
                    print("addi $sp, $sp, -4")  # Decrease stack pointer to allocate 4 bytes
                    print("sw $t0, 0($sp)")  # Store the value at the new top of the stack
        elif _node.name == "number":
            print(f"li $t0, {_node.value[0]}")  # load immediate number
            print("addi $sp, $sp, -4")  # adjust stack
            print("sw $t0, 4($sp)")  # push onto stack
        elif _node.name == "for":
            pass
        elif _node.name == "name":
            pass
        else:
            raise Exception("Unknown node name {}".format(_node.name))
