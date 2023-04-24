# CAPL内置的与结构化字节有关函数

在CAPL中我们要经常和结构化字节打交道，为了方便的写CAPL脚本，所以我整理了Vector官方提供的与结构化字节有关的函数，并对常用的进行简单说明。

>  本文几乎全部摘录自Vector的官方文档，只是做了整理与翻译。



## 一、CAPL中与结构化字节有关的函数

Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。

| Functions    | Short Description                          |
| :----------- | :----------------------------------------- |
| `memcmp`     | 比较参数的字节数据                         |
| `memcpy`     | 将字节从源复制到目标                       |
| `memcpy_h2n` | 将字节从结构复制到数组中                   |
| `memcpy_n2h` | 用数组中的字节填充结构                     |
| `memcpy_off` | 将字节从源复制到目标，并给出目标起始偏移量 |



## 二、 比较多个字节

### 2.1 函数:  `memcmp()`

#### 函数语法

```c
int memcmp(struct * dest, byte source[]); // form 1

int memcmp(byte dest[], struct * source); // form 2

int memcmp(struct * dest, struct * source); // form 3

int memcmp(byte dest[], byte source[], dword size); // form 4
```

#### 函数功能描述

Compares the bytes of the parameters. In form 3, both structs must have the same type.

#### 函数参数介绍


| 参数         | 含义                                                       |
| ------------ | ---------------------------------------------------------- |
| dest   | A struct                                         |
| source | Another struct                                   |
| size   | Size of the arrays (number of bytes to compare). |

#### 返回值介绍

0 if the bytes are equal; a value different from 0 if they are unequal

#### 举例说明

`DWORD` 就是 Double Word， 每个word为2个字节的长度，DWORD 双字即为4个字节，每个字节是8位，共32位。

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

输出结果：

```
Data represents the number: Little Endian is used.
```



## 三、 拷贝字节

### 3.1 函数:  `memcmp()`

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

#### 函数功能描述

Copies bytes from a source to a destination. In form 5, both structs must have the same type. In other forms with structs, the arrays must be large enough to contain the struct data. In form 17 and 18, the payload size and the struct size must be identical.



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

输出结果：

```
Bytes as dword: 0x03020100
dword as bytes: 0x78 0x56 0x34 0x12
```



### 3.2 函数:  `memcpy_h2n()`

#### 函数语法

```c
void memcpy_h2n(byte dest[], struct source); // form 1

void memcpy_h2n(byte dest[], int offset, struct source); // form 2
```

#### 函数功能描述

Copies the bytes from the struct into the array, and translates the byte order of the elements from little-endian to big-endian (h2n stands for "host to network").

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
  memcpy_n2h(dwordWrapper, data);
  write("Bytes as dword: %0#10lx", dwordWrapper.dw);
  
  dwordWrapper.dw = 0x12345678;
  memcpy_h2n(data, dwordWrapper);
  write("dword as bytes: %#lx %#lx %#lx %#lx", data[0], data[1], data[2], data[3]);
}
```

输出结果：

```
Bytes as dword: 0x00010203
dword as bytes: 0x12 0x34 0x56 0x78
```



### 3.3 函数:  `memcpy_n2h()`

#### 函数语法

```c
void memcpy_n2h(struct dest, byte source[]); // form 1

void memcpy_n2h(struct dest, byte source[], int offset); // form 2
```

#### 函数功能描述

Fills the struct with bytes from the array, and translates the byte order of the elements from big-endian to little-endian (n2h stands for "network to host").

#### 函数参数介绍


| 参数              | 含义                                       |
| ----------------- | ------------------------------------------ |
| `source`          | Struct whose bytes shall be copied         |
| `dest`            | Array into which the bytes shall be copied |
| `offset (form 2)` | Offset into the array                      |



#### 举例说明

示例代码参见`memcpy_h2n`部分的说明。



### 3.4 函数:  `memcpy_off()`

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

#### 函数功能描述

Copies bytes from a source to destination, giving a destination start offset. The size of the destination must be at least destOffset + length.

#### 函数参数介绍


| 参数              | 含义                                       |
| ----------------- | ------------------------------------------ |
| `dest`       | (form 1, 2): Struct into which the bytes shall be copied. (other forms): Array into which the bytes shall be copied. |
| `source`     | (form 3, 4): Struct from which the bytes shall be copied. (other forms): Array from which the bytes shall be copied. |
| `destOffset` | Start offset in the destination struct or array.             |
| `sourceOffset` | Start offset int the source struct or array.                 |
| `length`     | Number of bytes which shall be copied.                       |

