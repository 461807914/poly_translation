# introduce
该教程主要提供给想学习polyhedral编译的读者。主要关注概念和涉及到的操作，以及如何使用这些概念和操作完成基本的任务。在定义polyhedral编译的核心概念有一些变化。本文使用的工具是`isl`，比如`PPCG`。然而，其它常见变体(variation)也会在这里被涉及到，用来帮助读者理解ployhedral编译的理论。这些变体(variation)会被放在Alternatives部分,对isl专业术语（terminology)感兴趣的读者可能会跳过此部分。尽管本文尽量覆盖polyhedral编译技术的大部分主题，但是本文依旧有一些偏颇
(biased)以及本文从未声明是完善的。事实上，当前的初步版本是非常不完善的。

## 1.1 Polyhedral Compilation

从广义上来说，polyhedral编译技术（以后称为多面体编译）是一个程序分析和编译技术的合集，这些技术可以推断程序中的各个“动态执行实例”(dynamic excution instances)以及这些实例对之间的关系。一个动态执行实例是指一个操作(operation)或者一组操作在运行时执行，而不是这些操作在程序代码中出现的样子。
例如，一个语句(statement)出现在一个循环的程序当中，那么随着循环的迭代，会有很多个实例(instance)产生。因为在程序中可能有很多，甚至无限多的这样的实例(instances)，因此通常使用polyhedra模型和Presburger公式等数学模型来对其进行描述。更多的细节在第三章的 Presburger Sets and Relations描述。注意，在polyhedral编译中使用ployhedra不是必须，因为有可能在没有polyhedra（以后称为多面体）的情况下执行多面体编译，并且在多面体编译之外还有一些技术，比如abstract interpretation和array region analysis，也可以使用多面体。
下面的例子提供了一些在本教程中将要做的内容。该例子仅展示使用多面体编译的一个例子。
![fig_1.1](./1.1.png)

**Example 1.1**
考虑图1.1左上角部分的代码段。这是一个非常简短的两个循环的代码段，每个循环包含了一个语句。在这个例子当中，“动态执行实例”就是这两个语句。每个语句执行三次，每次循环迭代时执行一次。
