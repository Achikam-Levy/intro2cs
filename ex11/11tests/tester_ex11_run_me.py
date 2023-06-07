import copy
import filecmp
import os
import pickle
import random
import re as regex
import sys
import time
import traceback
import warnings
import zipfile

from colorama import init as colorInit, Fore as CF, Style
from tqdm import tqdm

from ex11 import Node, Diagnoser, Record, build_tree, optimal_tree, parse_data
from tester_helper_dont_touch import *

#######################################
# TODO: fill out all parameters
# TODO: enter files to tests (without '.py' suffix)
filenames = ['ex11']
zip_filename = 'ex11'
ENABLE_ZIP = False
ENABLE_IMPORTS = True
DEF_COUNT_LIMIT = 9
MAX_METHOD_LENGTH = 14
CONST_COUNT_LIMIT = 0

QUICK_DEF_ANALYZE = True
DYNAMIC_IMPORT = False


def analyze_raw_file(lines, filename):
    linestr = '\n'.join(lines)
    # count things:
    const_count = len(set(regex.findall('[A-Z0-9_]+\\s+', linestr)))
    imports = []
    functions = []
    func_lengths = []
    found_main = False
    def_len_counter = 0
    commented: bool = False
    loop = len(lines)
    warning_lst = []
    time.sleep(0.1)
    for i in tqdm(range(loop)):
        line = lines[i].strip()
        if line.count('"""') % 2 == 1 or line.count("'''") % 2 == 1:
            commented = not commented
            continue
        if commented:
            continue
        match = regex.match(IMPORT_REGEX, line)
        if match is not None:
            imports.append(match.groups())
            continue
        match = regex.match(MAIN_REGEX, line)
        if match is not None:
            if found_main:
                warnings.warn(CF.RED + "ERROR - You have to main blocks in your code!")
            found_main = True
            func_lengths.append(def_len_counter)
            def_len_counter = 0
            continue
        if QUICK_DEF_ANALYZE:
            match = regex.match(QUICK_DEF_ANALYZE, line)
        else:
            match = regex.match(DEF_REGEX, line)
        if match is None:  # count line in counter
            should_count = len(line) > 0 and not line.startswith('#')
            def_len_counter += 1 if should_count else 0
            continue
        # if it is a method line:
        def_name = match.group(1)
        def_args = [arg.strip() for arg in match.group(2).split(',')]
        if len(functions) > 0:
            func_lengths.append(def_len_counter)
        functions.append((def_name, def_args))
        def_len_counter = 0
        if not regex.match(DEF_REGEX_pep8, line):
            warning_lst.append(
                CF.YELLOW + "pep8 Warning: method name is probably not pep8 in line " + str(i) + ' : ' + line)
    time.sleep(0.2)
    func_lengths.append(def_len_counter)
    for warning in warning_lst:
        warnings.warn(warning + CF.RED)
    return const_count, functions, func_lengths, imports, found_main


NAME_REGEX = "[a-zA-Z0-9_]+"
ARGS_REGEX = f"{NAME_REGEX}(?:\\s*:\\s*{NAME_REGEX})?(?:\\s*=\\s*{NAME_REGEX})?"
DEF_REGEX = f"def\\s+({NAME_REGEX})\\s*\\(((?:{ARGS_REGEX}\\s*,?\\s*)*)\\s*\\)"
QUICK_DEF_ANALYZE = f"def\\s+({NAME_REGEX})\\s*\\(((?:))"
DEF_REGEX_pep8 = 'def\\s+[a-z0-9_]+\\s*\\('
IMPORT_REGEX = f"(?:from\\s+({NAME_REGEX})\\s+)?import\\s+({NAME_REGEX})\\s*"
MAIN_REGEX = f"if\\s+__name__\\s*==\\s*[\"']__main__[\"']\\s*:"

code_lines_maya = -1
# TODO: edit raw code tests
def test_raw_code(code, *filenames):
    global code_lines_maya
    code_lines_maya = len(code[0])
    def_count, const_count = 0, 0
    for file_index in range(len(filenames)):
        lines = code[file_index]
        consts, funcs, func_lens, imports, hasMain = analyze_raw_file(lines, filenames[file_index])
        def_count += len(funcs)
        const_count += consts
        # if hasMain:
        #     print(CF.RED + "You used __name__ == '__main__' to run some code, but you should only have functions!")
        #     return False
        if 'tester_helper_dont_touch' in imports or 'tester_ex11_run_me' in imports:
            print(CF.RED+"You may not import files of this tester (-it will not run on the university's computers...")
            return False
        for i, func in enumerate(funcs):
            if func_lens[i] > MAX_METHOD_LENGTH:
                print(
                    CF.YELLOW + f"Warning: the method '{func[0]}' seems a bit long. Please make sure it is readable and consider reformatting it.")
    if def_count < DEF_COUNT_LIMIT:
        print(
            CF.YELLOW + "Warning: it seems your code doesn't use enough methods / doesn't use them correctly. please consult with yair/raz - we'll be happy to help :D")
    if const_count < CONST_COUNT_LIMIT:
        print(
            CF.YELLOW + "Warning: it seems your code doesn't use enough constants / doesn't use them correctly. please consult with yair/raz - we'll be happy to help :)")
    return True


# TODO: match actual program to content
def test_main():
    print(CF.LIGHTBLUE_EX+'Before we start running the rest of the tests, we would like to give you a debugging tip:')
    print(CF.LIGHTBLUE_EX+'If you need to create a binary tree to test a method you can you the function "tree_builder" from the file "tester_helper_dont_touch".')
    print(CF.LIGHTBLUE_EX+"The function takes a str and turns it into a tree. each word is a node and a . represents that the node is a leaf")
    print(CF.LIGHTBLUE_EX+"After writing a non-leaf node you write the positive_child tree and then the negative_child tree.")
    print(CF.LIGHTBLUE_EX+"*You can also you the function 'tree_to_str' from the same file to print a tree nicely")
    print(CF.LIGHTBLUE_EX+"For example, the following code:")
    print(CF.LIGHTBLUE_EX+"\ttree = tree_builder('a b . c . hey . bi .')\n"
                          "\tprint(tree_to_str(tree))")
    print(CF.LIGHTBLUE_EX+"Will output:\n"
                          f"{tree_to_str(tree_builder('a b . c . hey . bi .'))}")
    print(CF.LIGHTBLUE_EX+"Another Example:\n"
                          "\ttree= tree_builder('a b None . hello . c d e . e . a None . hello .')\n"
                          "\tprint(tree_to_str(tree))\n" \
                          "Will output:\n" \
                          f"{tree_to_str(tree_builder('a b None . hello . c d e . e . a None . hello .'))}")
    print()
    time.sleep(0.6)
    print(CF.MAGENTA+"We will now run the tests..."+CF.WHITE)
    time.sleep(1)
    tests = [init_test, test_diagnose, test_success_rate, test_all_illnesses, test_paths_to_illness,
             test_build_tree, test_optimal_tree, test_optimal_tree_exeptions, test_minimize_1,
             test_minimize_2]  # TODO enter test method list
    passed = 0
    for i, test in enumerate(tests):
        bul = test()
        passed += 1 if bul else 0
        if bul: print(CF.LIGHTMAGENTA_EX + f'You passed the {ordinal(i)} test!'+ f' (tests "{test.__name__[5:]}") ' if i > 0 else '')
    if passed < len(tests):
        print(CF.BLUE +
              f"\n\nYou passed {passed} tests out of {len(tests)}. A little work and you'll do much better!")
        return False
    print(CF.GREEN + (f"We'd like to tell you congradulations for passing all {passed} tests,"
                      f"\nbut you first have to read through the weekly instructions:"))
    print(CF.WHITE + '...')
    print(CF.LIGHTCYAN_EX + 'now what?\t' + CF.WHITE)
    str = f"""
0.   Use Ctrl+F to search for the 'print' function in your code, make sure your program won't print anything unwanted!
{CF.CYAN}1.   Make sure your code is as readable as possible!
        Moreover, make sure it's in pep8 and that it answers all python programming conventions
        (such as function_names and CONSTANT_NAMES)
{CF.WHITE}2.   make sure you're code checks variable types and make sure it DOESN'T IMPORT ANYTHING! (but the 'typing' module and itertools' combinations method)
{CF.CYAN}3.   Upload your code to the moodle page and check to see if their tester found any errors.

{CF.BLUE}You've read through all our note!
{CF.LIGHTMAGENTA_EX}{Style.BRIGHT}Thank You! Congradulations! And Good Luck! 
"""
    print(str)
    time.sleep(15)
    print(f"{CF.RED}P.S. Message from Maya Yassur: You're code is {code_lines_maya} lines long.")


# TODO: enter tests:
######################################
def init_test():
    """Should test separately because here you pass if an expection isn't thrown instead of according to return value"""
    try:
        try:
            nodeA = Node('meow', None, None)
            nodeB = Node('meow')
            node = Node('data', nodeA, nodeB)
            another_node = Node(data='data', positive_child=nodeA, negative_child=nodeB)
        except:
            print(CF.LIGHTRED_EX + 'Error - while constructing a Node object. The error details are printed below:')
            raise
        try:
            assert node.data == "data", 'Node root field not set up correctly'
            assert node.positive_child == nodeA, 'Node positive_child field not set up correctly'
            assert node.negative_child == nodeB, 'Node must negative_child field not set up correctly'
            assert nodeB.negative_child is None and nodeB.positive_child is None, 'The default values of the child nodes must be None!'
        except:
            print(
                CF.LIGHTRED_EX + "ERROR - There's a problem with the variables of Node class. try to run the line yourself if you're struggling to fix the issue.\n more data about the problem below:")
            raise
        try:
            diag = Diagnoser(node)
            assert diag.root == node
        except:
            print(
                CF.LIGHTRED_EX + 'Error - while constructing a Diagnoser object. The error details are printed below:')
            raise
        try:
            name, symptoms = 'meow', ['a', 'b', 'c']
            rec = Record(name, symptoms)
            assert rec.illness == name
            assert rec.symptoms == symptoms
        except:
            print(CF.LIGHTRED_EX + 'Error - while constructing a Record object. The error details are printed below:')
            raise
    except:
        time.sleep(0.01)
        traceback.print_exc()
        return False
    return True


def test_diagnose():
    if not testMethod("diagnoser.diagnose", diagnoser1.diagnose, "cold", ["cough"], diagnoser1):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser1.diagnose, "healthy", [], diagnoser1):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser2.diagnose, "influenza", ["cough", "fever"], diagnoser2):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser2.diagnose, "healthy", [], diagnoser2):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser2.diagnose, "cold", ["cough"], diagnoser2):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser2.diagnose, "influenza", ["cough", "fever"], diagnoser2):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser2.diagnose, "hard influenza", ["cough", "fever", "headache"], diagnoser2):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser3.diagnose, "hard influenza", [], diagnoser3):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser3.diagnose, "hard influenza", ["cough", "fever", "headache"], diagnoser3):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser3.diagnose, "cold", ["cough"], diagnoser3):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser3.diagnose, "influenza", ["cough", "fever"], diagnoser3):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser4.diagnose, "hard influenza", ["cough", "fever", "headache"], diagnoser4):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser4.diagnose, "influenza", [], diagnoser4):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser4.diagnose, "cold", ["cough"], diagnoser4):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser4.diagnose, "influenza", ["cough", "fever"], diagnoser4):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser5.diagnose, "influenza", [], diagnoser5):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser5.diagnose, "cold", ["headache"], diagnoser5):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser5.diagnose, "cold", ["cough"], diagnoser5):
        return False
    if not testMethod("diagnoser.diagnose", diagnoser5.diagnose, "influenza", ["cough", "headache"], diagnoser5):
        return False
    return True


def test_success_rate():
    records = [Record("influenza", ["cough", "fever"]), Record("healthy", []),
               Record('hard influenza', ["cougth", "fever", "headache"])]
    if not testMethod("diagnoser.calculate_success_rate", diagnoser1.calculate_success_rate, 0.6666666666666666,
                      records, diagnoser1):
        return False
    records = [Record("influenza", ["cough", "fever"]), Record("healthy", []),
               Record('hard influenza', ["cough", "fever", "headache"])]
    if not testMethod("diagnoser.calculate_success_rate", diagnoser2.calculate_success_rate, 1.0, records, diagnoser2):
        return False
    records = [Record("influenza", ["cough", "fever"]),
               Record("indigestion", ["stomachache"])]
    if not testMethod("diagnoser.calculate_success_rate", diagnoser2.calculate_success_rate, 0.5, records, diagnoser2):
        return False
    if not testMethod("diagnoser.calculate_success_rate", diagnoser2.calculate_success_rate, 0.0, [Record("a", ["b"])], diagnoser2):
        return False
    records = []  # test an error is thrown as requested
    if not testMethod_err("diagnoser.calculate_success_rate", diagnoser1.calculate_success_rate, ValueError, records,
                          diagnoser1):
        return False

    return True


def test_all_illnesses():
    if not testMethod("diagnoser.all_illnesses", diagnoser5.all_illnesses, ['cold', 'influenza'],
                      tuple(), diagnoser5, check_sorted=True):
        return False
    if not testMethod("diagnoser.all_illnesses", diagnoser4.all_illnesses, ["hard influenza", 'cold', 'influenza'],
                      tuple(), diagnoser4, check_sorted=True):
        return False
    if not testMethod("diagnoser.all_illnesses", diagnoser3.all_illnesses, ["hard influenza", 'cold', 'influenza'],
                      tuple(), diagnoser3, check_sorted=True):
        return False
    if not testMethod("diagnoser.all_illnesses", diagnoser2.all_illnesses, ['healthy', 'cold', 'influenza', 'hard influenza'],
                      tuple(), diagnoser2, check_sorted=True):
        return False
    if not testMethod("diagnoser.all_illnesses", diagnoser1.all_illnesses, ['healthy', 'cold', 'influenza'],
                      tuple(), diagnoser1, check_sorted=True):
        return False
    actual = diagnoser3.all_illnesses()
    if not actual[0] == 'hard influenza':
        print_fail('diagnoser.all_illnesses', tuple(), ["hard influenza", 'cold', 'influenza'], actual, diagnoser3,
                   issue="The order of your answer is not correct!")
        return False
    return True


def test_paths_to_illness():
    tests = [
        ([[True, True, False], [False]], diagnoser4, 'influenza'),
        ([[True, False]], diagnoser4, 'cold'),
        ([], diagnoser4, 'somthing_that_doesnt_exist'),
        ([[]], diagnoserRootOnly, 'cold'),
        ([[False]], diagnoser2, 'healthy'),
        ([[True, False], [False, True]], diagnoser5, 'cold'),
        ([[True, True], [True, False], [False, True], [False, False]], diagnoser7, 'x')
    ]
    for test in tests:
        expected, obj, input = test
        if not testMethod("diagnoser.paths_to_illness", obj.paths_to_illness, expected, input, obj,
                          check_sorted=True):
            return False
    return True


# TODO: test the second section of everything
from tester_helper_dont_touch import tree_builder  # TODO: rid of his import


def test_build_tree():
    args_lst = [
        (parse_data(r"tests_data/tiny_data2.txt"), ["headache", "fever"]),
        (parse_data(r"tests_data/small_data1.txt"), ["headache", "fever"]),
        (parse_data(r"tests_data/medium_data1.txt"), ['fever', 'cough']),
        (parse_data(r"tests_data/medium_data2.txt"), ['fever', 'cough']),
        (parse_data(r"tests_data/tiny_data3.txt"), [])
    ]
    expected_lst = [
        'headache fever meningitis . influenza . fever cold . healthy .',
        'headache fever influenza . cold . fever strep . healthy .',
        'fever cough influenza . meningitis . cough cold . healthy .',
        'fever cough influenza . strep . cough cold . healthy .',
        'cold .'
    ]
    for i in range(len(args_lst)):
        args = args_lst[i]
        expected = Diagnoser(tree_builder(expected_lst[i]))
        if not testMethod('build_tree', build_tree, expected, args, builtTree=True):
            return False
    args = args_lst[0]
    for val in [None, 3]:
        for i in range(2):
            new_args = tuple([arg + [val] if j == i else arg for j, arg in enumerate(args)])
            if not testMethod_err('build_tree', build_tree, TypeError, new_args, obj=None):
                return False
    void_recs = [Record(None,[])]
    vals = ['a'], ['a','b','c']
    expecs = ['a None . None .', 'a'+' b c None . None . c None . None .'*2]
    for i in range(len(vals)):
        args= (void_recs, vals[i])
        expected = Diagnoser(tree_builder(expecs[i]))
        if not testMethod('build_tree', build_tree, expected, args, builtTree=True):
            return False
    return True


def test_optimal_tree():
    data = lambda i: rf"tests_data/test_optimal_tree{i}.txt"
    args_lst = [
        (1, ["cough", "headache", "fever"], 2),
        (2, ["cough", "fever", "headache"], 1),
        (3, ['fever', 'cough', 'headache'], 2)
    ]
    ans_lst = [
        ('cough fever cold . influenza . fever meningitis . healthy .',),
        ('fever influenza . cold .',),
        ('fever cough influenza . meningitis . cough cold . healthy .',)
    ]

    for i in range(len(args_lst)):
        records = parse_data(data(args_lst[i][0]))
        args = (records, args_lst[i][1], args_lst[i][2])
        answers = [Diagnoser(tree_builder(ans)) for ans in ans_lst[i]]
        test_method = testMethod if len(answers) == 1 else testMethod_options
        if len(answers) == 1: answers = answers[0]
        if not test_method('optimal_tree', optimal_tree, answers, args, builtTree=True):
            return False
    return True


def test_optimal_tree_exeptions():
    records = parse_data(rf"tests_data/test_optimal_tree1.txt")
    args = (records, ["cough", "headache", "fever"], 2)
    for depth in [-1, -12, len(args[1]) + 1]:
        new_args = (records, args[1], depth)
        if not testMethod_err('optimal_tree', optimal_tree, ValueError, new_args):
            return False
    for val in [None, 0.4]:
        for i in range(2):
            new_args = tuple([arg + [val] if j == i else arg for j, arg in enumerate(args)])
            if not testMethod_err('optimal_tree', optimal_tree, TypeError, new_args):
                return False
    return True


def test_minimize_1():
    covid_leaf1 = Node('covid-19', None, None)
    covid_leaf2 = Node('covid-19', None, None)
    flu_leaf = Node("insomnia", covid_leaf1, covid_leaf2)
    cold_leaf = Node("cold", None, None)
    inner_vertex = Node("fever", flu_leaf, cold_leaf)
    none_node = Node(None, None, None)
    healthy_leaf = Node('healthy', None, None)
    sweat_leaf = Node("sweat", none_node, healthy_leaf)
    tree_root = Node("cough", inner_vertex, sweat_leaf)

    diagnoser = Diagnoser(tree_root)
    expected_1 = Diagnoser(tree_builder('cough fever covid-19 . cold . sweat None . healthy .'))
    expected_2 = Diagnoser(tree_builder('cough fever covid-19 . cold . healthy .'))
    if not testMethod_mutableObj('diagnoser.minimize', diagnoser.minimize, expected_1, tuple(), obj=diagnoser):
        return False
    if not testMethod_mutableObj('diagnoser.minimize', diagnoser.minimize, expected_2, True, obj=diagnoser):
        return False

    return True


def test_minimize_2():
    trees = [
        ('x y a . z . y None . None .', True),
        ('x y b None . None . d None . None . y z . a .', True),
        ('x y b None . None . d e . None . y z . a .', True),
        ('x y b None . None . d None . e . y z . a .', True),
        ('x y b e . None . d None . None . y z . a .', True),
        ('x y b None . e . d None . None . y z . a .', True),
        ('x y b None . None . d e . e . y z . a .', True),
        ('x y b e . e . d None . None . y z . a .', True),
        ('a'+' b c None . None . c None . None .'*2, True),
        ('x y a . z . z y None . None . y a . z .', True),
        ('x .', True),
        ('x y . y .', True),
        ('x y a . z . z y a None . a . z z . None . y a . z .', True),
        ('None None . None .', True),
        ('x y c . d . y b . b .', False),
        ('x y b . b . y b . c .', False),
        ('x y b . b . y b . b .', False),
        ('x y b . a . y b . a .', False),
        ('x y a . b . y b . a .', False),
        ('x y z b . a . z b . a . y z b . a . z b . a .', False),
        ('x y a . z . z y None . None . y a . z .', False),
        ('x . ', False),
        ('x y . y .', False)
    ]
    answers = [
        'y a . z .',
        'y z . a .',
        'x e . y z . a .',
        'x e . y z . a .',
        'x e . y z . a .',
        'x e . y z . a .',
        'x e . y z . a .',
        'x e . y z . a .',
        'None .',
        'y a . z .',
        'x .',
        'y .',
        'y a . z .',
        'None .',
        'x y c . d . b .',
        'x b . y b . c .',
        'b .',
        'y b . a .',
        'x y a . b . y b . a .',
        'z b . a .',
        'x y a . z . z None . y a . z .',
        'x . '
        'y .'
    ]
    time.sleep(0.1)
    for i in tqdm(range(len(answers))):
        diagnoser = Diagnoser(tree_builder(trees[i][0])) if type(trees[i][0]) is str else trees[i][0]
        expected = Diagnoser(tree_builder(answers[i]))
        if not testMethod_mutableObj('diagnoser.minimize', diagnoser.minimize, expected, trees[i][1], obj=diagnoser):
            return False
    return True


########################################TODO: enter useful methods:

# Manually build a simple tree.
#                cough
#          Yes /       \ No
#        fever           healthy
#   Yes /     \ No
# influenza   cold

def equate(a, b, builtTree=False):
    if type(a) is not type(b):
        return False
    if type(a) is Diagnoser:
        return equate(a.root, b.root, builtTree)
    if type(a) is Node:
        if not equate(a.positive_child, b.positive_child): return False
        if not equate(a.negative_child, b.negative_child): return False
        if builtTree and not is_leaf(a): return True
        return a.data == b.data
    if type(a) is Record:
        if a.illness != b.illness:
            return False
        return a.symptoms == b.symptoms
    if type(a) is list or type(a) is tuple:
        if len(a) != len(b):
            return False
        for i in range(len(a)):
            if not equate(a[i], b[i]):
                return False
        return True
    return a == b


######YOU_DONT_HAVE_ANY_THING_TO_DO_BELOW_THIS_LINE###########

def ordinal(num: int) -> str:
    num = str(int(num))
    if num[-1] == '1':
        return f'{num}st'
    if num[-1] == '2':
        return f'{num}nd'
    if num[-1] == '3':
        return f'{num}rd'
    return f'{num}th'


def randomD(minval, maxval):
    return random.random() * (maxval - minval) + minval


def list_has_duplicates(lst):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                return True
    return False


def unordered_lists_equal(lstA, lstB):
    for i in lstA:
        if i not in lstB:
            return False
    for i in lstB:
        if i not in lstA:
            return False
    return True


def generate_vec(dim):
    vec = []
    for i in range(dim):
        vec.append(randomD(-50, 50))
    return vec

    if not (len(symptoms) >= depth >= 0):
        raise ValueError(f'the depth argument must be between len(symptoms) and 0 - given {depth}')
    if sorted(symptoms) != sorted(list(set(symptoms))):
        raise ValueError('the symptoms list may not include the same symptom twice!')
    for record in records:
        if type(record) is not Record:
            raise ValueError('all elements in the records list must be of type Record!')
    for symp in symptoms:
        if type(symp) is not str:
            raise ValueError('all elements in the symptoms list must be of type str!')
    if len(symptoms) == 0:
        illness = _lst_sorted_by_count(symptoms)[0]
        return Node(illness)
    max_success = -1
    optimal_tree = None
    for combination in combinations(symptoms, depth):
        diag = build_tree(records, combination)
        tree = diag.root
        success = diag.calculate_success_rate(records)
        if success > max_success:
            max_success = success
            optimal_tree = tree


##########################################
from tester_helper_dont_touch import tree_to_str  # TODO: rid of the import


def str_of_tree(root):
    return tree_to_str(root)


def repr_obj(obj, title=True):
    if type(obj) == Diagnoser:
        title = 'Diagnoser with the following tree structure:\n' if title else ''
        return title + repr_obj(obj.root, title=False)
    if type(obj) == Node:
        title = 'Tree with the following structure:\n' if title else ''
        return title + str_of_tree(obj)
    if type(obj) == Record:
        return f'Record:{{illness=\'{obj.illness}\',symptoms={obj.symptoms}}}'
    if type(obj) == list: return '[' + ', '.join([repr_obj(e) for e in obj]) + ']'
    return str(obj)


def input_str(tup):
    if len(tup) == 0:
        return 'No Input'
    return ', '.join([repr_obj(elem) for elem in tup])


def print_error(method_name, error, arguments, expected, object):
    err = f"{CF.RED}{Style.BRIGHT}An error occurred while running the function {method_name}:\n" \
          f"{Style.NORMAL}Error: {error.__class__.__name__}\n" \
          f"Expected: {CF.WHITE}{repr_obj(expected)}{CF.RED}\n" \
          f"Object: {CF.WHITE}{repr_obj(object)}"
    print(CF.RED + err, '\n')
    print(CF.YELLOW + "Error data is specified below:")
    time.sleep(0.01)
    traceback.print_exc()


TREE_EXP_NOTE = 'Note: the symptoms written in each row of the expected tree(s) are interchangeable :)\n'


def print_fail(method_name, args, expected, actual, object, issue=None, exp_note=''):
    if type(exp_note) is not str:
        exp_note = str(exp_note) + '\n'
    elif len(exp_note) > 0 and not exp_note.endswith('\n'):
        exp_note += '\n'
    err = Style.BRIGHT + f"{CF.RED}The function {method_name} did not return expectedly:\n" \
                         f"{Style.NORMAL}Input: {input_str(args)}\n" \
                         f"Expected: {CF.WHITE}{repr_obj(expected)}{CF.RED}\n" \
                         f"{exp_note}" \
                         f"Returned Value: {CF.WHITE}{repr_obj(actual)}{CF.RED}\n"
    if issue is not None:
        err += f"Issue: {CF.WHITE}{issue}{CF.RED}\n"
    if object is not None:
        err += f"Object: {CF.WHITE}{repr_obj(object)}\n"
    print(CF.RED + err, '\n')


def print_prob(method_name, args, expected, actual, object, problem):
    err = f"{CF.RED}{Style.BRIGHT}The function {method_name} did not act expectedly:\n" \
          f"{Style.NORMAL}Input: {input_str(args)}\n" \
          f"Expected: {repr_obj(expected)}\n" \
          f"Actual: {repr_obj(actual)}\n" \
          f"The problem: {problem}\n" \
          f"Object: {repr_obj(object)}"
    print(err, '\n')


def matchFileContent_predicate(fileA, fileB):
    return filecmp.cmp(fileA, fileB)


def testMethod_err(func_name, check_func, err_type, args, obj=None):
    if type(args) != tuple:
        args = (args,)
    act_args = copy.deepcopy(args)
    try:
        val = check_func(*act_args)
    except Exception as e:
        if type(e) is err_type:
            return True
        print_fail(func_name, args, f"Error of type {err_type}", f"Error of type {type(e)}", obj)
        time.sleep(0.01)
        print(CF.LIGHTCYAN_EX + 'The Error details are specified below for you comfort:')
        time.sleep(0.01)
        traceback.print_exc()
        return False
    print_prob(func_name, args, f"Error of type {err_type}", f"Returned {val}", obj,
               problem="Didn't raise error when should have.")


def testMethod_options(func_name, check_func, expected_options, args, obj=None, check_sorted=False,
                       mutableArgCheck=True, mutableObjCheck=True, builtTree=False):
    expected_msg = f'One of the {len(expected_options)} following options:\n' + '\nor '.join(
        [repr_obj(opt) for opt in expected_options])

    def predicate(val, act_args, org_args, obj):
        ok_types = {type(expected) for expected in expected_options}
        if type(val) not in ok_types:
            expected_types_str = ' or '.join([t.__name__ for t in ok_types])
            print(
                CF.LIGHTRED_EX + Style.BRIGHT + f'NOTE: YOU RETURNED A VALUE OF TYPE "{type(val).__name__}". ARE YOU SURE YOU SHOULD RETURN A VALUE OF THAT TYPE? (AND NOT {expected_types_str})  :' + Style.NORMAL)
            return False
        for expected in expected_options:
            if type(val) != type(expected):
                return False
            if check_sorted and sorted(val) == sorted(expected): return True
            if equate(val, expected, builtTree=builtTree): return True
        return False

    exp_note = TREE_EXP_NOTE if builtTree else ''
    testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck, mutableObjCheck,
                         exp_note=exp_note)


def testMethod(func_name, check_func, expected, args, obj=None, check_sorted=False, mutableArgCheck=True,
               mutableObjCheck=True, builtTree=False):
    expected_msg = expected

    def predicate(val, actual_args, original_args, obj):
        if type(val) != type(expected):
            print(
                CF.LIGHTRED_EX + Style.BRIGHT + f'NOTE: YOU RETURNED A VALUE OF TYPE "{type(val).__name__}". ARE YOU SURE YOU SHOULD RETURN A VALUE OF THAT TYPE? (AND NOT {type(expected).__name__})  :' + Style.NORMAL)
            return False
        if check_sorted: return sorted(val) == sorted(expected)
        return equate(val, expected, builtTree=builtTree)

    exp_note = TREE_EXP_NOTE if builtTree else ''
    return testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck,
                                mutableObjCheck, exp_note=exp_note)


def testMethod_arg(func_name, check_func, expected, args, arg_to_check: int, obj, check_sorted=False,
                   mutableArgCheck=True, mutableObjCheck=True):
    expected_msg = expected

    def predicate(val, actual_args, original_args, obj):
        if check_sorted: return sorted(actual_args[arg_to_check]) == sorted(expected)
        return equate(actual_args[arg_to_check], expected)

    return testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck,
                                mutableObjCheck)


def testMethod_mutableObj(func_name, check_func, expected, args, obj, mutableArgCheck=True):
    expected_msg = expected

    def predicate(val, actual_args, original_args, obj):
        return equate(expected, obj)
    exp_note = f'Note: before the method was called, the object was: {repr_obj(obj)}'
    return testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj, mutableArgCheck,
                                mutableObjCheck=False,exp_note=exp_note)


def testMethod_predicate(func_name, check_func, predicate, expected_msg, args, obj=None, mutableArgCheck=True,
                         mutableObjCheck=True, exp_note=''):
    if type(args) != tuple:
        args = (args,)
    actual_args = copy.deepcopy(args)
    actual_obj = copy.deepcopy(obj)
    try:
        val = check_func(*actual_args)
    except Exception as e:
        print_error(func_name, e, args, expected_msg, obj)
        return False
    if not predicate(val, actual_args, args, obj):
        print_fail(func_name, args, expected_msg, val, obj, exp_note=exp_note)
        return False
    if mutableArgCheck and pickle.dumps(args) != pickle.dumps(actual_args):
        print_prob(func_name, args, expected_msg, val, obj,
                   "The function changed the value of some mutable arguments, this is not allowed!")
        return False
    if mutableObjCheck and not pickle.dumps(obj) == pickle.dumps(actual_obj):
        print_prob(func_name, args, expected_msg, val, obj,
                   f"The function changed the value of fields of the object, this is not allowed!\nOriginal object's state:\n {repr_obj(obj)}")
        return False
    return True


####################################
def read_code_array2D(*filenames):
    code = []
    for filename in filenames:
        file = open(filename + ".py")
        lines = file.readlines()
        code.append(lines)
        file.close()
    return code


def read_code_array2D_from_zip(zipfilename, *filenames):
    code = []
    archive = zipfile.ZipFile(zipfilename + ".zip")
    for filename in filenames:
        file = archive.open(filename + ".py")
        lines = file.readlines()
        code.append(lines)
        file.close()
    return code


def import_files_dynamically(*filenames):
    import_cmds = ['from ' + fname + ' import *' for fname in filenames]
    import_cmds = '\n'.join(import_cmds)
    exec(import_cmds, globals())


class CWDLoader:
    def __init__(self):
        self.newPath = os.path.dirname(os.path.abspath(__file__))

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def main():
    try:
        colorInit()
        with CWDLoader():
            should_test_zip = input('type a number if you wish this program to read from a zip file:')
            should_test_zip = regex.match('\s*\d', should_test_zip)
            if should_test_zip:

                if not ENABLE_ZIP:
                    print("\nSorry but this week's tester doesn't support zip checks.")
                    print('Please run this tester on a python file, Thank you :) \n')
                    sys.exit(0)
                print('loading files from zip: ' + zip_filename + ".zip")
                sys.path.insert(0, zip_filename + ".zip")
                code = read_code_array2D_from_zip(zip_filename, *filenames)
            else:
                print('loading files:', *[fn + '.py' for fn in filenames])
                code = read_code_array2D(*filenames)
            if DYNAMIC_IMPORT: import_files_dynamically(*filenames)
            print(CF.CYAN + 'files loaded. now running tests...\n')
            res = test_raw_code(copy.deepcopy(code), filenames)
            if res is False:
                sys.exit(0)
            print(CF.WHITE + 'finished basic formatting test')

            print(' ')
            test_main()
            print(CF.RESET)
    except OSError as ose:
        d = os.path.dirname(os.path.abspath(__file__))
        print(CF.MAGENTA + 'could not find/load required files from folder:', d)
        raise ose
    except Exception:
        print(CF.MAGENTA + "the tester has thrown an error. please report to yair =) ")
        raise
    finally:
        time.sleep(0.1)
        input(CF.WHITE + "\nType enter when you are finished:")


flu_leaf = Node("influenza", None, None)
cold_leaf = Node("cold", None, None)
inner_vertex = Node("fever", flu_leaf, cold_leaf)
healthy_leaf = Node("healthy", None, None)
root = Node("cough", inner_vertex, healthy_leaf)

diagnoser1 = Diagnoser(root)

flu_leaf2 = Node("influenza", None, None)
cold_leaf2 = Node("cold", None, None)
hard_leaf2 = Node("hard influenza", None, None)
headache_node2 = Node("headache", hard_leaf2, flu_leaf2)
inner_vertex2 = Node("fever", headache_node2, cold_leaf2)
healthy_leaf2 = Node("healthy", None, None)
root2 = Node("cough", inner_vertex2, healthy_leaf2)

diagnoser2 = Diagnoser(root2)
# Manually build of diagnoser2.
#                          cough
#                    Yes /       \ No
#                  fever           healthy
#             Yes /     \ No
#            headache   cold
#       Yes /     \ No
# hard influenza influenza

flu_leaf3 = Node("influenza", None, None)
cold_leaf3 = Node("cold", None, None)
hard_leaf3 = Node("hard influenza", None, None)
headache_node3 = Node("headache", hard_leaf3, flu_leaf3)
inner_vertex3 = Node("fever", headache_node3, cold_leaf3)
healthy_leaf3 = Node("hard influenza", None, None)
root3 = Node("cough", inner_vertex3, healthy_leaf3)

diagnoser3 = Diagnoser(root3)
# Manually build of diagnoser3.
#                          cough
#                    Yes /       \ No
#                  fever       hard influenza
#             Yes /     \ No
#            headache   cold
#       Yes /     \ No
# hard influenza influenza

flu_leaf4 = Node("influenza", None, None)
cold_leaf4 = Node("cold", None, None)
hard_leaf4 = Node("hard influenza", None, None)
headache_node4 = Node("headache", hard_leaf4, flu_leaf4)
inner_vertex4 = Node("fever", headache_node4, cold_leaf4)
healthy_leaf4 = Node("influenza", None, None)
root4 = Node("cough", inner_vertex4, healthy_leaf4)

diagnoser4 = Diagnoser(root4)
# Manually build of diagnoser4.
#                          cough
#                    Yes /       \ No
#                  fever        influenza
#             Yes /     \ No
#            headache   cold
#       Yes /     \ No
# hard influenza influenza

flu_leaf5 = Node("influenza", None, None)
cold_leaf5 = Node("cold", None, None)
cold_leaf6 = Node('cold', None, None)
healthy_leaf5 = Node("influenza", None, None)
inner_vertex6 = Node("headache", cold_leaf5, healthy_leaf5)
inner_vertex5 = Node("headache", flu_leaf5, cold_leaf6)
root5 = Node("cough", inner_vertex5, inner_vertex6)

diagnoser5 = Diagnoser(root5)
# Manually build of diagnoser5.
#                          cough
#                    Yes /       \ No
#                     headache  headache
#             Yes /     \ No  Yes /     \ No
#           influenza  cold     cold    healthy

root6 = Node("cold", None, None)
diagnoserRootOnly = Diagnoser(root6)


x_1 = Node("x", None, None)
x_2 = Node("x", None, None)
x_3 = Node("x", None, None)
x_4 = Node("x", None, None)
inner_vertex7 = Node("b", x_1, x_2)
inner_vertex8 = Node("b", x_3, x_4)
root7 = Node("a", inner_vertex7, inner_vertex8)

diagnoser7 = Diagnoser(root7)
#   _a_
#  /   \
#  b   b
# / \ / \
# x x x x

if __name__ == '__main__':
    main()
