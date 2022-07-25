import islpy as isl

def print_set (s):
    print (s)
s = isl.UnionSet( " { C[6, 2]; B[2 ,8 ,1]; B[2, 8, 1]} ")

res = s.foreach_set(print_set)

