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

迭代域数据元素类型是presburger 运算的集合，描述一个语句的迭代范围;
访问关系是是presburger运算的关系，描述的是一个语句实例到变量之间的映射，即当前的语句实例会访问哪些内存单元，包括写或者读（注意区分语句和语句实例的概念）;
原始的调度信息是以调度树的形式表现的。

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



## 数据流依赖

在ch6原文中对数据流依赖的解释是:a data flow dependence is a read-after-write dependence for which there is no intermediate write to the same memory location.
即数据流依赖是一个没有对相同内存位置执行写入操作的写后读依赖。