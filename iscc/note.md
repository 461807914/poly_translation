# 安装
参考如下链接的内容安装iscc 

https://kumasento.github.io/2020-07-04-setting-up-development-environment-of-the-barvinok-library/

iscc的安装需要依赖第三方库包括gmp（一个高精度计算库），NTL计算库（一个数论的计算库），llvm（编译工具链，版本要最好是按照上面链接中安装9.0的），Barvinok（iscc本身）。

首先配置安装环境的环境变量，将所有生成的头文件以及库文件都放到一个指定的目录下面，并在环境变量中配置索引到该目录的环境。

```shell
export PATH=${PREFIX}/bin:${PATH}
export LD_LIBRARY_PATH=${PREFIX}/lib:${LD_LIBRARY_PATH}
```

llvm，gmp，NTL以及Barvinok 的安装步骤分别如下:

```shell
# Download llvm-9.0.1 from GitHub
wget https://github.com/llvm/llvm-project/releases/download/llvmorg-9.0.1/llvm-project-9.0.1.tar.xz
# Untar
tar xvf llvm-project-9.0.1.tar.xz
# CMake
cd llvm-project-9.0.1 && mkdir build && cd build
cmake -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld" \
			-DCMAKE_INSTALL_PREFIX=${PREFIX} \
      -DLLVM_BUILD_LLVM_DYLIB=ON ../llvm
# Build
make 
# Install
make install
```

```shell
wget https://gmplib.org/download/gmp/gmp-6.2.0.tar.xz
tar xvf gmp-6.2.0.tar.xz
cd gmp-6.2.0
./configure --prefix=${PREFIX}
make
make check
make install
```

```shell
wget https://shoup.net/ntl/ntl-11.4.3.tar.gz
tar xvf ntl-11.4.3.tar.gz
cd ntl-11.4.3/src
./configure NTL_GMP_LIP=on PREFIX=${PREFIX} SHARED=on GMP_PREFIX=${PREFIX}
make
# This may take a while ...
make check
make install
```

```python
git clone --recurse-submodules git://repo.or.cz/barvinok.git
cd barvinok
git checkout barvinok-0.41.3
```

如果想使用python，也可以将python安装到目录当中,比如上面链接中给出的是python 3.8

```python
wget xxxx 
./configure --prefix=${PREFIX} --enable-shared --enable-optimization
make
make test
make install
```
进入到barvinok目录中进行编译，编译选项和命令如下：

```shell
sh autogen.sh # 生成configure
./configure \
	--prefix=${PREFIX} \
	--with-ntl-prefix=${PREFIX} \
  --with-pet=bundled \
  --with-isl=bundled \
  --with-clang-prefix=${PREFIX} \
  --enable-shared-barvinok
make 
make check
make install

```

验证iscc是否安装成功


```shell
$ iscc --version
isl-0.22.1-347-g7ef6ed0c-IMath-32
barvinok-0.41.3
 -INCREMENTAL
 +PET -OMEGA -CDDLIB -GLPK -TOPCOM +ZSOLVE -PARKER
clang version 9.0.1
pet-0.11.3
```

使用python环境测试为：

```shell
python3 -c 'import isl'
```

# 第一个例子

在poly tutorial的第6章的依赖关系部分的内容为例子:

首先构造souce.c代码如下:
```c
float f1(float);
float f2(float);

void f(int n, float A[restrict static n], float B[restrict static n]) {
    float t;
    for (int i = 0; i < n; ++i) {
        t = f1(A[i]);
        B[i] = f2(t);
    }
}
```
使用iscc提取上面source.c中的各个关系代码`ex_6_1.iscc`如下:

```python
P := parse_file "source.c";
Iter_domain := P[0];
Must_write := P[1];
Write := P[2];
Read := P[3];
Ori_schedule := P[4];

print "Iter domain:";
print Iter_domain;

print "Must write:";
print Must_write;

print "May write:";
print Write;

print "Read:";
print Read;

print "Origin schedule:";
print Ori_schedule;

Schedule := map(P[4]);
```

运行的方式需要执行如下命令:

```shell
iscc < ex_6_1.iscc
```
输出结果为:

```shell
"Iter domain:"
[n] -> { S_2[i] : 0 <= i < n; S_3[i] : 0 <= i < n }
"Must write:"
[n] -> { S_3[i] -> B[i] : 0 <= i < n; S_2[i] -> t[] : 0 <= i < n }
"May write:"
[n] -> { S_3[i] -> B[i] : 0 <= i < n; S_2[i] -> t[] : 0 <= i < n }
"Read:"
[n] -> { S_3[i] -> t[] : 0 <= i < n; S_2[i] -> A[i] : 0 <= i < n }
"Origin schedule:"
domain: "[n] -> { S_2[i] : 0 <= i < n; S_3[i] : 0 <= i < n }"
child:
  schedule: "[n] -> L_0[{ S_3[i] -> [(i)]; S_2[i] -> [(i)] }]"
  child:
    sequence:
    - filter: "[n] -> { S_2[i] }"
    - filter: "[n] -> { S_3[i] }"
```

可以看到，使用`parse_file`函数可以直接从源码中提取处5个信息，分别为
- 迭域 domain
- 必然写访问关系 must write access relation
- 可能写访问关系 may write access relation
- 读访问关系 read access relation
- 原始调度信息 origin schedule（使用调度树的形式表达出来)

**重点:**

- 迭代域数据元素类型是presburger 运算的集合，描述一个语句的迭代范围;
- 访问关系是是presburger运算的关系，描述的是一个语句实例到变量之间的映射，即当前的语句实例会访问哪些内存单元，\[语句实例\]->\[内存变量\]包括写或者读（注意区分语句和语句实例的概念）;
- 原始的调度信息是以调度树的形式表现的。

## 读写关系

读写关系包含三种，读后写，写后读以及写后写。计算这三种关系需要写访问关系、读访问关系以及调度顺序信息。
其中写访问关系以及读访问关系可以直接提取出来，调度顺序可以使用调度计算出来，如下:

其中调度顺序的符号表示为$<_S$ （顺序从小到大）

以下分别为写后读、读后写以及写后写三种关系。$\circ$符号表示组合运算，详见ch2 operation 2.32

$(R^{-1} \circ W)\  \cap <_S$

$(W^{-1} \circ R)\  \cap <_S$

$(W^{-1} \circ W)\  \cap <_S$

组合运算符在iscc中的表示为 '.'，即一个点。而且组合运算的两个操作数的顺序与公式中是相反的。

调度顺序的计算使用$<_S = S \preccurlyeq S$获取，详见ch3 operation 3.70。

代码如下:

```shell
P := parse_file "source.c";
Iter_domain := P[0];
Must_write := P[1];
Write := P[2];
Read := P[3];
Ori_schedule := P[4];

print "Iter domain:";
print Iter_domain;

print "Must write:";
print Must_write;

print "May write:";
print Write;

print "Read:";
print Read;

print "Origin schedule:";
print Ori_schedule;

Schedule := map(P[4]);

print "Schedule:";
print Schedule;

Order := Schedule << Schedule;

print "Order relation:";
print Order;

print "read-after-write dep:";
RAW := (Write . Read^-1) * Order;
print RAW;

print "write-after-read dep:";
WAR := (Read . Write^-1) * Order;
print WAR;

print "write-after-write dep:";
WRW := (Write . Write^-1) * Order;
print WRW;
```

输出结果为:

```shell
"Iter domain:"
[n] -> { S_2[i] : 0 <= i < n; S_3[i] : 0 <= i < n }
"Must write:"
[n] -> { S_3[i] -> B[i] : 0 <= i < n; S_2[i] -> t[] : 0 <= i < n }
"May write:"
[n] -> { S_3[i] -> B[i] : 0 <= i < n; S_2[i] -> t[] : 0 <= i < n }
"Read:"
[n] -> { S_3[i] -> t[] : 0 <= i < n; S_2[i] -> A[i] : 0 <= i < n }
"Origin schedule:"
domain: "[n] -> { S_2[i] : 0 <= i < n; S_3[i] : 0 <= i < n }"
child:
  schedule: "[n] -> L_0[{ S_3[i] -> [(i)]; S_2[i] -> [(i)] }]"
  child:
    sequence:
    - filter: "[n] -> { S_2[i] }"
    - filter: "[n] -> { S_3[i] }"

"Schedule:"
[n] -> { S_3[i] -> [i, 1]; S_2[i] -> [i, 0] }
"Order relation:"
[n] -> { S_3[i] -> S_3[i'] : i' > i; S_3[i] -> S_2[i'] : i' > i; S_2[i] -> S_2[i'] : i' > i; S_2[i] -> S_3[i'] : i' > i; S_2[i] -> S_3[i' = i] }
"read-after-write dep:"
[n] -> { S_2[i] -> S_3[i'] : 0 <= i < n and i' > i and 0 <= i' < n; S_2[i] -> S_3[i' = i] : 0 <= i < n }
"write-after-read dep:"
[n] -> { S_3[i] -> S_2[i'] : 0 <= i < n and i' > i and 0 <= i' < n }
"write-after-write dep:"
[n] -> { S_2[i] -> S_2[i'] : 0 <= i < n and i' > i and 0 <= i' < n }
```

可见，在iscc中，将调度树转换为二元关系的操作即使用`map()`运算即可。

**重点:**

- 将调度树转换为二元关系形式是\[语句实例\]->\[调度顺序\]，后面的调度顺序使用字典序大小排列。
- 通过使用iscc字典序小于关系运算符`<<`可以得到调度顺序，调度顺序是一个二元关系，\[语句实例\]->\[语句实例\]，表示语句实例之间的执行顺序，在箭头前面的先执行，在箭头后面的后执行。
- 计算得到的读后写、写后读以及写后写三种关系中，同样是\[语句实例\]->\[语句实例\]，比如写后读操作的一个表达式，箭头前面的语句表示S2\[i\]语句先执行写入操作，随后S3\[i'\]语句再执行读取操作，要求i'>i。
- 从`iscc`的`parse_file`函数中读取到的信息，按照顺序分别为`instance set`、`must-write`访问关系、`may-write`访问关系、`may-read`访问关系以及一个`origin schedule`。注意没有`must-read`的说法。


## 数据流依赖

在ch6原文中对数据流依赖的解释是:a data flow dependence is a read-after-write dependence for which there is no intermediate write to the same memory location.
即数据流依赖是一个没有对相同内存位置执行写入操作的写后读依赖。

既然需要判断哪些内存单元被访问了，那么\[语句实例\]->\[语句实例\]这样的读写访问关系表达方式就不会体现出对哪写内存变量进行访问，因此要对原始的读和写的访问关系中访问内存变量的部分机进行保留。保留的方法为将读、写的形式\[语句实例\]->\[内存变量\]修改成\[\[语句实例\]->\[内存变量\]\] -> \[内存变量\]这样的形式，再后续的关系运算中，即使消去range部分的内容，也能保留内存变量这一信息。以读操作为例，该操作的数学符号形式为$R_1 = \xrightarrow{ran}R$，该操作为投影运算，详见ch2 operation 2.102。 类似的，如果想要保留一个映射当中的信息（key或者value），就可以使用投影运算来实现。

上面的读写关系变成了\[\[语句实例\]->\[内存变量\]\] -> \[内存变量\]这样的形式，但是需要与之进行运算的调度顺序$<_S$的形式为\[语句实例\]->\[语句实例\]，无法与投影后的读写关系进行运算，因此需要将调度顺序的计算公式也要修改一下。

$S_1 = S \circ (\xrightarrow{dom}(R \cup W)$

其中$\xrightarrow{dom}$表示再domain上的投影，再对得到的$S_1$使用iscc中的$S_1 << S_1$运算，即可得到变换后的调度顺序。

计算数据流依赖的方法根据定义，其计算公式为:

$F_1 = D_1 /\ (D_1 \circ O_1)$，其中斜线表示集合集合减法操作。$D_1$和$O_1$分别为变换后的写后读依赖以及写后写依赖关系。

其中$D_1$和$O_1$的计算公式如下:

$D_1 = (R^{-1}_1 \circ W_1) \cap <_{S_1}$ 

$O_1 = (W^{-1}_1 \circ W_1) \cap <_{S_1}$ 

代码为:

```shell
P := parse_file "source.c";
Write := P[2];
Read := P[3];
Schedule := map(P[4]);

# range project operation
Write1 := range_map Write;
Read1 := range_map Read;

print "Write:";
print Write;

print "Write1:";
print Write1;

print "Read:";
print Read;

print "Read1:"
print Read1;

Schedule1 := (domain_map (Read + Write)) . Schedule;

print "Schedule:";
print Schedule;

print "Schedule1:";
print Schedule1;

Order1 := Schedule1 << Schedule1;

print "Order1:";
print Order1;

RAW := (Write1 . Read1^-1) * Order1;
WAW := (Write1 . Write1^-1) * Order1;

print "read after write:";
print RAW;

print "write after write:";
print WAW;

Flow := RAW - (WAW . RAW);

print "flow:";
print Flow;
```

输出为

```shell
"Write:"
[n] -> { S_3[i] -> B[i] : 0 <= i < n; S_2[i] -> t[] : 0 <= i < n }
"Write1:"
[n] -> { [S_3[i] -> B[i]] -> B[i] : 0 <= i < n; 
         [S_2[i] -> t[]] -> t[] : 0 <= i < n }
"Read:"
[n] -> { S_3[i] -> t[] : 0 <= i < n; 
         S_2[i] -> A[i] : 0 <= i < n }
"Read1:"
[n] -> { [S_3[i] -> t[]] -> t[] : 0 <= i < n;
         [S_2[i] -> A[i]] -> A[i] : 0 <= i < n }
"Schedule:"
[n] -> { S_3[i] -> [i, 1]; 
         S_2[i] -> [i, 0] }
"Schedule1:"
[n] -> { [S_2[i] -> t[]] -> [i, 0] : 0 <= i < n;
         [S_2[i] -> A[i]] -> [i, 0] : 0 <= i < n;
         [S_3[i] -> t[]] -> [i, 1] : 0 <= i < n;
         [S_3[i] -> B[i]] -> [i, 1] : 0 <= i < n }
"Order1:"
[n] -> { [S_3[i] -> B[i]] -> [S_3[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> t[]] -> [S_3[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> t[]] -> [S_3[i' = i] -> B[i]] : 0 <= i < n;
         [S_2[i] -> A[i]] -> [S_2[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_3[i] -> B[i]] -> [S_2[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> t[]] -> [S_2[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> A[i]] -> [S_3[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> A[i]] -> [S_3[i' = i] -> B[i]] : 0 <= i < n;
         [S_2[i] -> A[i]] -> [S_3[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> A[i]] -> [S_3[i' = i] -> t[]] : 0 <= i < n;
         [S_2[i] -> A[i]] -> [S_2[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> t[]] -> [S_2[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_3[i] -> t[]] -> [S_2[i'] -> A[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_3[i] -> t[]] -> [S_2[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_3[i] -> B[i]] -> [S_3[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_3[i] -> B[i]] -> [S_2[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_3[i] -> t[]] -> [S_3[i'] -> B[i']] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> t[]] -> [S_3[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> t[]] -> [S_3[i' = i] -> t[]] : 0 <= i < n;
         [S_3[i] -> t[]] -> [S_3[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n }
"read after write:"
[n] -> { [S_2[i] -> t[]] -> [S_3[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;
         [S_2[i] -> t[]] -> [S_3[i' = i] -> t[]] : 0 <= i < n }
"write after write:"
[n] -> { [S_2[i] -> t[]] -> [S_2[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n }
"flow:"
[n] -> { [S_2[i] -> t[]] -> [S_3[i' = i] -> t[]] : 0 <= i < n }
```

可以看到上面的写后读关系变成了\[\[语句实例\]->\[内存变量\]\]->\[\[语句实例\]->\[内存变量\]\]的形式，保留了内存变量的信息。

如果不想将调度S变换成$S_1$，可以使用如下的计算公式也达到相同的效果。

$D_1 = zip((zip(R^{-1}_1 \circ W_1)) \cap {}_{dom} WRAP(<_S))$

$O_1 = zip((zip(W^{-1}_1 \circ W_1)) \cap {}_{dom} WRAP(<_S))$

再带入到公式 $F_1 = D_1 /\ (D_1 \circ O_1)$ 当中，结果相同。


观察一下写后读的关系表达式，其中包含两个表达式，分别为:

```shell
# 第一个
[S_2[i] -> t[]] -> [S_3[i'] -> t[]] : 0 <= i < n and i' > i and 0 <= i' < n;

# 第二个
[S_2[i] -> t[]] -> [S_3[i' = i] -> t[]] : 0 <= i < n
```

其中第一个表达式表达的内容，满足条件的情况包括`S_2[0]`先写入到`t`当中，`S_3[1]`再读取t中的内容，很显然，S_2写入的t与S_3读取的t不是一个，正常情况应该像第二个表达式一样，`s_2[0]`先写入到t，随后`S_3[0]`读取t。

即第二个表达式的关系是满足程序中数据流动的情况的。第一个表达式只能说它满足先写后读这样的关系，而数据流依赖关系就是为了去掉写后读依赖中存在的第一个表达式的情况。


即使用$RAW \circ WAR$即得到第一个表达式

这是因为，写后写的依赖关系，在描述内存变量t时，只能描述该变量随着迭代下标表示的先后写入关系。