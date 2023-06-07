
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


def num_of_orthogonal(vectors):
    """this function get"""
    lst = []
    count = 0
    for i in range(len(vectors[0])):
        for k in range(1,len(vectors[0])):
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
print(sum_of_vectors([[1, 1], [1, 3]]))

print(num_of_orthogonal([[0,0],[1,2],[10,3]]))