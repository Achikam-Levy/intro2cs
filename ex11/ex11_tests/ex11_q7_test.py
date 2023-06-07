from ex11 import Node, Diagnoser, Record, build_tree, optimal_tree, parse_data

#									Tree 1
#                cough  				 		  cough
#          Yes /       \ No 				Yes /       \ No
#        fever           healthy  -->		cold	   healthy
#   Yes /     \ No
# 	cold      cold

pos_pos1 = Node("cold", None, None)
pos_neg1 = Node("cold", None, None)

pos1 = Node("fever", pos_pos1, pos_neg1)
neg1 = Node("healthy", None, None)

root1 = Node("cough", pos1, neg1)
tree1 = Diagnoser(root1)



def test_minimize1():
    tree1.minimize(False)
    assert tree1.root.data == 'cough'
    assert tree1.root.positive_child.data == 'cold'
    assert tree1.root.negative_child.data == 'healthy'
    assert tree1.root.positive_child.positive_child is None
    assert tree1.root.positive_child.negative_child is None


#										Tree 2
#		                cough  				 		  cough
#		          Yes /       \ No 				Yes /       \ No
#		        fever           healthy  -->  influenza	    healthy
#		   Yes /     \ No
#		 headache   influenza
#		Yes /   \ No
#    influenza influenza
pos_pos_pos2 = Node('influenza', None, None)
pos_pos_neg2 = Node('influenza', None, None)

pos_pos2 = Node("headache", pos_pos_pos2, pos_pos_neg2)
pos_neg2 = Node("influenza", None, None)

pos2 = Node("fever", pos_pos2, pos_neg2)
neg2 = Node("healthy", None, None)

root2 = Node("cough", pos2, neg2)
tree2 = Diagnoser(root2)


def test_minimize2():
    tree2.minimize()
    assert tree2.root.data == 'cough'
    assert tree2.root.positive_child.data == 'influenza'
    assert tree2.root.negative_child.data == 'healthy'
    assert tree2.root.positive_child.positive_child is None
    assert tree2.root.positive_child.negative_child is None


#										Tree 3
#		                cough  				 		  cough
#		          Yes /       \ No 				Yes /       \ No
#		           fever      healthy   -->  influenza	    healthy
#		      Yes /     \ No
#		 headache   	  cold
#		Yes /   \ No	Yes /    \ No
#    influenza influenza  influenza influenza


pos_pos_pos3 = Node('influenza', None, None)
pos_pos_neg3 = Node('influenza', None, None)

pos_neg_pos3 = Node('influenza', None, None)
pos_neg_neg3 = Node('influenza', None, None)

pos_pos3 = Node("headache", pos_pos_pos3, pos_pos_neg3)
pos_neg3 = Node("cold", pos_neg_pos3, pos_neg_neg3)

pos3 = Node("fever", pos_pos3, pos_neg3)
neg3 = Node("healthy", None, None)

root3 = Node("cough", pos3, neg3)
tree3 = Diagnoser(root3)


def test_minimize3():
    tree3.minimize()
    assert tree3.root.data == 'cough'
    assert tree3.root.positive_child.data == 'influenza'
    assert tree3.root.negative_child.data == 'healthy'
    assert tree3.root.positive_child.positive_child is None
    assert tree3.root.positive_child.negative_child is None


#										Tree 4
#                          cough							  cough
#                    Yes /       \ No					 Yes /       \ No
#                 headache       headache       -->		   cold    influenza
#             Yes /     \ No  Yes /     \ No
#           cold        cold   influenza    influenza


pos_neg4 = Node("cold", None, None)
pos_pos4 = Node("cold", None, None)

neg_neg4 = Node("influenza", None, None)
neg_pos4 = Node("influenza", None, None)

neg4 = Node("headache", neg_pos4, neg_neg4)
pos4 = Node("headache", pos_pos4, pos_neg4)
root4 = Node("cough", pos4, neg4)
tree4 = Diagnoser(root4)


def test_minimize4():
    tree4.minimize()
    assert tree4.root.data == 'cough'
    assert tree4.root.positive_child.data == 'cold'
    assert tree4.root.negative_child.data == 'influenza'
    assert tree4.root.positive_child.positive_child is None
    assert tree4.root.positive_child.negative_child is None
    assert tree4.root.negative_child.positive_child is None
    assert tree4.root.negative_child.negative_child is None


#								  Tree 5
#                cough								  cough
#          Yes /       \ No				  		Yes /       \ No
#        fever           healthy       --> 		cold       healthy
#   Yes /     \ No    Yes/      \ No					Yes/      \ No
#    cold   cold       None       flu					None       flu

flu = Node('flu')
none_leaf2 = Node(None)
flu_leaf = Node("cold", None, None)
cold_leaf = Node("cold", None, None)
inner_vertex = Node("fever", flu_leaf, cold_leaf)
healthy_leaf = Node("healthy", none_leaf2, flu)
root = Node("cough", inner_vertex, healthy_leaf)

tree5 = Diagnoser(root)


def test_minimize5():
    tree5.minimize()
    assert tree5.root.data == 'cough'
    assert tree5.root.negative_child.data == 'healthy'
    assert tree5.root.negative_child.positive_child.data is None
    assert tree5.root.negative_child.negative_child.data == 'flu'
    assert tree5.root.positive_child.positive_child is None
    assert tree5.root.positive_child.data == 'cold'


# 								Tree 6
#                          cough					influenza
#                    Yes /       \ No
#                  fever        influenza  -->
#             Yes /     \ No
#            headache   None
#       Yes /     \ No
# influenza     influenza

flu_leaf4 = Node("influenza", None, None)
cold_leaf4 = Node(None, None, None)
hard_leaf4 = Node("influenza", None, None)
headache_node4 = Node("headache", hard_leaf4, flu_leaf4)
inner_vertex4 = Node("fever", headache_node4, cold_leaf4)
healthy_leaf4 = Node("influenza", None, None)
root6 = Node("cough", inner_vertex4, healthy_leaf4)

tree6 = Diagnoser(root6)


def test_remove_empty1():
    tree6.minimize(True)
    assert tree6.root.data == 'influenza'
    assert tree6.root.positive_child is None
    assert tree6.root.negative_child is None


#									Tree 7
#                cough  				 		  cough
#          Yes /       \ No 				Yes /       \ No
#        fever           healthy  -->		head	   healthy
#   Yes /     \ No
# 	None      head

pos_pos7 = Node(None, None, None)
pos_neg7 = Node("head", None, None)

pos7 = Node("fever", pos_pos7, pos_neg7)
neg7 = Node("healthy", None, None)

root7 = Node("cough", pos7, neg7)
tree7 = Diagnoser(root7)


def test_remove_empty2():
    tree7.minimize(True)
    assert tree7.root.data == 'cough'
    assert tree7.root.positive_child.data == 'head'
    assert tree7.root.negative_child.data == 'healthy'
    assert tree7.root.positive_child.negative_child is None
    assert tree7.root.positive_child.positive_child is None
