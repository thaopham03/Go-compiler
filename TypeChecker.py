#  Author:  Deanna M. Wilborne
# College:  Berea College
#  Course:  CSC386 Fall 2021
# Purpose:  AST Node Class
# History:
#           2024-04-15, DMW, created
#
#           Copyright (2024) Deanna M. Wilborne


from ASTNODE import ASTNODE

class TypeChecker:

    def __init__(self, ast: ASTNODE = None) -> None:
        self.no_type_nodes = [
            'program', 'stmt_list', 'block_stmts', 'print'
        ]

        self.number_types = {
            'double': 0,
            'single': 1,
            'float': 2,
            'integer': 3
        }

        # this list should be in the same order as they keys : values in the number_types dictionary
        self.number_type_names = [
            'double',
            'single',
            'float',
            'string'
        ]

        if ast is not None:
            self.ast = ast
            self.type_check(self.ast)

        def type_check(self, _node: ASTNODE):
            # recursively type check a node's children
            def process_children(_node: ASTNODE) -> None:
                for _child in _node.children:
                    self.type_check(_child)

            # if a node doesn't need type information, skip to its children
            if _node.name in self.no_type_nodes:
                # print("skipping: {}".format(_node.name))
                process_children(_node)
                return
            
            # at this point, we have a node where we should have type information;
            # binop is a good example that has expressions as children nodes, and we should
            # pull the type up from the expression nodes

            if _node.name == "prt_expr":
                process_children(_node)
                _node.value['type'] = _node.children[0].value['type']
            elif _node.name == "binop":
                if 'type' not in _node.value:
                    left_node = _node.children[0]
                    right_node = _node.children[1]
                    left_type = left_node.value['type']
                    right_type = right_node.value['type']

                if left_type == right_type:
                    _node.value['type'] = left_type
                else:
                    # possible type mismatch, are both types numeric in nature?
                    if left_type in self.number_types.keys() and right_type in self.number_types.keys():
                        cast_to_type = min(self.number_types[left_type], self.number_types[right_type])
                        _node.value['type'] = self.number_type_names[cast_to_type]
                        # 2024-04-16, DMW, TODO: upconvert numeric cast warning
                        return


                # TODO: if typecasting isn't used at this point there is a TYPE MISMATCH ERROR
                # print(left_type, " ", right_type)
            else:
                print("Add type checking for node: {}".format(_node.name))

    # 2024-04-15, DMW, TODO: implement unit testing
    # simple testing of the TypeChecker class
    if __name__ == "__main__":
    # 2024-04-15, DMW, test 0001
        num_left = ASTNODE(name="expr", value={'value': 5, 'type': 'integer'})
        num_right = ASTNODE(name="expr", value={'value': 14, 'type': 'integer'})
        binop = ASTNODE(name="binop", value={'op': '+'}, children=[num_left, num_right])

    ASTNODE.render_tree(binop)

    check = TypeChecker(binop)

    ASTNODE.render_tree(binop)
