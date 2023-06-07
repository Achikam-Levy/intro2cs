#################################################################
# FILE : shapes.py
# WRITER : achikam levy , aaa997 , 208764944
# EXERCISE : intro2cs2 ex2 2020
# DESCRIPTION:
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################




def input_list():
    """this function get numbers from user
     and returns list of the numbers and their sum"""
    list_of_numbers = []
    sum_numbers = 0
    x = input()
    while x != '':
        sum_numbers += float(x)
        list_of_numbers.append(float(x))
        x = input()
    list_of_numbers.append(sum_numbers)
    return list_of_numbers


def inner_product(vec_1, vec_2):
    """this function get two vectors and returns their scalar product"""
    sum_all = 0
    if len(vec_1) == len(vec_2):
        for i in range(len(vec_1)):
            sum_i = vec_1[i]*vec_2[i]
            sum_all = sum_all + sum_i
    else:
        return None
    return sum_all


def sequence_monotonicity(sequence):
    """this function get list of numbers
     and return bool values according to their order"""
    [a, b, c, d] = [True, True, True, True]
    for i in range(1, len(sequence)):
        if sequence[0] <= sequence[i]:
            if sequence[i] == sequence[i - 1]:
                b = False
                break
            if sequence[0] < sequence[i]:
                if sequence[i] >= sequence[i-1] and sequence[0] <= sequence[i]:
                    c = False
                    d = False
    for i in range(1, len(sequence)):
        if sequence[0] >= sequence[i]:
            if sequence[i] == sequence[i - 1]:
                d = False
                break
            if sequence[0] > sequence[i]:
                if sequence[i] <= sequence[i-1] and sequence[0] >= sequence[i]:
                    a = False
                    b = False
    for i in range(1,len(sequence)):
        if sequence[0] == sequence[i]:
            [a, b, c, d] = [False, False, False, False, ]
            if sequence[i] == sequence[i-1]:
                [a, b, c, d] = [True, False, True, False, ]
    return[a, b, c, d]


def monotonicity_inverse(def_bool):
    """this function get bool values and returns list of numbers
     according to the values order"""
    if def_bool[2] == False and def_bool[3] == False:
        if def_bool[0] == False and def_bool[1] == False:
            return [1 ,-1 ,0 ,1]
        if def_bool[0] == True:
            if def_bool[1] == True:
                return [1, 2, 3, 4]
            else:
                return [1, 2, 2, 4]
    elif def_bool[0] == False and def_bool[1] == False:
        if def_bool[2] == True:
            if def_bool[3] == True:
                return [4, 3, 2, 1]
            else:
                return [4, 3, 3, 1]
    elif (def_bool[0] == True and def_bool[2] == True
        and def_bool[1] == False and def_bool[3] == False):
        return [1, 1, 1, 1]
    else:
        return None


def primes_for_asafi(n):
    """this function get one 'n' number,
    and returns all tha first 'n' prime numbers"""
    def if_num_is_prime(num):
        if num == 1:
            return False
        if num == 2:
            return True
        for i in range(2, num):
            if num % i == 0:
                return False
        else:
            return True
    if n == 0:
        return []
    if n == 1:
        return [2]
    lst_prime = []
    while True:
        for i in range(2, n**2):
            z = if_num_is_prime(i)
            if z is True:
                lst_prime.append(i)
                if len(lst_prime) == n:
                    return lst_prime


def sum_of_vectors(vec_lst):
    """this function calculate tha sum of numbers lists"""
    vectors_sum = []
    vectors_sum1 = []
    y = 0
    if not vec_lst:
        return 'None'
    for k in range(len(vec_lst[0])):
        y = 0
        for i in range( len(vec_lst)):
            x = vec_lst[i][k]
            y = y + x
        vectors_sum1.append(y)
    return vectors_sum1



def num_of_orthogonal(vectors):
    """this function list of vectors,
     and returns the numbers of orthogonal vectors"""
    lst = []
    count = -1
    if len(vectors[0]) == 1:
        for i in range(len((vectors))):
            for k in range(1, len(vectors)):
                x = vectors[i][0] * vectors[k][0]
                if x == 0:
                    count = count + 1
        return count - (count//2)
    count = 0
    for i in range(len(vectors[0])):
        for k in range(1, len(vectors[0])):
            x = inner_product(vectors[i], vectors[k])
        lst.append(x)
    if 0 in lst:
        for i in lst:
            count = count + i
            if count == 0:
                return len(lst)
            else:
                return len(lst)-1
    else:
        return 0



