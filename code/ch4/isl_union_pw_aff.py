import islpy as isl

aff = isl.UnionPwAff("{A[x , y, z] -> [[y + 1], [x, y]]}")

print(aff)