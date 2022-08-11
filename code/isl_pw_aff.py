import islpy as isl

# 注意分号隔开的两个条件表达式的domain space 是相同的
# 两个表达式的范围空间相同 (似乎范围空间只能是1维)
# 对于x和y的限定条件不相交，如果相交了以后表达式就变了（可以试试）
aff = isl.PwAff("{ [x, y] -> [x + y] : 0 <= x < 10 and 0 <= y < 3; [a, y] -> [a - y] : a = 10 and y = 3 }")

# { [x, y] : 0 <= x <= 9 and 0 <= y <= 2; [x = 10, y = 3] }
# 可以见domain与 表达式相同
print (aff.domain())

print(aff)
