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
---
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

在`isl`中，拟仿射表达式的元组的写法与Notation 4.2中的拟仿射表达式的写法相同，除了中括号中的拟仿射表达式被推广为结构化命名整数元组模板，输入结构化命名整数元组模板中的变量中变量由拟仿射表达式替换。

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

该构造函数可以再次用于生成新类型。

### Definition 4.11 (Piecewise Quasi-Affine Expression)

一个分段拟仿射表达式的结果是将Definition 4.10施加到拟仿射表达式上。
在`isl`中，一个分段拟仿射表达式表示为`isl_pw_aff`。

### Notation 4.12 (Piecewise Quasi-Affine Expression)

在`isl`中，分段拟仿射表达式写作一个带有条件的拟仿射表达式序列，这些表达式使用分号分隔并且用一个大括号包围。
每个带有条件的拟仿射表达式包含了Notation 4.2中的解释的分段拟仿射表达式$E_i$（没有大括号）,并且用一个冒号来约束表示的空间$S_i$。

### Example 4.13 

一个分段拟仿射表达式的例子。
$\{f[x] != [x + 1] : 0 ≤ x < n - 1; [x] != [0] : x = n - 1 \}$


### Definition 4.14 (Piecewise Tuple of Quasi-Affine Expressions)

一个拟仿射表达式的分段元组就是将definition 4.10应用到拟仿射表达式上。在`isl`中，一个拟仿射表达式的分段元组表示为`isl_pw_multi_aff`

### Alternative 4.15 (Quasts)

*这单词啥意思？从下的定义来看，好像是个数据结构？*

准仿射选择树（quasi-affine selection tree），也称为 quast，形成了准仿射表达式的分段元组的替代表示。准仿射节树是具有作为叶子的准仿射表达式或$\bot$ 元组和作为内部节点的准仿射表达式的树。每个内部节点都有两个子节点，如果节点中的准仿射表达式是非负的，则表示为第一个孩子，如果表达式为负，则应表示为另外一个孩子节点。准仿射节树的值是在评估输入的内部节点时达到的准仿射表达式元组的值。如果该过程在$\bot$处种植，那么该值是未定义的。

*reach-def 分析？没太看明白这部分的表述*

### Notation 4.16 (Piecewise Tuple of Quasi-Affine Expressions)

在`isl`中，一个拟仿射表达式的分段元组表示成一个带有条件的拟仿射表达式元素序列，使用分号分隔并用大括号包围。每个拟仿射表达式的条件元组由Notation 4.6组成（不带大括号），对于每个拟仿射表达式$E_i$的元组，后面跟着一个冒号以及一个约束条件$S_i$。

每个分段表达式都由一个给定的作用域空间和一个范围空间。以下构造函数允许它们在多个空间中组合。

### Definition 4.17 （Multi-Space Expression)

多空间表达式将具有不同域和/或范围空间的分段表达式组合成一个表达式。多空间表达式没有特定的域或范围空间，即使所有组成分段表达式碰巧具有相同的域或范围空间。多空间表达式的域是组合分段表达式的域的并集。整数元组 x 处的多空间表达式的值是 x 处的分段表达式的值，该表达式在其域中包含 x，如果有的话。

### Definition 4.18 (Multi-Space Piecewise Quasi-Affine Expression)

一个多空间分段拟仿射表达式是将Definition 4.17应用于分段拟仿射表达式的结果。

在`isl`中，多空间分段拟仿射表达式的表示为`isl_union_pw_aff`


### Definitino 4.19 (Multi-Space Piecewise Quasi-Affine Expression)

多空间分段拟仿射表达式的编写方式与分段拟仿射表达式相同（参Notation 4.12）。 唯一的区别是域可能有不同的空间。

### Definition 4.20 (Multi-Space Piecewise Tuple of Quasi-Affine Expressions)

拟仿射表达式的多空间分段元组是将Definition 4.17 应用于准仿射表达式的分段元组的结果。

在`isl`中拟仿射表达式的多空间分段元组表示为`isl_union_pw_multi_aff`。

### Notation 4.21 (Multi-Space Piecewise Tuple of Quasi-Affine Expressions)

一个拟仿射表达式的多空间分段元组的表示方法与拟仿射表达式的分段元组相同（见Notation 4.16）。唯一的不同域和元组可能有不同的空间。

元组也可以通过分段表达式或者多空间表达式构造。

### Definition 4.22 (Tuple of Piecewise Quasi-Affine Expressions)

一个分段拟仿射表达式元组即将definition 4.4应用到分段拟仿射表达式上。

在`isl`中，一个分段拟仿射表达式元组的表示方法为`isl_multi_pw_aff`。

### Notation 4.23 (Tuple of Piecewise Quasi-Affine Expressions)

在`isl`中，分段拟仿射表达式元组的编写方式与Notation 4.6 中的拟仿射表达式元组相同，除了每个拟仿射表达式可以用分号分隔的拟仿射表达式，冒号和相应集合的约束。每个这样的序列都需要用括号括起来，以防止用于分隔序列的逗号被视为约束内的分隔表达式。

尽管拟仿射表达式的分段元组和分段拟仿射表达式的元组非常相似，但它们的处理方式略有不同，因为第一个是分段表达式，而第二个是元组。
两个表达式的类型可以表达的内容也有所不同。在一个分段拟仿射表达式元组当中，每个元素是一个分段拟仿射表达式，而且可以在域空间的不同部分中不去定义。

在拟仿射表达式的分段元组当中，整个元组在域空间中的任何特定点要么是定义的，要么是未定义的。

---
*这里注意区分两个概念*

一个是分段拟仿射表达式元组（tuple of piecewise quasi-affine expressions），另一个是拟仿射表达式的分段元组（piecewise tuple of quasi-affine expressions）。

### Example 4.24

下面的分段拟仿射表达式元组**不能**被表示成一个拟仿射表达式的分段元组。

$\{[i] \rightarrow [(i : i ≥ 0); (i - 1 : i ≥ 1)] \}$

第一个分段拟仿射表达式有域$\{[i] : i ≥ 0 \}$，但是第二个的域是$\{[i] : i ≥ 1\}$

### Example 4.25
下面代码将拟仿射表达式的分段元组转换成一个分段拟仿射表达式元组，而且不会有信息损失。

```python
import isl
a = isl.pw_multi_aff( " { [ i ] -> [i , i - 1] : i - 1 >= 0 } " ) # 拟仿射表达式分段元组
print a
a = isl.multi_pw_aff( a ) # 分段拟仿射表达式元组
print a
```

结果为

```python
{ [ i ] -> [( i ) , ( -1 + i ) ] : i > 0 }
{ [ i ] -> [(( i ) : i > 0) , (( -1 + i ) : i > 0) ] }
```

### Definition 4.26 (Tuple of Multi-Space Piecewise Quasi-Affine Expressions)
在`isl`中一个多空间分段拟仿射表达式元组通过Notation 4.21中的多空间分段拟仿射表达式符号，写成一个带有参数的结构化命名整数元组模板，其常量符号在结构化命名整数元组模板的外侧。

### Example 4.28
下面的代码展示一个多空间分段拟仿射表达式元组。

```python
import isl
a = isl.multi_union_pw_aff(" [ n ] -> A [{ S1 [] -> [ n ]; S2 [i , j ] -> [ i ] } , "
                           " { S1 [] -> [0]; S2 [i , j ] -> [ j ] }] " )
print a
```

输出结果为

```python
[ n ] -> A [{ S2 [i , j ] -> [( i ) ]; S1 [] -> [( n ) ] } , { S2 [i , j ] -> [( j ) ]; S1 [] -> [(0) ] }]
```

---
从API使用的角度，总结一下上面的内容，并添加几个例子
关于仿射表达式的形式一共出现了如下几种：

- `isl_aff`
- `isl_multi_aff`
- `isl_pw_aff`
- `isl_pw_multi_aff`
- `isl_union_pw_aff`
- `isl_union_pw_multi_aff`
- `isl_multi_pw_aff`

在概念上，有如下几种：
- 拟仿射表达式(Quasi-Affine Expression), 对应的API为 `isl_aff`
- 拟仿射表达式元组(Tuple of Quasi-Affine Expressions)，对应的API为 `isl_multi_aff`
- 分段拟仿射表达式(Piecewise Quasi-Affine Expression)，对应的API为 `isl_pw_aff`
- 拟仿射表达式的分段元组(Piecewise Tuple of Quasi-Affine Expressions)，对应的API为 `isl_pw_multi_aff`
- 多空间分段拟仿射表达式(Multi-Space Piecewise Quasi-Affine Expression)，对应的API为 `isl_union_pw_aff`
- 拟仿射表达式的多空间分段元组(Multi-Space Piecewise Tuple of Quasi-Affine Expressions)，对应的API为 `isl_union_pw_multi_aff`
- 分段拟仿射表达式元组(Tuple of Piecewise Quasi-Affine Expressions)，对应的API为 `isl_multi_pw_aff`

`isl_aff` 表示一个映射，映射的"key"是一个整数元组，范围称为 domain space，维数可以是多维; 映射的"value"是一个一维的整数元组（就是元组里面只有一个维度），范围称为range space，维数固定为1。

拟仿射表达式的元组需要用到定义4.4 关于表达式元组的描述，顾名思义，表达式元组就是有一个元组，里面有很多个表达式，按照定义中的要求，元组中的所有表达式的domain space需要相同。形式有两种：

第一种是$n[e_0, e_1,...,e_{d-1}]$，表示元组的名称为n，有d个相同domain space 的表达式。

第二种是$n[e \rightarrow f]$, 同样n表示元组的名称，e和f分别是两个表达式元组。 （个人理解，e和f如果是表达式元组，那么可以是第一种形式，也可以是第二种形式。另外，该模式的元组要求e和f有相同的domain space)

在定义4.8当中还专门描述了表达式元组的空间，同样有两种形式，第一种是描述元组中的表达式个数，即n/d

第二种是是在映射形式下，e和f的空间，即(n, S(f), S(e))

并且说明了在`isl_multi_aff`API中，元组的空间就是

关于`isl_multi_aff`的demo 可以看python的对应代码文件


定义4.9和定义4.10中介绍了表达式向量和分段表达式的概念，这里**注意表达式向量和表达式元组的区别**,表达式向量由表达式元组转化而来，因此，表达式向量中的元素包含表达式元组中domain space都相同的性质。

表达式向量有两种形式，从定义的描述中看，**可以将表达式元组转换成表达式向量**，第一种形式为如果有一种表达式元组我$n[e_0, e_1,...,e_{d-1}]$，那么转换成表达式向量后的形式为$(e_0, e_1,..., e_{d-1})$

如果是第二种形式的表达式元组，即$n[f \rightarrow g]$，那么转换成表达式向量后，表示为$\Epsilon (f) || \Epsilon (g)$，其中$\Epsilon (e)$表示将表达式元组e转换成表达式向量，符号$||$表示concatenation两个向量的操作。

定义4.11 描述了分段拟仿射表达式，即将定义4.10添加到拟仿射表达式上。定义4.10描述的是分段表达式，一个分段表达式里面有n个元素对，每个元素对由一个集合S和一个表达式E组成，且有5个约束条件：
1. S和E的domain space要相同
2. 所有$E_i$的范围空间(range space)要相同
3. $S_i$与$S_j$不相交（这里i != j)
4. 最后的分段表达式的domain space与range space与$E_i$相同 （注意是space）
5. 分段表达式的domain是$S_i$的并集

对应的API是`isl_pw_aff`，在符号表示上将Notation 4.12。

定义4.14定义了拟仿射表达式分段元组，即将分段表达式的概念应用到拟仿射表达式元组。

在符号表示上，拟仿射表达式分段元组中包含一堆带有条件的拟仿射表表达式元组，用分号分隔，每个带条件的拟仿射表达式元组的形式都和Notation 4.6一样。API使用`isl_pw_multi_aff`