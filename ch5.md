# Poluhedral Model

## 5.1 Main Concepts
多面体模型是一段代码的抽象，它在各种上下文中使用，因此存在于各种变体（incarnation）中。 尽管它们的名称和表示方式可能不同，但它们都有一些共同的概念。

**Instance Set** 


**Dependence Relation**


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