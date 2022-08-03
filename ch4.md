# Piecewise Quasi-Affine Expressions

虽然 Presburger 关系完全能够将函数表示为特殊情况，但有时处理函数的显式表示会更方便。 本章的分段拟仿射表达式(piecewise quasi-affine expressions）可以表示与可以表示为 Presburger 关系的函数相同的函数。

## 4.1 Quasi-Affine Expressions

### Definition 4.1 (Quasi-Affine Expression)

拟仿射表达式f是将具有给定空间（space）S的命名整数元素映射到有理数的函数，该函数被指定为元组变量中的Presburger 项（term），并且可选的除以整数常量。空间S称为函数f的域空间（domain space）写作$S^{dom}f$。
拟仿射表达式的域（domain）为所有空间为S的元素的集合。

作为一个特例，拟仿射表达式同样也可以是一个（符号化）的常量表达式，该情形下没有与空间，写作$S^{dom}f = \bot$，并且域是一个单元集合（unit set）。

这样的表达式称为拟仿射是因为它引入了整数除法。在`isl`当中，拟仿射表达式表示为`isl_aff`。一个`isl_aff`的域空间是它输入的整数元组的空间。`isl_aff`的范围空间（range space）是一个固定的匿名一维空间。在拟仿射表达式是一个常量表达式的情况下，它没有输入元组，`isl_aff`的空间是一个匿名一维空间。

---
补充一个`isl_aff`的例子
```python
import islpy as isl
aff = isl.Aff("{ A[x , y, z ] -> B[(2 * x + 4 * ( y / 2 ) ) / 3] }")
print (aff)
```
输出
```python
{ A[x, y, z] -> [(2x + 2y)/3] }
```
根据上面的定义，aff的输入是一个命名的整数元组，输出是一个匿名的一维空间，所以标识符B没了



### Notation 4.2 (Quasi-Affine Expression)

在`isl`当中，一个拟仿射表达式写作一个结构化命名整数元素模板（structured named integer tuple template），后面跟着一个`->`符号，并且结构化命名整数元组模板的变量中的拟仿射表达式用中括号括起来，整个表达式用大括号括起来。

如果拟仿射表达式没有域空间，结构化整数元组模板以及`->`符号会被省略。如果有常量符号被引入，那么需要想Notation 3.22中形式一样被声明。

作为集合与二元关系的例子，拟仿射表达式的打印方法可能会与用户描述的原始形式存在区别。

### Example 4.3

```python
import isl
a = isl.aff ( " { [x , y ] -> [ floor ((2* x +4* floor ( y /2))/3)] } " )
print a
```

输出为：

```python
{ [x , y ] -> [( x + floor (( y ) /2) + floor (( -2 x + y ) /6) ) ] }
```

显然，纯拟仿射表达式不足以表示任何可能的单值 Presburger 关系。相反，需要以结构化的方式组合几个这样的表达式。特别是，将以下类型构造函数应用于准仿射表达式的类型以获得更具表现力的类型：元组构造函数将多个表达式组合成一个元组； 一个分段构造函数，用于组合在空间的不相交部分上定义的多个表达式； 和一个联合构造函数，用于组合在不同空间上定义的多个表达式。

### Definition 4.4 (Tuple of Expressions)

表达式元组将零个或多个相同类型且具有相同域空间（或无域空间）的基本表达式组合成一个共享该域空间并具有规定范围空间的多维表达式。其表达方式为如下两种之一：

- 标识符n以及$d ≥ 0$的基本表达式$e_j$，且$0 ≤ j ≤ d$，写作$n[e_0, e_1,...,e_{d-1}]$
- 标识符n以及表达式e和f的两个元组，写作$n[e \rightarrow f]$

一个或多个表达式的元组的域是这些表达式的域的交集。一个元组中如果的表达式的数量是0，那么它的域是未定义的。

特别地，准仿射表达式的元组是从准仿射表达式构造元组表达式的结果。

### Definition 4.5 (Tuple of Quasi-Affine Expressions)

拟仿射表达式的元组是将Definition 4.4 施加到一个拟仿射表达式上，即表达式替换成拟仿射表达式。在`isl`中,拟仿射表达式元组表示为`isl_multi_aff`。

### Notation 4.6 (Tuple of Quasi-Affine Expressions)

在`isl`中，拟仿射表达式的元组的写法与Notation 4.2中的拟仿射表达式的写法相同，除了中括号中的拟仿射表达式被推广位结构化命名整数元组模板，输入结构化命名整数元组模板中的变量中变量由拟仿射表达式替换。

### Example 4.7

一个拟仿射表达式的元组
```python
import islpy as isl

aff = isl.MultiAff("{ S[i, j] -> A_x[A[i + 1, j - 1] -> x[]] }")

print (aff)
```


---
即范围中的元素可以是嵌套的表达式

再来来个例子，可以看到MultiAff当中的范围空间的元素可以是多维度，但是Aff则不行（在原始文档中没有说明）

```python
import islpy as isl
aff = isl.MultiAff("{ A[x , y, z ] -> [x * 100 + y * 10 + z, y * 100 + x * 10 + z, z * 100 + y * 10 + x] }")
print (aff)
```

### Definition 4.8 ((Space of a Tuple of Expressions)

一个表达式元组$e$的空间$Se$可能为如下两种情况之一
- n/d，如果$e$的形式是$n[e_0, e_1,..., e_{d_1}]$, n为标识符并且d为一个非负整数。
- (n, S(f), S(g)), 如果$e$的形式是$n[f \rightarrow g]$, n为标识符，且f和g是表达式元组

在`isl`中，拟仿射表达式的空间是`isl_multi_aff`的范维空间（range space）

### Definition 4.9 （Expression Vector）

表达式元组$e$的表达式向量$\Epsilon e$形式，是一个使用向量表示的方法，存在如下两种形式：
- $(e_0, e_1,...,e_{d-1})，如果$e$的形式是$n[e_0, e_1,...,e_{d-1}]$，其中n是标识符，并且d是一个非负整数
- $\Epsilon (f)|| \Epsilon (g)$, 其中$||$符号表示将两个向量连接起来（concatenation），如果$e$的形式是$n[f \rightarrow g]$，其中n是标识符，并且f和g分别是表达式元组。

### Definition 4.10 (Piecewise Expression)

一个分段表达式包含了n对（n≥0）固定空间（fixed-space）的集合$S_i$和基础表达式（base expression）$E_i$，并把它们放到一个表达式当中。
$S_i$的空间和$E_i$的域空间（domain space）需要相同。同样，所有$E_i$的范围空间（range space）也要相同。此外，$S_i$需要成对不相交（pairwise disjoint）。
分段表达式的域空间和范围空间与$E_i$相同。分段表达式的域空间是$S_i$的域空间的并集。分段表达式在一个整数元组$x$中的值是某些i对应的$E_i(x) \ if x \in S_i$
否则，值属于未定义。