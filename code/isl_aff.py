import islpy as isl

aff = isl.MultiAff("{ S[i, j] -> A_x[A[i + 1, j - 1] -> x[]] }")

print (aff)