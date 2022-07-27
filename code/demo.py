import islpy as isl

s = isl.UnionSet( " { C[6, 2]; B[2 ,8 ,1]; B[3, 1, 8]} ")

res = s.lexmax()

print(res)