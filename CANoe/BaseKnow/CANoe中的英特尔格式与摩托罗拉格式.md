# CANoe中的英特尔格式与摩托罗拉格式



## 一、 背景说明

制作过DBC文件的人都知道信号(Signal)的**字节排序(Byte Order)属性** 中有英特尔格式(Inter)格式与摩托罗拉(Motorola)格式可以选择，如下：

![Vector_Base_Signal_Example_1](.//Picture//Vector_Base_Signal_Example_1.png)

这两种格式对应的就是我们常说的大端模式(Big-endian)和小端模式(Little-endian).



### 1.1. 介绍大端模式与小端模式

举一个例子，比如我们要保存一个数字： `0x12 34 56 78` ， 通过它在内存中的分布位置来说明大小端存储的差异。

**大端模式(Big-Endian)：就是高位字节排放在内存的低地址端，低位字节排放在内存的高地址端**

```
低内存地址 -------------> 高内存地址
0x12  |  0x34  |  0x56  |  0x78
```



**小端模式(Little-Endian)：就是低位字节排放在内存的低地址端，高位字节排放在内存的高地址端。**

```
低内存地址 -------------> 高内存地址
0x78  |  0x56  |  0x34  |  0x12
```



可以很明显看到， 大端模式与我们直观非常相近，因为我们书写习惯是将高位写在前面，低位写在后面。

我们常用的X86结构是小端模式；并且很多的ARM架构也都为小端模式。


#### 举个例子

16bit宽的数字`0x1234`在Little-endian/Big-endian模式下， 内存中的存放方式（假设从地址0x4000开始存放）为：

| **内存地址** | **小端模式存放内容** | **大端模式存放内容** |
| ------------ | -------------------- | -------------------- |
| **0x4000**   | **0x34**             | **0x12**             |
| **0x4001**   | **0x12**             | **0x34**             |

32bit宽的数字`0x12345678` 在Little-endian/Big-endian模式下，内存中的存放方式（假设从地址0x4000开始存放）为：

| **内存地址** | **小端模式存放内容** | **大端模式存放内容** |
| ------------ | -------------------- | -------------------- |
| **0x4000**   | **0x78**             | **0x12**             |
| **0x4001**   | **0x56**             | **0x34**             |
| **0x4002**   | **0x34**             | **0x56**             |
| **0x4003**   | **0x12**             | **0x78 **            |



####  大端模式与小端模式的优缺点


- 大端模式的优点：符号位的判定固定为第一个字节，`容易判断正负`。
- 小端模式的优点：强制转换数据`不需要调整字节`内容



### 1.2. 大端模式与小端模式的判断与转换

#### 判断电脑使用了大端模式还是小端模式

使用C语言来实现：

```c
int i=1;   
char *p=(char *)&i;   
if(*p == 1)     
    printf("小端模式"); 
else // (*p == 0)
    printf("大端模式");
```



#### 大端模式与小端模式的转换

将大端模式转换为小端模式的C实现：

```c
#define BigtoLittle16(A)                 ((((uint16)(A) & 0xff00) >> 8) | \
                                         (((uint16)(A) & 0x00ff) << 8))


#define BigtoLittle32(A)                 ((((uint32)(A) & 0xff000000) >> 24) | \
                                         (((uint32)(A) & 0x00ff0000) >> 8) | \
                                         (((uint32)(A) & 0x0000ff00) << 8) | \
                                         (((uint32)(A) & 0x000000ff) << 24))
```




### 1.3. 介绍英特尔格式与摩托罗拉格式

英特尔格式与摩托罗拉格式与我们上面介绍的大端模式、小端模式特别类似：

- `Intel`  格式：同小端(Little-endian)，低字节在前
- `Motorola `格式：同大端(Big-endian)，高字节在前



同时我们需要了解两个基本概念：

- `MSB` :   Most Significant Bit ------- 最高有效位
- `LSB` :   Least Significant Bit ------- 最低有效位



一般情况下，CAN协议在传输数据的时候，先传输`LSB` 后传输 `MSB` . 

对于数据占用一个字节(Byte)或者不足一个字节(Byte)的，其实怎么传输影响不大，但是对于数据占用多个字节(Byte)的情况，这两种方式就需要注意了。



## 二、  实际举例说明

### 2.1. 使用纯英特尔格式

假设现在有一个Message名称为`Msg_1` ,其中包含三个Signal，信息如下：

![Vector_Base_Message_Example_1](.//Picture/Vector_Base_Message_Example_1.png)

在Vector的数据库编辑工具中，可以看到这三个信号的Layout如下：

![Vector_Base_Message_Example_2](.//Picture//Vector_Base_Message_Example_2.png)

关于Vector的DBC编辑工具，做以下说明：

1. 对于标准的CAN报文，统一采用8*8表格来表示其信号布局(Layout)。 第一行表示第一个字节(也就是**Byte_0 **)，后面依次；第一列表示一个Byte中的最高bit位(也就是**bit_7** )
2. 每一个Signal都有其最低有效位(LSB与最高有效位(MSB)， 对于只占一个bit的信号，因为其LSB与MSB在一起，所以就不显示了。
3. 数据传输时候，总是遵循： **从上到下， 从右到左**。



从上图我们可以看到采用英特尔格式时：

1. 不管信号占多少个字节，只要在一个字节内部，总是高bit位置（比如bit7高于bit0）表示的高位
2. 在信号占多个字节时， LSB在前面的位置(地址小)，MSB在后面的位置(地址大)， 也就是**小端模式的低字节在前高字节在后**



### 2.2. 使用纯摩托罗拉格式

将上面介绍的`Msg_1`  中的三个Signal全部换成摩托罗拉格式，更换后如下：

![Vector_Base_Message_Example_3](.//Picture//Vector_Base_Message_Example_3.png)

在Vector的数据库编辑工具中，可以看到这三个信号的Layout如下：

![Vector_Base_Message_Example_4](.//Picture//Vector_Base_Message_Example_4.png)

从上图我们可以看到采用摩托罗拉格式时：

1. 不管信号占多少个字节，只要在一个字节内部，总是高bit位置（比如bit7高于bit0）表示的高位
2. 在信号占多个字节时， MSB在前面的位置(地址小)，LSB在后面的位置(地址大)， 也就是**大端模式的高字节在低字节在后**



### 2.3. 混合英特尔格式与摩托罗拉格式

将上面介绍的`Msg_1`  中的第1个和Signal换成摩托罗拉格式，第二个Signal保持为英特尔格式，如下：

![Vector_Base_Message_Example_5](.//Picture//Vector_Base_Message_Example_5.png)

在Vector的数据库编辑工具中，可以看到这三个信号的Layout如下：

![Vector_Base_Message_Example_6](.//Picture//Vector_Base_Message_Example_6.png)

其实这种排序完全没有任何实际意义（不会有公司采用这种方式排序的），这里仅仅是做展示。





## 三、  CAPL内置的大小端转换函数

由于Intel格式与Motorola格式之间的转换很常见，所以在CAPL内置的Byte Swapping函数，我们下面进行介绍。

### 常用的函数语法

```c
word swapWord(word x); // form 1         word (unsigned, 2 Byte)

int swapInt(int x); // form 2            int (signed, 2 Byte)

dword swapDWord(dword x); // form 3      dword (unsigned, 4 Byte)

long swapLong(long x); // form 4         long (signed, 4 Byte)

int64 swapInt64(int64 x); // form 5      int64(signed, 8 Byte)

qword swapQWord(qword x); // form 6      qword(unsigned, 8 Byte)
```

可以看到这边介绍的都是超过1个字节的数据类型(2Byte到8Byte)， 另外没有介绍：

1.  浮点型： **float (8 Byte)**, **double (8 Byte)**
2. 1个字节的Char类型： **char (1 Byte)**
3. 1个字节的Byte类型： **byte (unsigned, 1 Byte)**

### 函数功能描述

交换入参中的字节。CAPL算法遵循“小端格式”（英特尔）。交换函数用于：

1. 交换转换到“big-endian格式”（Motorola）
2. 从“big-endian格式”转换的字节

### 函数参数说明

要交换其字节的值。(Value whose bytes are to be swapped.)

### 函数返回值说明

交换字节后的值。(Value with swapped bytes.)

### 举例说明

示例代码：

```c
bigEndian = swapInt(1234); // create constant 1234 for Motorola processors
```
