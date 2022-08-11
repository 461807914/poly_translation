import islpy as isl

aff = isl.MultiAff("{ A[x , y, z ] -> [x * 100 + y * 10 + z, y * 100 + x * 10 + z, z * 100 + y * 10 + x] }")
# { A[x, y, z] -> [(100x + 10y + z), (10x + 100y + z), (x + 10y + 100z)] }
# 该表示形式对应 n[e_0, e_1, ..., e_{d-1}]
# d个表达式拥有共同的domain space，统一写成 [x, y, z]，不同的range 统一放在一个range space当中
print (aff) 



aff = isl.MultiAff("{ S[i, j] -> A[a[i + 1, j - 1] -> [i, j, i + j]] }")

# 也可以把A去掉
aff2 = isl.MultiAff("{ S[i, j] -> [a[i + 1, j - 1] -> [i, j, i + j]] }")
# { S[i, j] -> A[a[(1 + i), (-1 + j)] -> [(i), (j), (i + j)]] }
# 该表示形式对应 n[e -> f]
# 从例子里面来看e 和 f 应该是有相同的domain space， 这里是指S[i, j]
# range space中的表达式应该对应e和f的range space可以有多个

print(aff)