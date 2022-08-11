import islpy as isl
aff = isl.Aff("{ A[x , y, z ] -> B[(2 * x + 4 * ( y / 2 ) ) / 3] }")
print (aff)

aff = isl.Aff("{ A[x , y, z ] -> [1 + 2] }")
print (aff) #  A[x, y, z] -> [(3)]
