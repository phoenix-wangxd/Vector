# CAPL内置的与Struct Byte有关函数

在CAPL中我们要经常和Struct Byte 打交道，为了方便的写CAPL脚本，所以我整理了Vector官方提供的与Struct Byte有关的函数，并对常用的进行简单说明。

>  本文大部分摘录自Vector的官方文档，做了整理与翻译，增加了自己的理解， 并将代码改造的更加优雅实用一些。



## 一、CAPL中与Struct Byte有关的函数

Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。

| Functions    | Short Description                                            |
| :----------- | :----------------------------------------------------------- |
| `memcmp`     | 比较入参中的**字节(bytes)** 数据                             |
| `memcpy`     | 将**字节(bytes)** 从源复制到目标                             |
| `memcpy_h2n` | 将**字节(bytes)** 从**结构(struct)** 复制到**数组(array)** 中 |
| `memcpy_n2h` | 用**数组(array)** 中的**字节(bytes)** 填充**结构(struct)**   |
| `memcpy_off` | 将**字节(bytes)** 从源复制到目标，并给出目标起始偏移量       |



为了便于理解本文中的示例代码，所以需要提前知道下面的知识：

1.  `DWORD` 就是 Double Word， 每个word为2个字节的长度;  **DWORD双字即为4个字节，每个字节是8位，共32位** 。
2.  小端(Little Endian) 模式 是嵌入式领域经常用到的排序方式， 特征为： **低位字节排放在内存的低地址端，高位字节排放在内存的高地址端**



## 二、 Struct Byte操作: 比较多个字节

### 2.1 函数:  `memcmp()`

#### 函数语法

```c
int memcmp(struct * dest, byte source[]); // form 1

int memcmp(byte dest[], struct * source); // form 2

int memcmp(struct * dest, struct * source); // form 3

int memcmp(byte dest[], byte source[], dword size); // form 4
```

#### 函数功能描述

比较入参的字节数据。在格式3中，两个结构必须具有相同的类型。

#### 函数参数介绍


| 参数         | 含义                                                       |
| ------------ | ---------------------------------------------------------- |
| `dest` | A struct                                         |
| `source` | Another struct                                   |
| `size` | Size of the arrays (number of bytes to compare). |

#### 返回值介绍

如果**字节(bytes)** 相等，则为0；如果它们不相等，则为非0的值

#### 举例说明

关于`memcmp()`函数说明的示例代码：

```c
on key 's'
{
  byte data[4];
  struct WrapDword
  {
     dword dw;
  } dwordWrapper;

  int i;
  for (i = 0; i < elcount(data); ++i){
    data[i] = i; 
  }
  dwordWrapper.dw = 0x03020100;
  
  if (memcmp(dwordWrapper, data) == 0){
    write("Data represents the number: Little Endian is used.");
  }
}
```

如果采用了**小端(Little Endian)模式** (一般的主机都是小端模式)， 输出结果：

```
Data represents the number: Little Endian is used.
```



## 三、 Struct Byte操作:  拷贝字节

在这一章节中，我们介绍四个函数：`memcmp()`、  `memcpy_n2h()`、  `memcpy_n2h()`、  `memcpy_off()` 四个函数， 它们的功能非常相似， 而且都是从`memcmp()` 的功能上进行简单的变种。



### 3.1 函数:  `memcmp()`

这个函数是最通用的拷贝字节函数，作用： 将**字节(bytes)** 从源复制到目标。

#### 函数语法

```c
void memcpy(byte dest[], struct * source); // form 1

void memcpy(char dest[], struct * source); // form 2

void memcpy(byte dest[], long offset, struct * source); // form 3

void memcpy(char dest[], long offset, struct * source); // form 4

void memcpy(struct * dest, byte source[]); // form 5

void memcpy(struct * dest, char source[]); // form 6

void memcpy(struct * dest, byte source[], long offset); // form 7

void memcpy(struct * dest, char source[], long offset); // form 8

void memcpy(struct * dest, struct * source); // form 9

void memcpy(byte dest[], byte source[], dword length); // form 10

void memcpy(byte dest[], char source[], dword length); // form 11

void memcpy(char dest[], byte source[], dword length); // form 12

void memcpy(char dest[], char source[], dword length); // form 13

void memcpy(struct dest, char source[]); // form 14

void memcpy(struct dest, byte source[]); // form 15

void memcpy(char dest[], struct source); // form 16

void memcpy(byte dest[], struct source); // form 17

void memcpy(PDUPayload dest, PDUPayload source, dword length); // form 18

void memcpy(PDUPayload dest, byte source[], dword length); // form 19

void memcpy(byte source[], PDUPayload dest, dword length); // form 20

void memcpy(PDUPayload dest, struct * source); // form 21

void memcpy(struct * dest, PDUPayload source); // form 22

void memcpy(bytes dest, byte source[]); // form 23

void memcpy(bytes dest, char source[]); // form 24

void memcpy(bytes dest, byte source[], dword length); // form 25

void memcpy(bytes dest, char source[], dword length); // form 26

void memcpy(byte dest[], bytes source); // form 27

void memcpy(char dest[], bytes source); // form 28
```

#### 函数功能详细描述

将**字节(bytes)** 从源复制到目标。在格式5中，两个结构体必须具有相同的类型。在其他具有结构体的形式中，**数组(arrays)** 必须足够大才能包含结构数据。在格式17和格式18中，**负载大小(the payload size)** 和**结构大小(the struct size)** 必须相同。



#### 函数参数介绍

| 参数     | 含义                                                         |
| -------- | ------------------------------------------------------------ |
| `source` | **(form 1, 2, 5):** Struct whose bytes shall be copied.   **(form 14, 15, 17):** Payload data of a PDU whose bytes shall be copied.    **(form 27, 28):** vCDL "bytes" value that shall be copied.  **(other forms):** Array whose bytes shall be copied. |
| `dest`   | **(form 3, 4, 5, 6, 7):** Struct into which the bytes shall be copied.    **(form 14, 16, 18):** Payload data of a PDU into which the bytes shall be copied.   **(form 23, 24, 25, 26):** vCDL "bytes" value into which the bytes shall be copied.**(other forms):** Array into which the bytes shall be copied. |
| `offset` | **(form 2, 4, 7):** Offset in the array which marks the start of the data. |
| `length` | **(form 8, 9, 10, 11, 14, 15, 16, 25, 26):** number of bytes which shall be copied. |



#### 举例说明

示例代码：

```c
on key 's'
{
  byte data[4];
  struct WrapDword
  {
     dword dw;
  } dwordWrapper;

  int i;
  for (i = 0; i < elcount(data); ++i){
    data[i] = i; 
  }

  memcpy(dwordWrapper, data);
  write("Bytes as dword: %0#10lx", dwordWrapper.dw);
  
  dwordWrapper.dw = 0x12345678;
  memcpy(data, dwordWrapper);
  write("dword as bytes: %#lx %#lx %#lx %#lx", data[0], data[1], data[2], data[3]);
}
```

如果采用了**小端(Little Endian)模式** (一般的主机都是小端模式)， 输出结果：

```
Bytes as dword: 0x03020100
dword as bytes: 0x78 0x56 0x34 0x12
```



### 3.2 函数:  `memcpy_h2n()`

这个函数与前面介绍的`memcpy()` 的区别：

将**结构体(struct)** 中的字节复制到**数组(array)** 中，**同时**将元素的字节顺序从小端(little-endian)模式转换为大端(big-endian)模式.

>  其中h2n代表“主机(host) 到网络(network)” ,  因为**一般操作系统都是小端，而通讯协议是大端的。**
>
> 1. 主机(host)侧大部分用小端(little-endian)模式
> 2. 网络(network)传输大部分用大端(big-endian)模式


#### 函数语法

```c
void memcpy_h2n(byte dest[], struct source); // form 1

void memcpy_h2n(byte dest[], int offset, struct source); // form 2
```

#### 函数参数介绍


| 参数     | 含义                                                         |
| -------- | ------------------------------------------------------------ |
| `source`        | Struct whose bytes shall be copied         |
| `dest`          | Array into which the bytes shall be copied |
| `offset (form 2)` | Offset into the array                      |

#### 举例说明

示例代码：

```c
on key 's'
{
  byte data[4];
  struct WrapDword
  {
     dword dw;
  } dwordWrapper;

  int i;
  for (i = 0; i < elcount(data); ++i){
    data[i] = i; 
  }
  memcpy_n2h(dwordWrapper, data);                      // 拷贝同时完成小端模式转大端模式
  write("Bytes as dword: %0#10lx", dwordWrapper.dw);
  
  dwordWrapper.dw = 0x12345678;
  memcpy_h2n(data, dwordWrapper);                      // 拷贝同时完成大端模式转小端模式
  write("dword as bytes: %#lx %#lx %#lx %#lx", data[0], data[1], data[2], data[3]);
}
```

输出结果：

```
Bytes as dword: 0x00010203
dword as bytes: 0x12 0x34 0x56 0x78
```





### 3.3 函数:  `memcpy_n2h()`

这个函数与前面介绍的`memcpy()` 的区别：

将**结构体(struct)** 中的字节复制到**数组(array)** 中，**同时**将元素的字节顺序从大端(big-endian)模式转换为小端(little-endian)模式.

>  其中n2h代表“网络(network) 到主机(host)” ,  因为**一般操作系统都是小端，而通讯协议是大端的。**
>
>  1. 网络(network)传输大部分用大端(big-endian)模式
>  2. 主机(host)侧大部分用小端(little-endian)模式

#### 函数语法

```c
void memcpy_n2h(struct dest, byte source[]); // form 1

void memcpy_n2h(struct dest, byte source[], int offset); // form 2
```

#### 函数参数介绍


| 参数              | 含义                                       |
| ----------------- | ------------------------------------------ |
| `source`          | Struct whose bytes shall be copied         |
| `dest`            | Array into which the bytes shall be copied |
| `offset (form 2)` | Offset into the array                      |

#### 举例说明

示例代码参见`memcpy_h2n()` 部分的说明。



### 3.4 函数:  `memcpy_off()`

这个函数与前面介绍的`memcpy()` 的区别：

>  将**字节(bytes)** 从源复制到目标，同时给出目标起始偏移量。目标的大小必须至少为`destOffset+length`。



#### 函数语法

```c
void memcpy_off( struct type dest, dword destOffset, byte source[], dword sourceOffset, dword length); // form 1

void memcpy_off( struct type dest, dword destOffset, char source[], dword sourceOffset, dword length); // form 2

void memcpy_off( byte dest[], dword destOffset, struct type source, dword sourceOffset, dword length); // form 3

void memcpy_off( char dest[], dword destOffset, struct type source, dword sourceOffset, dword length); // form 4

void memcpy_off( byte dest[], dword destOffset, byte source[], dword sourceOffset, dword length); // form 5

void memcpy_off( char dest[], dword destOffset, byte source[], dword sourceOffset, dword length); // form 6

void memcpy_off( byte dest[], dword destOffset, char source[], dword sourceOffset, dword length); // form 7

void memcpy_off( char dest[], dword destOffset, char source[], dword sourceOffset, dword length); // form 8
```



#### 函数参数介绍


| 参数              | 含义                                       |
| ----------------- | ------------------------------------------ |
| `dest`       | **(form 1, 2)**: Struct into which the bytes shall be copied.  **(other forms)**: Array into which the bytes shall be copied. |
| `source`     | **(form 3, 4)**: Struct from which the bytes shall be copied.  **(other forms)**: Array from which the bytes shall be copied. |
| `destOffset` | Start offset in the destination struct or array.             |
| `sourceOffset` | Start offset int the source struct or array.                 |
| `length`     | Number of bytes which shall be copied.                       |

