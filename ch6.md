## 6.1 Dependence Analysis

从访问关系和调度中来计算依赖关系十分中容易。我们以**写后读**依赖关系为例子。设$W$为may-write访问关系，设$R$为may-read访问关系。首先，要计算语句实例对，一个执行写入操作，一个执行读取操作，两个操作可能会访问相同的数据元素。

---
may-write的映射表示形式见第五章中access relation，是语句到变量的映射（与依赖中语句到语句的映射区分开）

上面的$R^{-1} \circ W$就是写后读的计算，例如may-read和may-write的表达式为:

```python
for i in range (10):
    A[i] = i        # S
    B[i] = A[i] + 1 # T

```
那么may-read关系为，${T[] -> A[]}$ may-write关系为${S[] -> A[]; T[] -> B[]}$
执行上面的写后读的运算后应该为$S[] -> T[]$

---
最后，只有哪些按照实例先后顺序执行语句实例对应该被保留。即，语句实例对需要必须是定义在输入调度中的成员。换句话说，$R^{-1} \circ W$需要与顺序关系进行交集运算。

$(R^{-1} \circ W)\  \cap <_S$

**读后写**依赖关系的计算和**写后写**依赖关系的计算方式类似，分别为:

$(W^{-1} \circ R)\  \cap <_S$

$(W^{-1} \circ W)\  \cap <_S$

上面表达式中对于依赖关系的直接计算需要先使用调度S中计算得到的执行顺序关系$<_S$。顺序关系可以很容易的从调度的Presburger关系中计算得到，因为它是调度中域元素对之间的关系，因此相应的范围（range）元素按照字典序排列。执行顺序的关系就是调度S与其本身之间的字典序小于关系。即如下为S的Presburger关系的调度表示。记，作为在调度的定义与表示章节中5.6.1部分解释的那样，对顺序关系计算的显示计算会产生一个二次方数量级的语句数量的数据结构。这个计算可以通过使用在section 6.3近似数据流分析的方式方式来进行优化。

$<_S = S \preccurlyeq S$

---
直接使用上面的方式计算$<_S$会得到的次幂数量级数量的语句实例，这很耗时，这里会使用下面6.3节中的近似数据流分析进行优化一波

在iscc当中，composition操作写作before或者'.'，详见第二章operation 2.32
---

### Example 6.1
考虑代码清单6.1中的内容，该大妈的完整的部分在代码列表5.16当中。如下描述了首先计算对应的顺序关系以及生成的依赖关系。依赖关系的结果如example 5.34所示，专用于执行相关访问的一组实例。

```python
P := parse_file " demo / false .c";
Write := P [2];
Read := P [3];
Schedule := map(P [4]);
Order := Schedule << Schedule ;
print " Order relation :";
print Order ;
print "Read -after - write dependence relation :";
( Write . Read ^-1) * Order ;
print "Write -after - read dependence relation :";

( Read . Write ^-1) * Order ;
print "Write -after - write dependence relation :";
( Write . Write ^-1) * Order ;
```
输出

```python
" Order relation :"
[n] -> { S[i] -> T[i'] : i' > i; S[i] -> T[i]; T[i] -> S[i'] : i' > i; S[i] -> S[i'] : i' > i; T[i] -> T[i'] : i' > i }
"Read -after - write dependence relation :"
[n] -> { S[i] -> T[i'] : 0 <= i < n and i' > i and 0 <= i' < n; S[i] -> T[i] : 0 <= i < n }
"Write -after - read dependence relation :"
[n] -> { T[i] -> S[i'] : 0 <= i < n and i' > i and 0 <= i' < n }
"Write -after - write dependence relation :"
[n] -> { S[i] -> S[i'] : 0 <= i < n and i' > i and 0 <= i' < n }

```

---
在iscc上平台上有一个更详细的例子，如下:

输入为
```python
### Example code (analysed by pet)
# void polynomial_product(int n, int *A, int *B, int *C) {
#     for(int k = 0; k < 2*n-1; k++)
# S:      C[k] = 0;
#     for(int i = 0; i < n; i++)
#         for(int j = 0; j < n; j++)
# T:          C[i+j] += A[i] * B[j];
# }

Domain := [n] -> {
    S[k] : k <= -2 + 2n and k >= 0;
    T[i, j] : i >= 0 and i <= -1 + n and j <= -1 + n and j >= 0;
};

Read := [n] -> {
    T[i, j] -> C[i + j];
    T[i, j] -> B[j];
    T[i, j] -> A[i];
} * Domain;

Write := [n] -> {
    S[k] -> C[k];
    T[i, j] -> C[i + j];
} * Domain;

Schedule := [n] -> {
    T[i, j] -> [1, i, j];
    S[k] -> [0, k, 0];
};

print "Schedule";
print Schedule;

### Happens-Before relation without syntactic sugar
# Lexico := { [i0,i1,i2] -> [o0,o1,o2] : i0 < o0 or i0 = o0 and i1 < o1 or i0 = o0 and i1 = o1 and i2 < o2 };
# Before := Schedule . Lexico . (Schedule^-1)
Before := Schedule << Schedule;

print "Before";
print Before;

#
RaW := (Write . (Read^-1)) * Before;
WaW := (Write . (Write^-1)) * Before;
WaR := (Read . (Write^-1)) * Before;

print "RaW deps";
print RaW;

print "WaW deps";
print WaW;

print "WaR deps";
print WaR;

IslSchedule := schedule Domain respecting (RaW+WaW+WaR) minimizing RaW;
# compute a schedule for the domains in 'Domain' that respects all dependences in '(RaW+WaW+WaR)' and tries to minimize
# the dependences in 'Raw'
# 计算 'Domain' 中的域的调度，该调度依照 '(RaW+WaW+WaR)' 中的所有依赖关系，并尝试最小化 'Raw' 中的依赖关系

IslSchedule := IslSchedule + {}; # flatten the schedule tree

print "IslSchedule";
print IslSchedule;

IslBefore := IslSchedule << IslSchedule;

print "IslBefore";
print IslBefore;

print "Does IslSchedule respects RaW deps?";
print RaW <= IslBefore;

print "Does IslSchedule respects WaW deps?";
print WaW <= IslBefore;

print "Does IslSchedule respects WaR deps?";
print WaR <= IslBefore;

print "Codegen";
codegen (IslSchedule * Domain);
```

输出为:

```python
"Schedule"
[n] -> { S[k] -> [0, k, 0]; T[i, j] -> [1, i, j] }
"Before"
[n] -> { S[k] -> T[i, j]; S[k] -> S[k'] : k' > k; T[i, j] -> T[i', j'] : i' > i; T[i, j] -> T[i, j'] : j' > j }
"RaW deps"
[n] -> { S[k] -> T[i, k - i] : 0 <= k <= -2 + 2n and i >= 0 and -n + k < i <= k and i < n; T[i, j] -> T[i', i + j - i'] : 0 <= i < n and 0 <= j < n and i' > i and i' >= 0 and -n + i + j < i' <= i + j and i' < n }
"WaW deps"
[n] -> { S[k] -> T[i, k - i] : 0 <= k <= -2 + 2n and i >= 0 and -n + k < i <= k and i < n; T[i, j] -> T[i', i + j - i'] : 0 <= i < n and 0 <= j < n and i' > i and i' >= 0 and -n + i + j < i' <= i + j and i' < n }
"WaR deps"
[n] -> { T[i, j] -> T[i', i + j - i'] : 0 <= i < n and 0 <= j < n and i' > i and i' >= 0 and -n + i + j < i' <= i + j and i' < n }
"IslSchedule"
[n] -> { S[k] -> [k, 0, 0]; T[i, j] -> [i + j, i, 1] }
"IslBefore"
[n] -> { S[k] -> T[i, j] : j > k - i; S[k] -> T[i, k - i] : i > 0; S[k] -> T[0, k]; T[i, j] -> S[k] : k > i + j; T[i, j] -> S[i + j] : i < 0; T[i, j] -> T[i', j'] : j' > i + j - i'; T[i, j] -> T[i', i + j - i'] : i' > i; S[k] -> S[k'] : k' > k }
"Does IslSchedule respects RaW deps?"
True
"Does IslSchedule respects WaW deps?"
True
"Does IslSchedule respects WaR deps?"
True
"Codegen"
for (int c0 = 0; c0 < 2 * n - 1; c0 += 1) {
  S(c0);
  for (int c1 = max(0, -n + c0 + 1); c1 <= min(n - 1, c0); c1 += 1)
    T(c1, c0 - c1);
}
```
上面展示了一个完整的优化流程

---


## 6.2 数据流分析
数据流依赖的计算比较复杂。首先假设数据流依赖可以准确计算。这意味着写和读访问时已知的并且可以准确表示。存在数种计算数据流依赖的方法，这些方法的目标主要时为了展示一些在集合与二元关系上的操作，并指出一些不同和可能出现的陷阱。

如section 5.4的依赖关系解释的那样，一个数据流依赖是一个写后读依赖，该依赖没有对同一个内存位置的中间写入操作。一个计算数据流依赖的办法是对一个存在中间写入的操作，去掉写后读依赖。去除掉依赖关系称之为被中间写入杀死（killed）。为了能够将中间写入与正确的写后读依赖相匹配，依赖关系需要跟踪所涉及的内存元素。为此，将语句实例映射到数据元素的读访问关系$R$被其范围投影(range projection) $R_1 = \xrightarrow{ran}R$ 替换，将语句实例和数据元素对映射到数据元素。类似，写访问关系$W$被替换为$W_1 = \xrightarrow{W}$。

只将$R$替换为$R_1$以及将$W$替换为$W_1$不会产生期望的结果，因为$<_S$仍然包含语句实例对，而不是语句实例对和数据元素组成的pair。（原文是:pairs of
pairs of statement instances and data elements.)数据元素可以通过如下公式引入到调度当中。

$S_1 = S \circ (\xrightarrow{dom}(R \cup W)$ (6.8)

---

投影操作可以见第二章2.100和2.102中叫做`isl_union_map_domain_map` 和 `isl_union_map_range_map`

圆圈操作是是组合操作，见第二章2.32在isl中叫做`isl_union_map_apply_range`

---

写后读依赖以及关联的数组元素可以使用如下计算:

$D_1 = (R^{-1}_1 \circ W_1) \cap <_{S_1}$ (ps:写后读)（6.9)

其中$<_S$的计算方式与之前相同。同样，写后写的依赖关系如下。

$O_1 = (W^{-1}_1 \circ W_1) \cap <_{S_1}$ (ps: 写后写)（6.10）

流依赖是将写后读依赖减去写后写依赖于写后读依赖的组合。

$F_1 = D_1 /\ (D_1 \circ O_1)$ (ps: 斜线表示集合减法，详见第二章2.10)

对数组元素的引用可以通过取其域因子从 F1 中删除。

---
上面的$F_1$应该是dataflow 依赖，详见ch5中5.35
flow dependence应该是data flow dependence表示的是一个

---

### Exmaple 6.2
下面的代码展示了代码列表6.1中的数据流依赖关系的计算。计算域因子（domain factor）的最后一步是使用获取压缩关系（zipped relation）的域来执行的。最后得到的数据流依赖关系的结果与exmpale 5.38相同，专门用于执行相关访问的一组实例。

```python
P := parse_file "demo/false.c";
Write := P[2];
Read := P[3];
Schedule := map(P[4]);
Write1 := range_map Write; # operation 2.102 
Read1 := range_map Read;
Schedule1 := ( domain_map ( Read + Write )) . Schedule; # '+' in operation 2.8 is isl_union_set_union 集合的并操作
# Write 为 [n] -> {T[i]->B[i] : 0 <= i < n; S[i] -> t[] : 0 <= i < n}
# Read 为 [n] -> {S[i] -> A[i] : 0 <= i < n; T[i] -> t[] }
# Schedule 为 [n] -> {S[i] -> [0, i] : 0 <= i < n; T[i] -> [1, i] : 0 <= i < n}
Order1 := Schedule1 << Schedule1 ;
RAW := ( Write1 . Read1 ^-1) * Order1 ;
WAW := ( Write1 . Write1 ^-1) * Order1 ;
Flow := RAW - (WAW . RAW );
print " Write access relation :";
print Write1 ;
print " Read access relation :";
print Read1 ;
print " Schedule :";
print Schedule1 ;

print " Order relation :";
print Order1 ;
print "Read -after - write dependence relation :";
print RAW;
print "Write -after - write dependence relation :";
print WAW;
print " Flow dependence relation :";
print Flow ;

# wrap和unwrap操作是将映射和集合互相转换的操作，详见operation 2.72和operation 2.73
# zip 操作为 [i -> m] -> [j -> n] : [i -> j] -> [m -> n] ∈ R
# domain 就是取domain的操作
unwrap ( domain ( zip Flow ));
```
输出为

```python
" Write access relation :"
[n] -> { [T[i] -> B[i]] -> B[i] : 0 <= i < n; [S[i] -> t[]] -> t[] : 0 <= i < n }
" Read access relation :"
[n] -> { [S[i] -> A[i]] -> A[i] : 0 <= i < n; [T[i] -> t[]] -> t[] : 0 <= i < n}
" Schedule :"
[n] -> { [S[i] -> A[i]] -> [i, 0] : 0 <= i < n; [T[i] -> B[i]] -> [i, 1] : 0 <= i < n; [T[i] -> t []] -> [i, 1] : 0 <= i < n; [S[i] -> t[]] -> [i, 0] : 0 <= i < n }
" Order relation :"
[n] -> { [S[i] -> t[]] -> [S[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n; 
         [S[i] -> t[]] -> [S[i'] -> t []] : 0 <= i < n and i' > i and 0 <= i' < n;
         [T[i] -> t[]] -> [S[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [T[i] -> t[]] -> [T[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n; 
         [T[i] -> B[i]] -> [T[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [T[i] -> t []] -> [T[i'] -> t []] : 0 <= i < n and i' > i and 0 <= i' < n; 
         [S[i] -> A[i]] -> [T[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S[i] -> A[i]] -> [T[i] -> t[]] : 0 <= i < n;
         [T[i] -> B[i]] -> [S[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n; 
         [S[i] -> t []] -> [T[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S[i] -> t []] -> [T[i] -> B[i]] : 0 <= i < n; 
         [S[i] -> A[i]] -> [T[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n; 
         [S[i] -> A[i]] -> [T[i] -> B[i]] : 0 <= i < n; 
         [S[i] -> A[i]] -> [S[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [T[i] -> B[i]] -> [T[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S[i] -> t[]] -> [T[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S[i] -> t[]] -> [T[i] -> t[]] : 0 <= i < n; 
         [S[i] -> A[i]] -> [S[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [T[i] -> B[i]] -> [S[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [T[i] -> t[]] -> [S[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n 
        }
"Read -after - write dependence relation :"
[n] -> { [S[i] -> t[]] -> [T[i'] -> t[]] : i >= 0 and i < i' < n; [S[i] -> t []] -> [T[i] -> t []] : 0 <= i < n }

"Write -after - write dependence relation :"
[n] -> { [S[i] -> t[]] -> [S[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n }

" Flow dependence relation :"
[n] -> { [S[i] -> t[]] -> [T[i] -> t[]] : 0 <= i < n }
[n] -> { S[i] -> T[i] : 0 <= i < n }
```

修改 (6.8) 中的调度并使用此修改后的调度定义的顺序的替代方法是使用原始调度定义的顺序并将其应用于 $R^{-1}_1 \circ W_1$ 的正确部分。特别是，（6.9）可以使用

$D_1 = zip((zip(R^{-1}_1 \circ W_1)) \cap {}_{dom} WRAP(<_S))$ (ps: WRAP在原文当中是花体的W，注意这里的调度是S而不是$S_1$)

替换。

（6.10）可以使用如下公式替换

$O_1 = zip((zip(W^{-1}_1 \circ W_1)) \cap {}_{dom} WRAP(<_S))$

### Example 6.3
下面的代码展示另外一种方法来计算$D_1$和$O_1$，并产生相同的结果

```python
P := parse_file "demo/false.c";
Write := P[2];
Read := P[3];
Schedule := map(P[4]);
Write1 := range_map Write ;
Read1 := range_map Read ;
Order := Schedule << Schedule ;
RAW := zip (( zip ( Write1 . Read1 ^-1 )) * wrap ( Order ));
WAW := zip (( zip ( Write1 . Write1 ^-1 )) * wrap ( Order ));
print " Order relation :";
print Order ;
print "Read -after - write dependence relation :";
print RAW;
print "Write -after - write dependence relation :";
print WAW;

```
输出为:

```python
" Order relation :"
[n] -> { S[i] -> T[i'] : i' > i; S[i] -> T[i]; T[i] -> S[i'] : i' > i; S[i] -> S[i'] : i' > i; T[i] -> T[i'] : i' > i }
"Read -after - write dependence relation :"
[n] -> { [S[i] -> t[]] -> [T[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n; [S[i] -> t []] -> [T[i] -> t []] : 0 <= i < n }
"Write -after - write dependence relation :"
[n] -> { [S[i] -> t[]] -> [S[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n }
```

上面所描述的计算数据流依赖的主要问题是不能轻松的处理近似问题（approximations）。特别是，$D_1$在减法运算的两侧时（6.11）。这意味着如果$D_1$是一个过度近似模型，那么结果不能保证是过度近似或近似不足，而大多数实际应用都依赖于这样的保证。

---
这句话的意思是，$D_1$除了包含了真实正确的数据流信息，还包含了很多冗余的信息。详见数据流分析或者软件分析的教材。

---

一个可选的计算数据流依赖的办法是不要视为这些数据流中存在包含中间写入过程的写后读依赖关系，**而是将每次的读取操作与对内存元素最后一次写入操作进行组对**。

此计算的第一步是将每次读取操作与对同一内存元素的**所有先前写入操作**组对，其中$W$为写访问关系，$R$为读访问关系$S$为调度。

$A = (W^{-1} \circ R) \cap (<_S)^{-1}$

为了简化解释过程，假设所有的语句实例都对同一块内存单元进行读或者写操作。否则，需要对相关的数据元素进行跟踪。在得到了所有前面所说的对同一个内存元素进行访问操作的语句实例之后，现在需要计算这些写入语句实例中的最后一个。尤其是那个在计算调度顺序中，字典序最大的那个语句实例（使用Presburger 关系表示）。正在执行写入操作的实例首先会被映射到对应的调度当中，并选出在调度中字典序最大的位置并将该位置映射回写入实例当中。最后得到的结果映射表会将对实例的读取操作映射到实例的写入操作，最后将数据流依赖关系进行取逆操作，即:

$F = (S^{-1} \circ lexmax(S \circ A))^{-1}$

注意，该计算假设所有的计算顺序都是由调度定义的，例如，调度对每个语句实例否赋值了一个不同的位置信息，因此语句实例可以从该位置恢复。在与调度组合之前跟踪写入语句实例的额外副本并没有帮助，因为词典序最大值将被计算为读取和写入语句实例的函数。

### Example 6.4
下面的代码描述了与example 6.2相同的流依赖信息。

```python
P := parse_file "demo/false.c";
Write := P[2];
Read := P[3];
Schedule := map(P[4]);
Order := Schedule << Schedule;
A := ( Read . Write ^-1) * ( Order ^ -1);
F := (( lexmax (A . Schedule )) . Schedule ^-1 )^ -1;
print " Reads mapped to all previous writes :";
print A;
print " Flow dependences :";
print F;
```

---
上面的概念相当重要，要好好理解。

---


## 6.3 近似数据流分析
之前的部分描述了如何执行准确的数据流分析（简单的）。然而，通常访问关系可能不会是准确知道的，因为访问关系的可能依赖于运行时的信息或者可能没有在Presburger关系中表示出来。在这样的例子中，数据流分析只能进行近似估计。通常来说，有两种方法来计算近似数据流。

- 一种方法是操作may或者must访问关系来直接计算数据流。
- 另外一种方法是对运行时信息进行额外的跟踪，得到一个精确但是依赖于运行时信息的数据流依赖关系。一个近似的数据流依赖关系可以通过对所有的运行时依赖信息进行投影操作获得（projecting out），可能在经过一些已知的运行时依赖信息进行简化之后。因为这个方法持续跟踪更多的信息，通常能够计算出更准确的近似估计。本节专注于直接计算近似数据流依。

回想一下基于内存的依赖分析以及基于值的依赖关系分析的主要区别。其区别主要是在基于值的依赖分析中，一个写入操作会杀死所有第一次写入之前的另一个写入和第一次写入之后的读取。本章节中，对近似数据流依赖背后的主要主要思想是仅允许必然写入操作（`must-write`）杀死任何依赖关系。在最糟糕的情况下，所有的可能写入（`may-writes`）都不是必然写入（`must-writes`），并且最后得到的依赖分析与基于内存的依赖分析结果相同。为了不太具体到标准的数据流分析，**所有的操作都是使用may-sources（可能源点）、must-sources（必然源点）以及sinks（汇点）的表示方式，而不使用may-writes、must-writes以及reads的表示方式。** 

---
仔细理解上面的这段话

---

### Operation 6.5(近似数据流分析)
近似数据分析的输入有三个二元关系和一个在二元关系的域上的调度。三个二元关系分别称为汇点（sink）K，可能源点（may-source）Y，以及必然源点T。调度S用于估算以下句子中的谓词“last"，“before”, “after”。(ps: 这三个谓词是什么意思?）对于汇点的每个域(domain）元素`i`与其对应的范围（range）元素`a`，近似数据流分析确定必然源点（`must-source`）的最后一个域（domain）元素`j`，该域元素在`i`之前执行并且也有`a`作为对应的范围（range） 元素。进一步，该分析收集了在`i`之前和`j`之后执行的所有`may-source`的域元素`k`，并且还具有`a`作为对应的范围元素。如果对于一个特定的`i`和`a`这样的组合找不到对应的`j`，那么`after j`条件会被丢弃。换句话说，对于汇点的每个域元素以及每个对应的范围元素，搜集之前执行的共享该范围元素的的`must-source`和`may-source`的域元素，直到找到`must-source`的域元素。所有搜集到的，诸如$j \rightarrow (i \rightarrow a)$以及$k \rightarrow (i \rightarrow a)$的三元组组成了可能依赖关系（may-dependence relation）。$j \rightarrow (i \rightarrow a)$没有中间`k`的子集组成必然依赖关系（`must-dependence` relation）。如果一个汇点没有对应的域元素`j`，那么它的子集可以组成可能无源关系（`may-no-source` relation）。如果一个汇点没有对应的域元素`j`或者`k`，那么它的子集组成必然无源关系（`must-no-source` relation）。

即，may-dependence的关系为

$\{k \rightarrow (i \rightarrow a) : i \rightarrow a \in K \land k \rightarrow a \in (T \cup Y) \land k <_S i \land \neg (\exists j : j \rightarrow a \in T \land k <_S j <_S i)\}$ （6.16）

must-dependence 关系为：

$\{k \rightarrow (i \rightarrow a) : i \rightarrow a \in K \land k \rightarrow a \in T \land k <_S i \land \neg (\exists j : j \rightarrow a \in (T \cup Y) \land k <_S j <_S i)\}$  (6.17)

may-no-source 关系为:

$\{ i \rightarrow a \in K : \neg (\exists j : j \rightarrow a \in T \land j <_S i) \}$


must-no-source关系为：

$\{ i \rightarrow a \in K : \neg (\exists j : j \rightarrow a \in (T \cup Y) \land j <_S i) \}$

在`isl`中，近似数据流分析的函数可以通过`isl_union_access_info_compute_flow` 函数实现。该函数的输入数据类型为`isl_union_access_info`对象（描述汇点、must-souce、may-source以及调度）作为输入，并输出一个`isl_union_flow`对象（描述may-dependence关系、must-dependence关系、may-no-source关系以及must-no-source关系）作为输出。该函数的实现结合了前面的几个Section, 但是不需要构造一个全局的顺序关系$<_S$。`isl_union_access_info`对象通过sink关系被构造，即通过调用函数`isl_union_access_info_from_sink`。must-source，may-source以及调度信息（调度树形式或者Preburger关系）可以使用如下函数进行设置。

- `isl_union_access_info_set_must_source`
- `isl_union_access_info_set_may_source`
- `isl_union_access_info_set_schedule` 此函数在调度是调度树的情况下使用
- `isl_union_access_info_set_schedule_map` 此函数在调度是一个Presburger关系的情况下使用

如果must-source 以及/或者 may-source 没有设置，那么就假定它们是空的。但是调度信息必须被设置。may-dependence关系、must-dependence关系、may-no-source关系以及must-no-source关系可以通过`isl_union_flow`对象使用如下方法提取出来。

- `isl_union_flow_get_full_may_dependence` 返回（6.16）完整的may-dependence关系。
- `isl_union_flow_get_full_must_dependence` 返回（6.17）完整的must-dependence关系。
- `isl_union_flow_get_may_dependence` 返回与投影处的访问元素的may-dependence关系，即完整的may-dependence关系的使用`range product`计算的range factor结果。
- `isl_union_flow_get_must_dependence` 返回与投影处的访问元素的must-dependence关系。即完整的must-dependence关系的使用`range product`计算的range factor结果。
- `isl_union_flow_get_may_no_source`
- `isl_union_flow_get_must_no_source`

在`iscc`中，近似数据流分析可以使用`last-any-before-under`的操作来实现。其中，参数`last`指定了must-source，参数`any`指定了may-source，参数`before`指定了sink，参数`under`指定了调度（使用调度树或者二元关系的形式）。`last`或`any` 之一（连同其参数）可以省略。如果`last`被使用，那么结果是一个包含must-dependence关系和must-no-source关系的列表。否则，输出是一个may-dependence关系。

---
本section相当重要，可惜以上内容没太看明白 orz。（有一些概念在数据流分析的教程中没有看到）

其中有一些概念需要先弄明白
- source，即源的概念是指什么?
- sink
- may-source
- must-source
- may-no-source
- must-no-source
- may-dependence
- must-dependence

可以先看一下例子再回过头来理解这些概念

---

## 6.4 Applications of Approximate Dataflow Analysis
近似数据流分析操作最明显的应用是计算数据流依赖关系。其中，`sink`被设置成`may-read`访问关系，`may-source`设置成`may-write`访问关系，`must-source`设置成`must-write`访问关系。得到的`may-dependence`关系表示的是`may-dataflow dependence`关系，而`must-dependence`关系表示的`must-dataflow dependence`关系。此外，`may-no-source`关系可以用作`may-live-in`关系。该关系（指`may-live-in`）包含了读取访问关系，这些读取访问可能读取未写入分析程序片段内的值。如果写访问关系是确切已知的，那么只有`must-source`需要被指定，`must-no-source`关系可表示准确的`live-in`关系。


---
是不是可以理解成如下？

`sink`就是`may-read`；`may-source`就是`may-write`；`must-source`就是`must-write` ?

---

### Example 6.6

下面展示了使用近似数据流分析计算数据流依赖的计算过程的一个确切案例。得到的结果与example 6.2和exapmle 6.4相同，这里也是假设写入访问关系是精确的。此外，`live-in`访问关系可以被计算。所有的再语句S当中读取A都是`live-in`的。


```python
P := parse_file "demo/false.c";
Write := P[2];
Read := P[3];
Schedule := P[4];
F := last Write before Read under Schedule ; # 应该可以直接从语法上来猜测该功能，“在调度的条件下，读之前的最后一次写操作”， 就是在计算数据流依赖。
print " Flow dependences :";
print F[0];
print "Live -in accesses :";
print F[1];
```

输出为:

```python
" Flow dependences :"
[n] -> { S[i] -> T[i] : 0 <= i < n }
"Live -in accesses :"
[n] -> { S[i] -> A[i] : 0 <= i < n }
```

### Example 6.7

