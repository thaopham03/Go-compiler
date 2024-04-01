#  Author:  Deanna M. Wilborne
# College:  Berea College
#  Course:  CSC386 Fall 2021
# Purpose:  AST Node Class
# History:
#           2024-03-12, DMW, modified to make print value more concise
#           2024-02-27, DMW, modified to print node value information if present for render_tree()
#           2024-02-12, DMW, modified for CSC486 Compiler Design & Implementation
#           2023-04-30, DMW, conditionally import curses if not on Windows
#           2023-04-24, DMW, added __str__ method() for pretty printing nodes; imports curses.ascii and Common
#           2023-04-16, DMW, extra fields added to nodes, line, and index, for additional diagnostics
#           2023-04-04, DMW, updated for 2023-Summer CSC420 Programming Languages
#           2021-10-28, DMW, corrected an issue with __init__ where valid values of 0 wouldn't be saved in the node
#           2021-10-21, DMW, created
#
#           Copyright (2023) Deanna M. Wilborne

from anytree import NodeMixin, RenderTree
from Common import Common
from sys import platform

if platform != "win32":
    import curses.ascii as ca


# noinspection SpellCheckingInspection
class ASTNODE(NodeMixin):
    version = "2024-02-27"

    def __init__(self, name: str, value=None, parent=None, children=None, line=None, index=None) -> None:
        self.name = name
        self.parent = parent
        self.value = value
        # 2023-04-16, DWM, line and index is based on:
        # https://my.eng.utah.edu/~cs3100/lectures/l14/ply-3.4/doc/ply.html#ply_nn33
        self.line = line
        self.index = index

        if children is not None:
            self.children = children

    # 2023-04-24, DMW, substitute control characters in value attibutes of type string
    def safe_value(self) -> str:
        output = ""
        for char in self.value:
            output += ca.unctrl(char)
        return output

    # 2023-04-24, DMW, provide ability to print node details
    def __str__(self) -> str:
        output_str = "{" + " name='{}'".format(self.name)
        if self.value is not None:
            if platform != "win32":
                if Common.object_type(self.value) == "str":
                    output_str += ", value='{}'".format(self.safe_value())
                else:
                    output_str += ", value='{}'".format(self.value)
            else:
                output_str += ", value='{}'".format(self.value)
        if self.parent is not None:
            output_str += ", parent='{}'".format(self.parent.name)
        if self.children is not None:
            if len(self.children) != 0:
                children = ""
                for child in self.children:
                    if children != "":
                        children += ", '{}'".format(child.name)
                    else:
                        children = "[ '{}'".format(child.name)
                children += " ]"
                output_str += ", children={}".format(children)
        if self.line is not None:
            output_str += ", line={}".format(self.line)
        if self.index is not None:
            output_str += ", index={}".format(self.index)
        output_str += " }"
        return output_str

    # 2024-02-12, DMW, added class static method
    @staticmethod
    def render_tree(tree) -> None:
        for pre, fill, node in RenderTree(tree):
            # print("node value={}".format(node.value))
            if node.value is None:
                node_info = node.name
            else:
                node_info = node.name + "(" + str(node.value) + ")"
            print("%s%s" % (pre, node_info))


# limited functional testing
# 2023-04-24, DMW, updated to use test() to prevent pycharm warnings about shadowing "child"
if __name__ == "__main__":
    def test():
        child2 = ASTNODE("child2", value="2")
        child3 = ASTNODE("child3", value="3")
        child = ASTNODE("child", children=[child2, child3])
        root = ASTNODE("root", value="\ntest\n", children=[child])
        ASTNODE.render_tree(root)

    test()

