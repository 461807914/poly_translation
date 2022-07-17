# Presburger Sets and Relations
在前一章中，通过明确列出包含在集合或二元关系中的（成对的）元素，对集合和二元关系进行了扩展描述。 本章解释了如何通过元素（对）需要满足的属性来内涵地描述集合和二元关系。 和前一章一样，集合和关系将继续被纯粹抽象地处理。

## 3.1 Intensional Descriptions
在内涵描述(internsional descriptions)中，集合的元素是根据结构化的命名整数元组模板(structured named integer tuple templates)来描述的。 这些本质上与结构化命名整数元组( structured named integer tuples)相同，只是整数已被变量替换。 将以下定义与第 28 页的定义 2.66、第 29 页的定义 2.68 和第 29 页的定义 2.70 进行比较。

### Definition 3.1 (Structured Named Integer Tuple Template)
一个结构化命名整数元组模板可能为如下两种情况之一：
1. 一个标识符n，以及变量$i_j$满足$0≤j<d$且$d≥0$，记为$n[i_0, i_1,...,i_{d-1}]$
2. 一个标识符n有两个结构化命名整数元组模板$i$和$j$，写为$n[i->j]$

### Definition 3.2 (space)
一个结构化命名整数元组模板$i$的空间$Si$有可能为如下两种情况之一：
1. n/d，如果$i$的形式为$n[i_0, i_1, i_2,...,i_{d-1}]$，n为一个标识符，d是一个非负整数。
2. (n, S(j), S(k))，如果i的形式是$n[j->k]$，且n是一个标识符，并且j和k是结构化命名整数元组模板.

结构化命名整数元组模板对$i->j$的空间表示为:$(S(i), S(j))$

### Definition 3.3 (Variable Vector)
变量向量$Vi$的结构化命名整数元组模板$i$是一个向量，有如下两种形式：
1. (i_0, i_1,...,i_{d-1}),如果$i$的形式是$n[i_0, i_1,...,i_{d-1}]$，其中n是标识符，并且d是一个非负整数
2. $V(j) || V(k)$，其中$||$表示concat两个向量，这里要求$i$的形式是$n[j->k]$，其中n是一个标识符，并且$j$和$k$是结构化命名整数元组模板。

一对结构化命名整数元组模板$i->j$的变量向量的形式是$V(i)||V(j)$。

现在根据上面的模板形式重新定义集合与二元关系。

### Notation 3.4 (Set)
集合的表示法由分号分隔的元素描述列表组成，该列表括在大括号中。 元素描述由一个模板组成，后跟一个冒号和一个根据模板中的变量的公式。*就是描述集合的范围*
在每个公式中，对应元组的变量向量的元素称为集合变量(set variables)。

### Notation 3.5 (Binary Relation)
二元关系的表示法由分号分隔的元素对描述列表形成，该列表括在大括号中。 元素对描述由一对模板组成，由箭头分隔，后跟冒号，以及根据模板对中的变量的公式。
一个整数元组$i$属于一个集合，当且仅当集合描述包含一个元素描述，使得元组模板与$i$具有相同的空间，并且$i$的值向量满足相应的公式。对于二元关系也是如此。公式的确切性质及其满足性（satisfaction)在第 3.2 节 Presburger 公式中进行了描述。


### Example 3.6
集合${B[i]:5 ≤ i ≤ 6; C[]:}$和与在第二章的集合命名整数元组的形式${B[5]; B[6]; C[]}等价$

## 3.2 Presburger Formulas
Presburger 公式是一阶公式概念的特定实例。 首先定义这个一般概念。

### Definition 3.7 (Language)
一个语言(language)的描述公式为:$L = {f_1/r_1, f_2/r_2,..., P_1/s_1, P_2/s_2,...}$
即，由函数符号$f_i$和谓词符号(predicate symbols)$P_i$组成的集合，其中$f_i$和$P_i$都带有一个属性元(arity)$r_i$或$s_i$，比如这些属性元表示$f_i$或$P_i$需要的参数。
一个函数带有0个属性元称之为常量。

### Definition 3.8 (Term)
在一个语言$L$中一个项(term)的表示有如下两种之一：
1. v, 一个变量v
2. $f_i(t_1,...,t_{ri})$，$L$中一个函数符号$f_i$，带有一个属性元$r_i$和$t_j$项，其中$1 ≤ j ≤ r_i$。特别的，如果$r_i=0$，那么$f_i()$就是一个项。

### Definition 3.9 (First Order Formula)
在一个语言$L$中一阶公式可以归纳为如下之一：
1. true （就是布尔量）
2. $P_i(t_i,...,t_{si})$，其中$P_i$是语言$L$中的一个谓词符号带有属性元$s_i$和项$t_j$，满足$1 ≤ j ≤ s_i$
3. $t_1 = t_2$，其中$t_1$和$t_2$是语言$L$中的项。
4. $F_1 \wedge F_2$，连接两个两个公式(formulas)$F_1$和$F_2$
5. $F_1 \vee F_2$，分离两个两个公式(formulas)$F_1$和$F_2$
6. $\neg F$，对公式$F$取反。
7. $\exists v : F$，公式$F$在变量$v$上存在量化(existential quantification)
8. $\forall v : F$，公式$F$在变量$V$的全称量化

*这里存在量化和全称量化是谓词逻辑(离散数学)中的术语,全称量化即表示一个谓词再所考虑的每一个对象中都为真；存在量化表示一个谓词对所考虑中的一个或多个对象为真。这里的谓词就是函数F*

参考[谓词逻辑](https://www.jianshu.com/p/fb371b50800c)

### Definition 3.10 (Free and Bound Variables)
*翻译成自由变量与绑定变量*
公式$F$中一个变量$v$当F是$\exists v : F_1$或者$\forall v : F_2$的子公式(subformula)并且$v$出现在$F_1$或者$F_2$当中，此时$v$称之为绑定变量。否则称之为自由变量。

### Definition 3.11 (Closed Formula)
*翻译成闭式公式*
当一个公式没有包含任何自由变量的时候，称之为闭式公式。

### Definition 3.12 (Presburger Language)
Presbugrger 语言是带有如下函数符号的一阶语言(first order language),满足如下：
1. +/2
2. -/2
3. 对于每个整数$d$都有一个常量符号$d/0$
4. 对于每个正整数$d$都有一个一元函数符号$\lfloor ·/d \rfloor$
5. 一组符号$c_i/0$的以及一个单个的谓词符号
6. ≤/2

*上面的+/2中，加号表示加法的谓词符号，这里理解成函数，后面的2是属性元，表示有两个参数，可以理解成加法op要有两个操作数组成*

### Definition 3.14 (Presburger Term)
Presburger term 是在Presburger 语言中的项。

### Definition 3.14 (Presburger Formula)
一个Presburger 公式是Presburger语言中的一阶公式

为了能够评估是否满足一阶公式，需要考虑讨论域和所有函数和谓词符号的解释。这里的讨论域（范围）是指公式中变量的一组值。演绎(interpretation)将函数或谓词符号映射到实际函数或谓词。
在Presburger 公式的例子中，讨论域就是整数集合。

*这里的interpretation应该是翻译成逻辑学中的演绎（演绎推理，或者逻辑推断），而不是解释吧*

### Definition 3.15 (Interpretation of Presburger Symbols)
对 Presburger 公式中的函数和谓词符号给出以下演绎。

1. 函数符号$+/2$会被映射到两个整数的加法函数。
2. 函数符号$-/2$会被映射到两个整数的减法函数，第一个数减去第二个。
3. 每个常量符号$d/0$会被映射到对应的整数值。
4. 每个函数符号$\lfloor ·/d \rfloor$会被映射到一个返回以$d$作为除数的整数除法函数结果
5. 谓词符号≤/2会被映射到一个整数集上的小于等于关系。

常数符号 $c_i$ 没有赋予固定的演绎。相反，考虑了所有可能的整数演绎。 Presburger 项的演绎是将演绎递归地应用于该项中出现的函数符号的结果。
以下定义根据讨论域（或范围）和符号的演绎定义了一般一阶公式的真值概念。该定义使用了$F\{v \longmapsto d\}$形式来表达，表示用$d$替换$F$中的每个任意出现的$v$的结果。

### Definition 3.16 (True Value)
在给定的范围和演绎下，第一类公式的真值表达如下：
1. 公式为true，结果就是true
2. 公式为$P_i(t_1,...,t_{si})$为真，如果$P_i$的演绎应用到$t_j$的演绎为真
3. 公式$t_1 = t_2$为真的情况是当$t_1$和$t_2$的演绎结果相同。
4. $F_1 \land F_2$为真，如果$F_1$与$F_2$为真。
5. $F_1 \lor F_2$为真，当$F_1$或者$F_2$为真。
6. $\neg F$ 为真，当$F$不为真时。
7. $\exists v : F(v)$为真，如果在讨论域中存在$d$使得$F\{v \longmapsto d\}$为真
8. $\forall v : F(v)$为真，如果在讨论域中所有$d$使得$F\{v \longmapsto d\}$为真

## 3.3 Presburger Set and Relation

### Definition 3.17 (Presburger Set)
Presburger Set是第42页Notation 3.4符号中的一个集合，其中公式是 Presburger 公式，如前页定义 3.14 中所述。 此公式中唯一允许的自由变量是元组模板的变量。

### Definition 3.18 (Presburger Relation)
Presburger 关系是第 42 页 Notation 3.5 的符号中的二元关系，其中公式是 Presburger 公式，如前一页的定义 3.14 中所述。 此公式中唯一允许的自由变量是一对元组模板的变量。

正如第 3.1 节内涵描述中已经解释的，整数元组$i$属于一个集合，当且仅当集合描述包含元素描述$t : F$使得元组模板具有与$i$相同的空间，即 $Si = St$，并且$i$的值向量满足对应的公式，比如
$F\{Vt \longmapsto Vi\}$为真。

### Example 3.19 
集合的例子
$\{[i]: 0 ≤ i \land i ≤ 10 \land \exists α: i = α + α\}$ 与集合 $\{[0];[2];[4];[6];[8];[10]\}$ 等价

### Exmaple 3.20 
$\{[i] : \forall i : 0 ≤ i \land i ≤ 10 \}$是空集，因为子公式$0 ≤ i \land i ≤ 10$为真的情况只有对部分$i$值有效，而不是所有$i$。这表示公式$\forall i : 0 ≤ i \land i ≤ 10 \}$为假，因此，没有元组变量 i 的值符合该公式。

*把“所有”改成“存在”应就对了*

如果元素描述中的公式包含任何常数符号，则公式的真值可能取决于对这些常数符号的解释。因此，Presburger 集本质上表示一组集合，每个集合代表常数符号的值。


### Example 3.21
考虑如下的 Presburger 集合

$\{S[i] : 0 ≤ i \land i ≤ n\}$
该集合的值依赖于常量符号$n$，该集合对应于如下集合的其中之一。
1. Φ if n ＜ 0
2. $\{S[0]\}$ if n = 0
3. $\{S[0]; S[1]\}$ if n = 1
4. $\{S[0]; S[1]; S[2]\}$ if n = 2
5. ...

表3.1 显示了第 43 页定义 3.9 的一阶逻辑连接词和第 43 页定义 3.12 的 Presburger 符号的 isl 符号，以及将在第 3.4 节语法糖中解释的一些语法糖。

*页码请对照原始pdf*

### Notation 3.22 (Constant Symbols)
在这部分文档当中，常量符号将会以roman 字体出现。在isl中，常量符号成为参数（parameter)。参数和变量的表示方式相同，但是参数需要在集合或者二元关系的描述之前就先声明好。尤其是，所有的参数需要放在一个逗号分隔的列表中，并用括号括起来，并且在集合或二元关系的描述前面加上一个 “$->$”。参数的顺序无关紧要。

### Example 3.23 
考虑例子3.21中的集合。在isl中的表示如下

$[n] -> \{S[i] : 0 ≤ i\ and\ i ≤ n\}$

在一些例子当中，对于一个非空的集合或关系，去判断限定它们的常量符号值会很方便。
这些集合关系可以用单元集合(unit set)来表示，该集合当中不包含任何元组，不过它根据常量符号的值来判断是否为空。
单元集的符号类似于第 42 页的符号 3.4 中的集合，除了它不包含任何元组模板。

![表3.1 isl中的Presburger格式](./3.1.png)

### Notation 3.24 (Unit Set)
单元集合(unit set)由冒号和一个常量公式（依赖于常量符号的公式）组成，并使用括号括起来。

在isl中，单元集合称为参数集合（parameter sets），并且在isl中表示为 isl_set。

### Examples 3.25

Exmample 3.21中的集合非空条件可以描述为$\{ : n ≥ 0\}$
或者在isl中表示如下$[n] -> \{ : n >= 0 \}$

第 2 章命名整数元组集合中定义的大多数操作不受常量符号存在的影响。 该操作简单地统一应用于这些常量符号的所有可能值。 然而，一些操作，特别是比较操作，会受到影响。

### Operation 3.26 (Equality of Sets)
两个集合A和B相等(A = B)，如果它们对于常量符号的每个值都包含相同元素。

### Example 3.27
集合 $\{a[i] : i ≥ 0 \}$与集合$\{a[i] : i ≥ 0 \land n ≥ 0\}$不相同
因为第二个集合当n为负值的时候，集合是空的，而且第一个集合对于所有的n值包含无限多个元素。

在iscc中表示如下：

```python
A :=  [ n ] -> { A [ i ] : i >= 0 };
B := [ n ] -> { A [ i ] : i >= 0 and n >= 0 };
A = B
```

```python
False
```

### Example 3.28
集合 $\{a[i] : 0 ≤ i < n\}$ 与集合 $\{a[i] : 0 ≤ i < m\}$ 不相等，因为常量符号n和m不一定相同。

在iscc中如下：

```python
A := [ n ] -> { A [ i ] : 0 <= i < n };
B := [ m ] -> { A [ i ] : 0 <= i < m };
A = B ;
```

```python
False
```

### Example 3.29

集合$\{ a[n, i] : 0 ≤ i < n \}$与集合$\{ a[m, i] : 0 ≤ i < m \}$相等。因为两个集合包含相同的整数元组。

在iscc中如下：
```python
A := { A [n , i ] : 0 <= i < n };
B := { A [m , i ] : 0 <= i < m };
A = B ;
```
```python
True
```



*这里没明白，为什么3.28不相同，但是3.29相同。前面3.28的常量符号是作为参数出现的，但是在例子3.29当中常量符号没有作为参数出现，这里猜测如果没有出现常量符号参数，那么取值都相同*


### Operation 3.30 (Equality of Binary Relations)

两个二元关系 A 和 B相同（A == B）的条件是对于每个常量符号，它们都包含相同的元素对。

### Operation 3.31 (Emptiness of a Set)

一个集合为空的条件是对于任意的常量符号，它不包含任何元素。

### Example 3.32

如果Example 3.29中的集合A仅对常数n的某些值是空的，而不是所有值。因此集合A不是空集。

在iscc中
```python
[ n ] -> { A [ i ] : i >= 0 and n >= 0 } = { };
```
```python
False
```
*注意":="表示赋值，"="表示判断是否相等*

*这里原文是集合B应该是写错了*

### Operation 3.33 (Emptiness of a Binary Rlation)
如果二元关系不包含任何常量符号值的任何元素对，则该二元关系为空。


### Operation 3.34 (Subset)
集合 A 是集合 B 的子集，$A ⊆ B$，如果对于常数符号的每个值，A 的所有元素都包含在 B 中，即，如果 $A \backslash B = ∅$。

### Example 3.35
iscc输入
```python
A := [ n ] -> { A [ i ] : i >= 0 };
B := [ n ] -> { A [ i ] : i >= 0 and n >= 0 };
B <= A ;
```
```python
True
```
*在iscc中子集的表示是<=*

### Operator 3.36 (Subrelation)
二元关系A是二元关系B的自己，表示为$A \subseteq B$，条件是对于任意的常量符号值，如果所有在A中的元素对都包含在集合B中。如果$A \backslash B = ∅$。

### Operation 3.37 (Strict Subset)
集合A是集合B的严格子集（真子集），即$A \subsetneq B$，如果对于任意常量符号，A中所有的元素都包含在B中，并且B中有部分元素A中没有，$A \backslash B = ∅$并且 $A \neq B$。

### Example 3.38
在iscc中的输入为
```python
A := [ n ] -> { A [ i ] : i >= 0 };
B := [ n ] -> { A [ i ] : i >= 0 and n >= 0 };
B < A ;
```
```python
True
```

### Operation 3.39 (Strict Subrelation)
bla bla

## 3.4 Syntactic Sugar

### Notation 3.46 (False) 
公式为假与$\neg \ true$等价

### Notation 3.47 (Implication)
公式 $a \Rightarrow b$ 与 $\neg a \lor b$

*离散数学 逻辑表达中的“蕴含”关系*

遵循第 42 页的 Notation 3.4 和第 42 页的 Notation 3.5 中的元组模板的公式是可选的。 如果公式缺失，则认为它是正确的。

### Exmaple 3.48
iscc 输入
```python
A := { A [ i ] : true };
B := { A [ i ] };
A = B ;
```
```python
True
```
元组模板中的变量可以被 Presburger 项替换，这些项仅涉及出现在模板中较早位置的变量。

### Notation 3.49 (二元关系rewritten)
设$V = (v_1,..., v_n) = V_t$ 为元组模板的变量 $t$。一个元素的描述$t$的表达方式$v_k = g(v_1,...,v_{k-1} \land f(v))$可以重写为$t \{v_k \mapsto g(v_1,...,v_{k-1}) \}: f(v)$

### Exmaple 3.50
二元关系 $\{S[i] \mapsto S[i+1]\}$ 等价于 $\{S[i] \mapsto S[j] : j = i + 1 \}$

但是请注意，语法 $\{ S[j−1] \mapsto S[j] \}$ 是不允许的，因为表达式 j − 1 包含的变量不是出现在前面位置的变量。

```python
A := { S [ i ] -> S [ i + 1] };
B := { S [ i ] -> S [ j ] : j = i + 1 };
A = B ;
```

```python
True
```

前面一页Notation 3.49 以及其公式中元素的可选的描述内容，都可以看作是第二章集合的命名整数元组的语法特殊形式,因为元组 $N[d]$可以看作元素表述$N[v]: v = d$，表示相同的元素。

### Notation 3.51 
符号 $< / 2$表示整数集合的小于关系，比如公式$a<b$ 等价于$a <= b - 1$.

*< / 2表示小于号是一个二元运算符的意思，前面有提过*

*(TODO) 先掠过几个关系符的描述bla bla*

### Example 3.56
集合$\{S[i,j]: i,j ≥ 0\}$ 等价于 $\{S[i,j]: i ≥ 0 \land j ≥ 0\}$

在iscc中的例子如下：
```python
A := { S [i , j ] : i , j >= 0 };
B := { S [i , j ] : i >= 0 and j >= 0 };
A = B ;
```
输出结果为:
```python
True
```

*（TODO) 略过部分*

### Notation 3.59
一元函数$-/1$表示一个负数整数，即公式$-a$等价于$0-a$

### Notation 3.60
符号$n·e$，其中n是一个非负整数常量，速记为:
$\underbrace{e+e+...+e}_{n\ times}$

其中$dot(·)$可以被省略

Presburger公式中不允许出现左侧时变量或者时常量符号的乘法操作。

### Example 3.61
集合$\{[i] : 0 ≤ i ≤ 10 \land i = 2n\}$ 等价于$\{[2n]\}$，当常量n满足条件$0 ≤ n ≤ 5$时成立，否则集合为空。

### Notation 3.62
公式 $a\ mod\ b$, 其中b和a时非负整数常量，等价于$a - b · \lfloor a/b \rfloor$.

下面的符号内容是用来处理字典序的，首先定义什么是字典序。

### Definition 3.63 (Lexicographic Order)
给定两个长度相同的向量a和b，如果a的字典序小于b的字典序，向量a与向量b中第一个不同的元素pa和pb，有 $pa < pb$。

如果两个向量的长度都是N,那么使用Presburger 公式的表示形式为：

$$
\mathop{\lor}\limits_{i: 1\leq i \leq n}((\mathop{\land}\limits_{j: 1\leq i \leq i} a_j = b_j)\land a_i < b_i)
$$

### Notation 3.64
符号$\prec / 2$表示一个在相同长度的整数序列当中的字典序小于关系。即，$a \prec b$, 这里的a和b为两个长度为n的序列，如果元素中的序列关系满足上面定义的字典序公式。

### Example 3.65
有二元关系如下
$\{S[i_1, i_2] \rightarrow S[j_1, j_2] : i_1, i_2 \prec j_1, j_2\}$
等价于$\{S[i_1, i_2] \rightarrow S[j_1, j_2] : i_1 < i_2 \lor (i_1 = j_1 \land i_2 < j_2 \}$

*根据Notation 3.64上面左边的公式$i_1,i_2$ 是一个序列，在字典序的定义中看做一个向量*

在iscc中的例子如下
```python
A := { S [ i1 , i2 ] -> S [ j1 , j2 ] : i1 , i2 << j1 , j2 };
B := { S [ i1 , i2 ] -> S [ j1 , j2 ] : i1 < j1 or ( i1 = j1 and i2 < j2 ) };
A = B ;
```

```python
True
```
*上面的例子描述两个分别满足其字典序约束的两个二元关系，他们的字典序约束是等价的，那么得到的集合肯定也是等价的*

### Alternative 3.66 (Extended Lexicographic Order)
有一些作者考虑了对字典序的扩展形式，并且定义在不同长度的向量对上。通常将较短的向量与较长的向量的初始元素进行比较。如果一个向量是另一个向量的完全匹配的前缀，这样仍然会出现两个向量如何进行比较的问题。对于这样的问题，要么假设没有这样的比较方法，要么定义一些隐含的顺序。

### Notation 3.67
符号$\preccurlyeq /2$ 表示字典序在一个相同长度序列的整数上的小于或者等于关系。记$a \preccurlyeq b$等价于$a \prec b \lor a = b$

*(TODO) 略过字典序大于和大于等于定义*

## 3.5 Lexicographic Order

前页定义 3.63 的字典顺序是在一对向量上定义的，但这个概念可以扩展到一对集合。 结果是一个二元关系，它包含来自两个集合的元素对，使得第一个在字典上小于第二个。 由于仅按字典顺序比较具有相同空间（space）的两个元素才有意义，这尤其意味着结果中的元素对具有相同的空间。

### Operation 3.70 (Lexicographically-smaller-than Relation on Sets)
字典序在两个集合A和B之间的小于关系$A \prec B$表示为一个包含元素对的二元关系, 其中一个元素来自于A另外一个来自于B，两个元素都有相同的空间并且第一个元素的字典序小于第二个。即

$A \prec B \{a \rightarrow b: a \in A \land b \in B \land Sa = Sb \land Va \prec Vb \}$

在isl中，这个操作写作`isl_union_set_lex_lt_union_set`。在iscc中，这个操作写作`<<`。

*Sa表示a所在的空间, Va表示值向量 见Definition 2.68和2.70*

### Operation 3.71 (Lexicographically-smaller-than-or-equal Relation on Sets)
字典序在两个集合A和B上的小于等于$A \preccurlyeq B$ 是一个包含元素对的二元关系，一个元素来自于A，领一个元素来自B，两个元素来自相同的空间，并且第一个元素字典序小于或等于第二个元素。  $A \preccurlyeq B = \{ a \rightarrow b : a \in A \land b \in B \land Sa = Sb \land Va \preccurlyeq Vb\}$

*（TODO) 字典序大于和大于等于的先略过*

### Example 3.74 
下面描述不同字典序关系在集合的计算：

$\{ A[i, j] : 0 ≤ i, j < 10; B[]; C[i] : 0 ≤ i < 100 \}$ 并且
$\{ A[i, j] : 0 ≤ i, j < 20; B[] \}$

```python
A := { A [i , j ] : 0 <= i , j < 10; B []; C [ i ] : 0 <= i < 100 };
B := { A [i , j ] : 0 <= i , j < 20; B [] };
A << B ;
A < <= B ;
A >> B ;
A > >= B ;
```
输出
```python
{ A [i , j ] -> A [ i’ , j’] : 0 <= i <= 9 and 0 <= j <= 9 and i’ > i and 0 <= i’ <= 19 and 0 <= j ’ <= 19; A [i , j ] -> A[i , j’] : 0 <= i <= 9 and 0 <= j <= 9 and j’ > j and 0 <= j’ <= 19 }

{ A [i , j ] -> A [ i ’ , j ’] : 0 <= i <= 9 and 0 <= j <= 9 and i’ > i and 0 <= i’ <= 19 and 0 <= j’ <= 19; A [i , j ] -> A[i , j’] : 0 <= i <= 9 and 0 <= j <= 9 and j’ >= j and 0 <= j ’ <= 19; B [] -> B [] }

{ A [i , j ] -> A [ i’ , j’] : 0 <= i <= 9 and 0 <= j <= 9 and 0 <= i’ <= 19 and i’ < i and 0 <= j’ <= 19; A [i , j ] -> A [i , j’] : 0 <= i <= 9 and 0 <= j <= 9 and 0 <= j’ <= 19 and j’ < j }

{ B [] -> B []; A [i , j ] -> A [ i’ , j’] : 0 <= i <= 9 and 0 <= j <= 9 and 0 <= i’ <= 19 and i’ < i and 0 <= j’ <= 19; A [i , j ] -> A [i , j’] : 0 <= i <= 9 and 0 <= j <= 9 and 0 <= j’ <= 19 and j’ <= j }
```

同样的操作也适用于二元关系，但在这种情况下，比较是在输入关系的范围元素（range elements）上执行的，结果收集相应的域元素（domain elements）。

### Operation 3.75 (Lexicographically-smaller-than Relation on Binary Relations)
字典序在两个二元关系A和B的小于等于$A \prec B$, 是一个包含两个元素的二元关系，一个来源于A的域（domain）一个来源于B的域（domain），它们有相同的元素范围（range），使第一个元素在字典序上小于第二个。即：

$A \prec B = \{a \rightarrow b: \exists c, d : a \rightarrow c \in A \land b \rightarrow d \in B \land Sc = Sd \land Vc \prec Vd \}$

在isl中，这个操作叫做`isl_union_map_lex_lt_union_map`.在iscc中，该操作写为`<<`。

*(TODO) 关系字典序小于等于、大于以及大于等于略过*

### Example 3.79
```python
A := { A [i , j ] -> [i ,0 , j ] };
B := { B [i , j ] -> [j ,1 , i ] };
A << B ;
```
iscc输出为
```python
{ A [i , j ] -> B [i’ , j’] : j’ > i ; A [i , j ] -> B [ i’ , i ] }
```