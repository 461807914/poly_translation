# Poluhedral Model

## 5.1 Main Concepts
多面体模型是一段代码的抽象，它在各种上下文中使用，因此存在于各种变体（incarnation）中。 尽管它们的名称和表示方式可能不同，但它们都有一些共同的概念。

**Instance Set** 

实例集合是所有“动态执行实例”的集合，例如，一段抽象代码中执行运算部分的集合。

**Dependence Relation**

依赖关系是实例集元素之间的二元关系，其中一个实例以某种方式依赖于另一个。可以考虑几种类型的依赖关系，并且一个实例对另一个实例的依赖的确切性质取决于依赖关系的类型。但是，通常依赖关系表示一个实例需要在另一个实例之前执行。

**Schedule**

一个调度关系（schedule）S定义了一个严格的偏序关系（strict partial order）$<_{S}$，比如一个满足反自反性（irreflexive）和传递性（transitive）的关系，对应到instance set上的元素，表示的是这些instance的执行顺序。

虽然一些多面体编译技术仅将多面体模型用于分析目的，但其他人也使用它来转换所考虑的程序片段。这些转换时通过修改调度顺序（schedule）来表达的。生成的调度顺序需要满足如下属性。


---
这里解释一下上面的严格偏序关系


普通的偏序关系满足如下性质：

给定集合S，设$\le$为集合上的二元关系

1. 自反性: $\forall a \in S, a \leq a$
2. 反对称性: $\forall a, b \in S, a \leq b\ and\ b \leq a$ 则a = b
3. 传递性: $\forall a, b, c \in S, a \leq b\ and\ b \leq c$则 $a \leq c$

严格偏序关系

给定一个集合S, < 是集合S上的二元关系，若 < 满足:
1. 反自反性: $\forall a \in S, a \nless a$
2. 反对称性: $\forall a, b \in S, a < b \Rightarrow b \nless a$
3. 传递性:  $\forall a, b, c \in S, a < b\ and\ b < c$则 $a < c$

严格偏序关系对应一个有向无环图


### Definition 5.1 (Valid Schedule)
设D为依赖关系（dependence relation），表示第一个实例（instance）需要在第二个实例之前执行。设S表示一个调度顺序。调度顺序为一个合理的调度（valid schedule）时，满足依赖关系D，即：

$D \subseteq (<_{S})$

为了满足实例自身的依赖，该条件可以放宽到如下：

$D \backslash 1_{dom\ D} \subseteq (<_{S})$

另外一个常用的抽象关系时访问关系（access relation）。该关系将实例集合的元素映射到某个数据集合的元素，并表示实例集合给定的元素可以访问那些数据元素。

在`iscc`中，`parse_file`操作可以用来从C语言的源码当中提取部分多面体模型。特别是，该操作从源码中第一个最合适的区域中提取出一个多面体模型。该操作以源文件的名字的字符串作为输入，并返回一个包含实例结合的列表（见5.2 Instance Set），must-write关系，may-write关系，may-read关系（见5.3 Acess Relation），以及一个原始调度表示（见5.6 Schedule）。

pet的`pet_scop_extract_from_C_source`函数可以用用来从一个C语言的源码中的一个指定的函数中提取多面体模型。尤其是，从该函数的第一个合适区域中提取`pet_scop`形式的多面体模型。该函数通过`python`的接口导出到`pet`。使用`pet_scop_get_schedule`函数可以用来从`pet_scope`中提取调度。函数`pet_scop_get_instance_set`可以用来从`pet_scop`中提取实例集合。一下函数可以用来提取访问关系（access relation）。
- pet_scop_get_may_read
- pet_scop_get_may_writes
- pet_scop_get_must_writes

## 5.2 Instance Set
### 5.2.1 Definition and Representation

### Definition 5.2 (Instance Set)
实例集合是所有动态执行实例的集合。

动态执行实例通常以组（groups）的形式出现，这些组对应于所表示的程序中的代码片段。组中的不同实例对应于运行时相应代码段的不同执行（distinct executions）。如果程序以源代码形式进行分析和/或转换，那么这些组通常是被分析代码片段中的语句，但是一个语句(statement)也可以分解为几个组，或者相反，一个组也可能包含多个语句。如果程序以编译的形式被分析，那么这些组通常对应于编译器内部表示中的基本块。为了简化讨论，比如组（group），无论是否表示一个程序语句（statement)，一个基本块或者是一些其它的概念，全部统称为多面体语句（polyhedral statement）。

多面体语句的概念的更多细节会在5.8 中的多面体语句中讨论。

通过在每个元素的名称中编码多面体语句并在其整数值中编码多面体语句的动态实例，可以将实例集表示为 Presburger 集。尤其是，如果一个多面体语句嵌套n层循环，那么这个动态实例通常（不是必须的）会表示成n个整数值，每个整数值表示一个循环的迭代数。应该注意，实例集元素中的这些整数序列仅用于识别不同的动态实例，并且它们并不暗示任何特定的执行顺序。也要注意，如果一个多面体模型仅被用于分析程序，例如判定程序中的循环属性，那么语句实例和循环迭代之间的映射要么是隐式的（implicit），要么是单独跟踪的（track of separately）。

### Exmaple 5.3
代码片段5.1 计算了两个向量A和B的内积，A和B的向量长度是100。在该程序段中有两个程序语句（program statements），一个用标签S标记，另一个用标签T。将这两个程序语句看成**多面体语句**。在该代码片段的执行阶段，标记有标签S的语句执行了一次，然而标记有标签T的语句执行了100次。这100个循环当中，在运行期间每一个都可以用循环迭代值$i$来表示。即程序片段中的实例可以表示成如下的**实例集合**：

$\{ S[]; T[i] : 0 \leq i < 100 \}$

在分析的程序片段内未修改的程序变量可以用常量符号表示，因为它具有固定（但未知）的值。 这样的变量也称为参数。

![长度为100的两个向量的内积](./5.1.png)