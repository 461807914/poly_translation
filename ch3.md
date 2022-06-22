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

