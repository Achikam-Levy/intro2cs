from itertools import combinations

def is_leaf(node):
    # No need to check for childs because there's either both or neither.
    return node.positive_child is None

def __build_str(node):
    if node is None:
        return [''], 0
    if is_leaf(node):
        s = 'None(str)' if node.data == 'None' else str(node.data)
        return [s], len(s)
    root = 'None(str)' if node.data == 'None' else str(node.data)
    leafL, widthL = __build_str(node.positive_child)
    leafR, widthR = __build_str(node.negative_child)
    split = max(widthR, widthL) + 1
    df = widthR // 2 + 1  # TODO: sort this out

    line0 = ' ' * (split - len(root) // 2) + root
    line1 = ' ' * (split - 2 - df) + '_' * df + 'Y/' + ' ' + '\\N' + '_' * df
    lines = [line0, line1]
    width = max(len(line1), len(line0))
    L_pos, R_pos = split - 2 - df, df
    for i in range(max(len(leafR), len(leafL))):
        line = ''
        if i < len(leafL):
            line += ' ' * (L_pos - len(leafL[i])) + leafL[i]
        if i < len(leafR):
            line += ' ' * (split - len(line) + 3) + leafR[i]
        width = max(len(line), width)
        lines.append(line)
    return lines, width


def tree_to_str(node):
    s_array, _ = __build_str(node)
    return '\n'.join(s_array)

from ex11 import Node
def __tree_builder(tokens):
    val = None if tokens[0] == 'None' else tokens[0]
    root = Node(val)
    if tokens[1] == '.':
        return root, 2
    for token in tokens:
       root.positive_child, read = __tree_builder(tokens[1:])
       root.negative_child, read2 = __tree_builder(tokens[read+1:])
    return root, read+read2+1

def tree_builder(str_repr):
    return __tree_builder( str_repr.split() )[0]