#################################################################
# FILE : ex11.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex6 2021
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################

import operator
import copy
from collections import Counter
import itertools



class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child

    def insert_node_in_all_leaves(self, cur_node, old_nodes, symptom):
        if cur_node.positive_child is None and cur_node.negative_child is None:
            cur_node.positive_child = Node(symptom, None, None)
            cur_node.negative_child = Node(symptom, None, None)
            return
        if cur_node.positive_child is not None:
            self.insert_node_in_all_leaves(cur_node.positive_child,
                                           old_nodes, symptom)
            self.insert_node_in_all_leaves(cur_node.negative_child,
                                           old_nodes, symptom)


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath):
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root: Node):
        self.root = root

    def diagnose(self, symptoms):
        """
        :param symptoms: symptoms of illness
        :return: the illness match to the symptoms
        """
        diagnose = self.diagnose_searcher(symptoms, self.root)
        return diagnose

    def diagnose_searcher(self, symptoms, cur_node):
        """
        fine the required illness by recursive
        :param symptoms: symptoms of illness
        :param cur_node: the current symptom of the childes of the nodes
        :return: the match illness
        """
        if cur_node.data in symptoms:
            if cur_node.positive_child is None and cur_node.negative_child is None:
                # checks if the root is a leaf, and returns the right illness
                return cur_node.data
            return self.diagnose_searcher(symptoms, cur_node.positive_child)

        else:
            if cur_node.positive_child is None and cur_node.negative_child is None:
                # checks if the root is a leaf, and returns the right illness
                return cur_node.data
            return self.diagnose_searcher(symptoms, cur_node.negative_child)

    def calculate_success_rate(self, records):
        """
        :param records: list of illnesses and symptoms
        :return: the match success_rate
        """
        if len(records) == 0:
            raise ValueError("njkbjb")
        counter = 0
        for record in records:
            if record.illness == self.diagnose(record.symptoms):
                counter += 1
        return counter / len(records)

    def all_illnesses(self):
        """
        find all illnesses of given tree
        :return: list of illnesses
        """
        old_nodes = {}
        ill_dict = {}
        self.all_illnesses_helper(self.root, ill_dict, old_nodes)
        sorted_ill_dict = dict(
            sorted(ill_dict.items(), key=operator.itemgetter(1), reverse=True))
        lst = [key for key in sorted_ill_dict]
        for i in lst:
            if i is None:
                lst.remove(i)
        return lst

    def all_illnesses_helper(self, cur_node, ill_dict, old_nodes):
        """
        :param cur_node: current symptom
        :param ill_dict: dict of found illnesses
        :param old_nodes: dict of old nodes
        :return: ill dict
        """
        if cur_node.positive_child is None and cur_node.negative_child is None:
            if cur_node.data not in ill_dict:
                ill_dict[cur_node.data] = 1
            else:
                ill_dict[cur_node.data] += 1
            return self.all_illnesses_helper(self.root, ill_dict, old_nodes)
        if cur_node not in old_nodes:
            old_nodes[cur_node] = cur_node
            if cur_node.positive_child is not None and cur_node.negative_child is not None:
                self.all_illnesses_helper(cur_node.positive_child, ill_dict,
                                          old_nodes)
                self.all_illnesses_helper(cur_node.negative_child, ill_dict,
                                          old_nodes)

    def paths_to_illness(self, illness):
        """
        :param illness: fined a path/path's to a given illness
        :return: list of bool values according to the matches symptoms
        """
        big_lst = []
        lst = []
        self.paths_to_illness_helper(self.root, lst, big_lst, illness)
        return big_lst

    def paths_to_illness_helper(self, cur_node, lst, big_lst, illness):
        """
        :param cur_node: current node
        :param lst: empty list represent one path
        :param big_lst: list of all path's
        :param illness: the given illness
        :return: big_lst
        """
        if cur_node.positive_child is None and cur_node.negative_child is None:
            if cur_node.data == illness and cur_node:
                big_lst.append(lst)
                return big_lst
        if cur_node.positive_child is not None and cur_node.negative_child is not None:
            positive_lst = copy.deepcopy(lst)
            positive_lst.append(True)
            negative_lst = copy.deepcopy(lst)
            negative_lst.append(False)
            self.paths_to_illness_helper(cur_node.positive_child, positive_lst,
                                         big_lst, illness)
            self.paths_to_illness_helper(cur_node.negative_child, negative_lst,
                                         big_lst, illness)

    def remove_node(self, cur_node, new_node):
        cur_node.data = new_node.data
        cur_node.positive_child = new_node.positive_child
        cur_node.negative_child = new_node.negative_child

    def minimize(self, remove_empty=False):
        """
        running tha main function
        :param remove_empty: bool value
        :return: None
        """
        for i in range(10000):
            self.main(self.root, remove_empty)

    def what_to_remove(self, cur_node):
        """
        checks which node to remove
        :param cur_node: current Node
        :return: None
        """
        if cur_node.negative_child is not None:
            self.remove_node(cur_node, cur_node.negative_child)
            return
        if cur_node.positive_child is not None:
            self.remove_node(cur_node, cur_node.positive_child)
            return

    def main(self, cur_node, remove_empty):
        """
        the main function checks recursive if same_subtrees for all the tree nodes
        :param cur_node: current node
        :param remove_empty: bool value
        :return: None
        """
        if cur_node.positive_child is None and cur_node.negative_child is None:
            return

        if self.same_subtrees(cur_node.positive_child, cur_node.negative_child,):
            self.what_to_remove(cur_node)
            return

        if remove_empty:
            if cur_node.negative_child.data is None:
                self.remove_node(cur_node.negative_child,
                                 cur_node.positive_child)
            if cur_node.positive_child.data is None:
                self.remove_node(cur_node.positive_child,
                                 cur_node.negative_child)
            if self.same_subtrees(self.root.positive_child,
                                  self.root.negative_child,):
                self.what_to_remove(cur_node)

        if cur_node.positive_child is not None:
            self.main(cur_node.positive_child, remove_empty)
        if cur_node.negative_child is not None:
            self.main(cur_node.negative_child, remove_empty)

    def same_subtrees(self, left_cur_node, right_cur_node):
        """
        checks if two node subtrees are identical
        :param left_cur_node: cur_node positive child
        :param right_cur_node: cur_node positive child
        :return: bool value
        """
        if left_cur_node is None and right_cur_node is None:
            return True

        if left_cur_node is not None and right_cur_node is not None:
            return ((left_cur_node.data == right_cur_node.data) and
                    self.same_subtrees(left_cur_node.positive_child,
                                       right_cur_node.positive_child, ) and
                    self.same_subtrees(left_cur_node.negative_child,
                                       right_cur_node.negative_child, ))
        return False


def fined_illness_place(cur_node, symptoms, record):
    """
    fined a leaf end put in the leaf data(list) th right illness
    :param cur_node: current node
    :param symptoms: tree symptoms
    :param record: current record
    :return:None
    """
    if cur_node.data == symptoms[-1]:
        if record.symptoms == [] and cur_node.data in symptoms and record.illness is None:
            cur_node.positive_child = Node([record.illness], None, None)
            cur_node.negative_child = Node([record.illness], None, None)
        if cur_node.data in record.symptoms or cur_node.data == 'None':
            if cur_node.positive_child is None or cur_node.data == 'None':
                cur_node.positive_child = Node([record.illness], None, None)
                return
            else:
                if type(cur_node.positive_child.data) is list:
                    cur_node.positive_child.data.append(record.illness)
                    return
        if cur_node.data not in record.symptoms:

            if cur_node.negative_child is None:
                cur_node.negative_child = Node([record.illness], None, None)

                return
            else:
                if type(cur_node.negative_child.data) is list:
                    cur_node.negative_child.data.append(record.illness)
                    return

    if cur_node.data in record.symptoms or record.symptoms == []:
        fined_illness_place(cur_node.positive_child, symptoms, record)
    if cur_node.data not in record.symptoms or record.symptoms == []:
        fined_illness_place(cur_node.negative_child, symptoms, record)


def finel_illness_place(cur_node, symptoms):
    """
    put the finel illness in every leaf according to the leaf data
    :param cur_node: current node
    :param symptoms: tree symptoms
    :return: None
    """
    if cur_node.data == symptoms[-1]:
        if cur_node.positive_child is None:
            pass
        else:
            cur_node.positive_child.data = \
                Counter(cur_node.positive_child.data).most_common()[0][0]
        if cur_node.negative_child is None:
            pass
        else:
            cur_node.negative_child.data = \
                Counter(cur_node.negative_child.data).most_common()[0][0]

    if cur_node.positive_child is not None:
        finel_illness_place(cur_node.positive_child, symptoms)
    if cur_node.negative_child is not None:
        finel_illness_place(cur_node.negative_child, symptoms)


def build_tree(records, symptoms):
    """
    build tree according to given records and symptoms
    :param records: illness name and illness symptoms
    :param symptoms: symptoms to the tree
    :return: fit object diagnoser
    """
    for symptom in symptoms:
        if not isinstance(symptom, str):
            raise TypeError("symptoms must contain string objects")
    for record in records:
        if not isinstance(record, Record):
            raise TypeError("records must contain Records objects")

    if not records and not symptoms:
        return Diagnoser(Node(None, None, None))

    if records == []:
        records = [Record(None, [])]

    if not symptoms:
        lst = []
        for record in records:
            lst.append(record.illness)
        root = Node(Counter(lst).most_common()[0][0], None, None)
        return Diagnoser(root)

    root = Node(symptoms[0], None, None)
    old_nodes = {}
    for i in range(1, len(symptoms)):
        if not isinstance(symptoms[i], str):
            raise TypeError("symptoms must contain string objects")
        root.insert_node_in_all_leaves(root, old_nodes, symptoms[i])
    diagnoser = root
    for record in records:
        if not isinstance(record, Record):
            raise TypeError("records must contain Records objects")
        fined_illness_place(diagnoser, symptoms, record)
    finel_illness_place(diagnoser, symptoms)
    return Diagnoser(diagnoser)


def optimal_tree(records, symptoms, depth):
    """
    checks what the optimal tree diagnose wise
    :param records: illness name and illness symptoms
    :param symptoms: symptoms to the tree
    :param depth: the depth of the tree
    :return: optimal tree
    """
    if depth < 0 or depth > len(symptoms):
        raise ValueError("depth value must be -  len(symptoms) ≥ depth ≥ 0",
                         ValueError)
    combinations = itertools.combinations(symptoms, depth)
    tree_optimal = ["", 0]
    for combination in combinations:
        tree = build_tree(records, combination)
        successes_rate = tree.calculate_success_rate(records)
        if successes_rate >= tree_optimal[1]:
            tree_optimal[0] = tree
            tree_optimal[1] = successes_rate
    return tree_optimal[0]


if __name__ == "__main__":
    print(build_tree(parse_data('/Users/hyqmlwy/Desktop/intro/exercises/week11/ex11/testssss/Data/big_data.txt'),
                     ['congestion', 'cough', 'fatigue', 'fever', 'headache',
                      'irritability']))