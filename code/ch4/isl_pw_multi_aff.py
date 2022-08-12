import islpy as isl

# { A[x, y, z] -> [(3 + 2y), (3 + 2x), (6 + 2z)] }
aff = isl.PwMultiAff("{A[x , y, z ] -> [y + 1, x + 2, z + 3]; A[x , y, z ] -> [y + 2, x + 1, z + 3]}")

print(aff)