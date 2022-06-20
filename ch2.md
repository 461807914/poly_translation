# Set of Name Integer Tuples
本章描述了本教程后面用于表示各种实体的抽象元素、这些元素的集合和二元关系以及对这些集合和关系的操作。 为了使对多面体编译不感兴趣的读者能够理解本章，我们对这些概念进行了纯粹抽象的处理。 此外，本章中的所有集合都将进行宽泛的描述。 详细描述在第 3 章 Presburger 集合和关系的主题。

## 2.1 Named Integer Tuples
本教程中考虑的对象每个都由一个命名的整数元组(named integer tuple)表示，由一个标识符（名称）和一个整数值序列组成。标识符可以省略，整数序列的长度可以为零。 如果两个这样的命名整数元组具有相同的标识符和相同的整数值序列，则它们被认为是相同的。

### Notation 2.1 (Named Integer Tuple)
命名整数元组（Named Integer Tuple）的符号由标识符组成，后跟以逗号分隔的方括号中的整数值列表。例如，没有标识符且具有零长度整数序列的“命名”整数元组写成`[]`。 具有标识符 A 和整数序列 2、8 和 1 的命名整数元组写成`A[2, 8, 1]`。 命名整数元组将扩展为第 28 页定义 2.66 中的结构化命名整数元组。

### Alternative 2.2 (Unnamed Integer Tuples)
一些框架只处理整数序列，不支持显式标识符(explicit indentifier)。 为了防止在概念上存在不同类型的此类序列的情况，通常通过添加在序列开头或结尾的附加整数值对不同类型进行编码。例如，如果 A 被赋值为 0，那么上面命名的元组可以表示为`[0, 2, 8, 1]`。

## 2.2 Sets
一组命名整数元组包含零个或多个命名整数元组作为元素。

### Notation 2.3 (Set)
集合的表示法由用大括号括起来的以分号分隔的元素列表构成。集合中的元素没有定义顺序。 这尤其意味着，一个集合中的元素可能以与定义它的顺序不同的顺序打印。 集合中的元素不能重复。 也就是说，一个元素要么属于一个集合，要么不属于一个集合，但它不能多次属于该集合。例如下面集合
`{[]; A[2, 8, 1]}`与集合`{A[2, 8, 1];[];[]}`是等价的。
在isl中，这样的集合表示为一个`isl_union_set`。空集写成`{}`或者`φ`，在iscc中写成`{}`。在isl中，空寂可以使用`isl_union_set_empty`来创建。

### Alternative 2.4 （Fixed-dimensional Sets)
一些框架不允许将不同大小的整数元组组合到同一个集合中。然后通常用任意整数值（例如，零）填充较小大小的元组。例如，如果`A[2, 8, 1]`被编码为`[0, 2, 8, 1]`，如 Alternative 2.2 Unnamed Integer Tuples 中那样，并且如果该元素需要与`B[5]`在同一个集合中组合，则后者可以编码为`[1, 5, 0, 0]`，假设 `B` 由值 1 表示。

### 2.2.1 Basic Operations
最基本的操作是交集、并集和集差。

#### Operation 2.5 (Intersection of Sets)
两个集合 A 和 B 的交集 `A ∩ B` 包含同时包含在 A 和 B 中的元素。
在 isl 中，此操作称为`isl_union_set_intersect`。在 iscc 中，这操作写成`*`。

#### Example 2.6 
iscc input
```python
{ B [0]; A [2 ,8 ,1] } * { A [2 ,8 ,1]; C [5] };
```
iscc output
```python
{ A [2 , 8 , 1] }
```

#### Example 2.7  
使用 python 接口可以获得与示例 2.6 相同的结果，如下所示。
```python
import isl
s1 = isl . union_set ( " { B [0]; A [2 ,8 ,1] } " )
s2 = isl . union_set ( " { A [2 ,8 ,1]; C [5] } " )
print s1 . intersect ( s2 )

```
输出为：
```python
{ A [2 , 8 , 1] }
```

#### Operation 2.8 (Union of Sets)
两个集合 A 和 B 的并集 `A∪` 包含 A 或 B 中包含的元素。
在isl，这个操作可以调用`isl_union_set_union`。在iscc中，该操作写作`+`。

#### Example 2.9
```python
{ B [0]; A [2 ,8 ,1] } + { A [2 ,8 ,1]; C [5] };
```
输出为：
```python
{ C [5]; B [0]; A [2 , 8 , 1] }
```
请注意，由于集合中的元素没有定义顺序，因此union中的元素可能会以不同的顺序打印在屏幕上。

#### 2.10 （Set Difference)
两个集合 A 和 B 的差 `A \ B` 包含 A 中包含但 B 中不包含的元素。
在isl中，该操作调用`isl_union_set_substrace`。在iscc中，该操作写为`-`。


#### 2.11
iscc的输入为
```python
{ B [0]; A [2 ,8 ,1] } - { A [2 ,8 ,1]; C [5] };
```
iscc的输出为
```python
{B[0]}
```

### 2.2.2 Comparisons