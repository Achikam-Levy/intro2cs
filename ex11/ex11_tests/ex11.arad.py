#############################################################
# FILE: lab1.py
# WRITER: arad tal , aradtal , 209327527
# EXRECISE: intro2cs ex11 2021
# DESCRIPTION:build binary tree
#############################################################

from typing import List, Dict, Optional
from itertools import combinations

Symptoms = List[str]


class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
        self.data = data
        self.positive_child = positive_child
        self.negative_child = negative_child

    def is_leaf(self):
        if self.negative_child:
            return False
        if self.positive_child:
            return False
        return True


class Record:
    def __init__(self, illness, symptoms):
        self.illness = illness
        self.symptoms = symptoms


def parse_data(filepath) -> List[Record]:
    with open(filepath) as data_file:
        records = []
        for line in data_file:
            words = line.strip().split()
            records.append(Record(words[0], words[1:]))
        return records


class Diagnoser:
    def __init__(self, root: Node):
        self.root = root

    def diagnose(self, symptoms: Symptoms):
        cur = self.root
        while cur.negative_child or cur.positive_child:
            if cur.data in symptoms:
                cur = cur.positive_child
            else:
                cur = cur.negative_child
        return cur.data

    def calculate_success_rate(self, records: List[Record]) -> float:
        success = 0
        num_of_records = 0
        for record in records:
            num_of_records += 1
            if self.diagnose(record.symptoms) == record.illness:
                success += 1
        if num_of_records <= 0:
            raise ValueError("must have records")
        return success / num_of_records

    def all_illnesses_minimize(self):
        if not self.root:
            return []
        all_dict = {}
        self.all_illnesess_helper(all_dict)
        sorted_dict = sorted(all_dict.items(), key=lambda x: x[1], reverse=True)
        all_illnesses_list = [i for i, j in sorted_dict]
        return all_illnesses_list

    def all_illnesses(self):
        all_init = self.all_illnesses_minimize()
        update = [i for i in all_init if i]
        return update
    #

    def have_child(self) -> bool:
        if self.root.negative_child:
            return True
        if self.root.positive_child:
            return True
        return False

    def all_illnesess_helper(self, all_list: Dict[str, int]) -> Dict[str, int]:
        if not self.have_child():
            if self.root.data in all_list.keys():
                all_list[self.root.data] += 1
            else:
                all_list[self.root.data] = 1
        if self.root.negative_child:
            Diagnoser(self.root.negative_child).all_illnesess_helper(all_list)
        if self.root.positive_child:
            Diagnoser(self.root.positive_child).all_illnesess_helper(all_list)
        return all_list

    def paths_to_illness(self, illness: str) -> Optional[List[List[bool]]]:
        all_illnesses = self.all_illnesses_minimize()
        if illness not in all_illnesses:
            return []
        all_path = self.path_to_illness_helper([], illness, [])
        if all_path:
            return all_path
        else:
            return [[]]

    def path_to_illness_helper(self, all_path: List[List[bool]], illness: str, rout: List[bool]) -> Optional[
        List[List[bool]]]:
        # if not self.root.data:
        #     return
        if not self.have_child():
            if illness in all_path:
                return
            if self.root.data == illness:
                new_rout = [i for i in rout]
                all_path.append(new_rout)
            return

        rout.append(True)
        Diagnoser(self.root.positive_child).path_to_illness_helper(all_path, illness, rout)
        rout.pop(-1)

        rout.append(False)
        Diagnoser(self.root.negative_child).path_to_illness_helper(all_path, illness, rout)
        rout.pop(-1)

        return all_path

    def all_symptoms(self, lst) -> Optional[List[str]]:
        if self.root.is_leaf():
            return
        lst.append(self.root.data)
        Diagnoser(self.root.positive_child).all_symptoms(lst)
        Diagnoser(self.root.negative_child).all_symptoms(lst)
        return lst



    def minimize(self, remove_empty=False):
        self.minimize_helper(remove_empty)
        # if self.root.is_leaf():
        #     return self
        # return self

    def minimize_helper(self, remove_empty=False):
        if not self.root:
            return
        if self.root.is_leaf():
            return self

        negative_minimize = Diagnoser(self.root.negative_child).minimize_helper(remove_empty)
        positive_minimize = Diagnoser(self.root.positive_child).minimize_helper(remove_empty)

        if self.root.is_leaf():
            return self

        all_illnesess_negative = None
        all_symptoms_neg = []
        all_illnesess_positive = None
        all_symptoms_pos = []
        if positive_minimize:
            all_illnesess_positive = positive_minimize.all_illnesses_minimize()
            all_symptoms_pos.append(positive_minimize.all_symptoms([]))
        if negative_minimize:
            all_symptoms_neg.append(negative_minimize.all_symptoms([]))
            all_illnesess_negative = negative_minimize.all_illnesses_minimize()



        if set(all_illnesess_positive) == set(all_illnesess_negative):
            for ill in all_illnesess_positive:
                neg_path = negative_minimize.paths_to_illness(ill)
                pos_path = positive_minimize.paths_to_illness(ill)
                if neg_path != pos_path:
                    break
                else:
                    if all_symptoms_neg == all_symptoms_pos:
                        self.root = positive_minimize.root
                    return self


        if positive_minimize and positive_minimize.root.data:
            self.root.positive_child = positive_minimize.root
            if not negative_minimize or not negative_minimize.root.data:
                if remove_empty:
                    self.root = self.root.positive_child
        if negative_minimize and negative_minimize.root.data:
            self.root.negative_child = negative_minimize.root
            if not positive_minimize or not positive_minimize.root.data:
                if remove_empty:
                    self.root = self.root.negative_child
        if not remove_empty:
            if negative_minimize and not negative_minimize.root.data:
                self.root.negative_child = negative_minimize.root
            if positive_minimize and not positive_minimize.root.data:
                self.root.positive_child = positive_minimize.root

        return self


def check_valid_build_tree(records: List[Record], symptoms: List[str]) -> None:
    for record in records:
        if not isinstance(record, Record):
            raise TypeError('Record is not Record type')
    for symptom in symptoms:
        if not isinstance(symptom, str):
            raise TypeError('not a valid symptom')


def build_tree(records: List[Record], symptoms: List[str]):
    check_valid_build_tree(records=records, symptoms=symptoms)
    new_tree = create_cross(current_branch=records, symptoms=symptoms, counter=0)
    return Diagnoser(new_tree)


def find_most_common_illness(record_list: List[Record]) -> Optional[str]:
    select_ill = {}
    if not record_list:
        return
    for record in record_list:
        if record.illness not in select_ill:
            select_ill[record.illness] = 1
        else:
            select_ill[record.illness] += 1
    most_common = max(select_ill.items(), key=lambda x: x[1])
    return most_common[0]


def create_cross(symptoms: List[str], current_branch: List[Record], counter) -> Node:
    if len(symptoms) == counter:
        most_common = find_most_common_illness(current_branch)
        return Node(most_common)

    new_node = Node(symptoms[counter])

    positive_option = [record for record in current_branch if symptoms[counter] in record.symptoms]
    new_node.positive_child = create_cross(symptoms, positive_option, counter + 1)

    negative_options = [record for record in current_branch if symptoms[counter] not in record.symptoms]
    new_node.negative_child = create_cross(symptoms, negative_options, counter + 1)

    return new_node


def check_optimal_tree_variable(symptoms: List[str], depth: int) -> None:
    #check duplicate symptoms
    for symptom in symptoms:
        for other_symptom in symptoms:
            if symptom == other_symptom and symptom is not other_symptom:
                raise ValueError('incorrect value')
        # check type
        if not isinstance(symptom, str):
            raise TypeError('incorrect type')
    #check depth validity
    if not 0 <= depth <= len(symptoms):
        raise ValueError('incorrect depth')


def optimal_tree(records: List[Record], symptoms: List[str], depth: int) -> Diagnoser:
    check_optimal_tree_variable(symptoms, depth)
    comb_lst = list(combinations(symptoms, depth))
    result_lst = []
    for combination in comb_lst:
        new_tree = build_tree(records, combination)
        result_lst.append((new_tree, new_tree.calculate_success_rate(records)))
    opt_tree = max(result_lst, key=lambda x: x[1])
    return opt_tree[0]







if __name__ == "__main__":
    print(build_tree(parse_data(
        '/Users/hyqmlwy/Desktop/intro/exercises/week11/ex11/testssss/Data/big_data.txt'),
                     ['congestion', 'cough', 'fatigue', 'fever', 'headache',
                      'irritability']))





