# CAPL内置的与CRC有关函数



## 0、 参考文档

本文参考文档
- CRC介绍部分： https://www.geeksforgeeks.org/modulo-2-binary-division/
- 本文函数部分摘录自Vector的官方文档，做了整理与翻译，增加了自己的理解， 并将代码改造的更加优雅实用一些。
- 



## 二、 CRC简介

CRC(Cyclic Redundancy Check)全称为：循环冗余校验，是一种常用的、具有检错、纠错能力的校验码。 用于检测**通信信道(the communication channel)** 中意外变化/错误的方法。


### 2.1  CRC基础知识

CRC使用**生成器多项式(Generator Polynomial) ** 来进行计算，它在发送方和接收方都可用。**生成器多项式(Generator Polynomial) **  是一个极为重要的概念，它有两种不同的表示方法，举例说明：

1. 一个示例生成器多项式 `x3 + x + 1`，   也可以表示为`key`： 二进制 `1011`。
2. 一个示例生成器多项式 `x2 + 1`，   也可以表示为`key`： 二进制  `101`。


为了后续解释方便， 下面先定义`n`与`k`两个变量，其含义如下：

```
n : Number of bits in data to be sent from sender side.  
k : Number of bits in the key obtained from generator polynomial.
```



为了简化说明，后面将所有的**生成器多项式(Generator Polynomial) ** 称之为**多项式(Polynomial)** ， 实际项目中也经常这么表示。



### 2.2  发送方与接收方的处理数据过程

发送方， 根据原始数据和多项式(Polynomial),  也可以称之为密钥(key)生成用于传输的编码数据， 步骤如下：

1. 首先在二进制数据的末尾添加上`k-1`个零来进行扩充， 形成一个新的二进制数
2. 使用**模2二进制除法(modulo-2 binary division)** 将上一步生成的新二进制数据除以 **key**，并存储除法后的余数。
3. 将余数附加在数据的末尾以形成编码数据并发送相同的数据

​	

接收器侧（检查传输中是否引入错误）

1. 再次执行**模2除法(modulo-2 division)** ，如果余数为0，则没有错误。

在本文中，我们将只关注查找余数(remainder) ，即检查字(check word)和码字(code word)。



### 2.2  **模2除法(modulo-2 division)** 

**模2除法(modulo-2 division)** 介绍：

**模2二进制除法(modulo-2 binary division)** 的过程与我们熟悉的十进制除法过程相同。只是我们在这里使用XOR而不是**减法(subtraction)** 。

1. 在每个步骤中，**除数(或数据)** 的一个副本与**被除数(或密钥)** 的k位进行**异或(XORed)**。
2. XOR运算(余数)的结果是(n-1)个比特，在将1个额外的比特拉低以使其变为n个比特长之后，将其用于下一步。
3. 当没有剩余的部分可以下拉时，我们就有了结果。附加在发送方的（n-1）位余数。



原文：

- In each step, a copy of the divisor (or data) is XORed with the k bits of the dividend (or key).
- The result of the XOR operation (remainder) is (n-1) bits, which is used for the next step after 1 extra bit is pulled down to make it n bits long.
- When there are no bits left to pull down, we have a result. The (n-1)-bit remainder which is appended at the sender side.



### 2.3  举例说明

#### 2.3.1.  第一个例子，传输过程中没有错误产生

假设要发送的数据： `100100(0x24)`，  使用到的Key为`1101(0xD)`,  或者说使用到的多项式(polynomial)为： `x3 + x2 + 1`， 计算过程如下：

![CRC_Example_1](.//SimpleFunctions_DataTypes//Picture//CRC_Example_1.png)

从上面可以看到，**余数(remainder)** 为二进制的`001`，因此要发送的编码数据为二进制的 `100100001`。



**对于接收器侧来说：**
接收端接收的数据为： `100100001`， CRC校验部分计算过程如下：

![CRC_Example_2](.//SimpleFunctions_DataTypes//Picture//CRC_Example_2.png)

从上面可以看到，**余数(remainder)** 都是零。因此，接收到的数据没有错误。



#### 2.3.2.  第二个例子，传输过程中有错误产生

这个例子在发送方还是使用前面的例子：

>  假设要发送的数据： `100100`，  使用到的Key为`1101`,  或者说使用到的多项式(polynomial)为： `x3 + x2 + 1`， 
>
> 然后，计算出来要发送的编码数据为二进制的 `100100001`。



在这里，我们构造一个传输过程中出现错误，也就是构造一个错误的接收数字，假设接收端接收到的数据为二进制的`100000001`

在收到这个数字后，CRC校验部分计算过程如下：
![CRC_Example_3](.//SimpleFunctions_DataTypes//Picture//CRC_Example_3.png)

从上面可以看到，由于**余数(remainder)** 不全为零，因此在接收器侧检测到错误。



### 2.4  其他CRC常用概念说明

上面部分介绍的CRC纯理论部分，实际使用时候还有很多新的概念。

#### 2.4.1 `宽度(Width)`
指CRC校验码的宽度，同时也是指多项式的宽度。比如： crc-16的width是16，crc-32的宽度是32

下图摘自在线CRC计算网页， 这里列出了常见的CRC计算模型与其对应的多项式：

![CRC_Example_4](D:\Code\Vector\CANoe\CAPL\SimpleFunctions_DataTypes\Picture\CRC_Example_4.png)

#### 2.4.2 `多项式(Poly)`
指CRC校验的多项式的二进制码去掉最高位。
eg. crc8的Poly：gx=x8+x2+x1+1,二进制码100000111，所以POLY这个参数为：0x07

> 之所以去掉最高位，是因为最高位一直为1，所有进行了省略。  在很多实际使用场合中都省略了最高位。



#### 2.4.3 `初始值(Init)`
是指CRC的寄存器的初始值.
eg.如为0xff,则INIT = 0xff;   如为0x0，则INIT = 0x00

> 如果初始值为(0x00)，那么经过初始值异或运算后，被除数保持不变**(初始值的恒等率)** ； 也就是相当于加不加初始值都没有影响


#### 2.4.4 `输入值反转(RefIN)`
是指需要校验的数据（输入值）二进制位数相反。
eg. 输入值为：10101100，则实际进行校验的值为00110101


#### 2.4.5 `输出值反转(RefOut)`
指输出的校验码二进制位进行反转。
eg. 输出值为：10101100，则实际输出值为00110101


#### 2.4.6 `结果异或值(XorOut)`
指运算出的校验码与结果异或值异或之后，最终最为校验码。
eg. XorOut为0xff,计算的校验码为0x17，则输出校验码为：0xff^0x17




## 三、 常见概念

上述介绍的是通用的CRC概念，但是在汽车领域，还有一些专用的与CRC有关的概念。

### 3.1 E2E概念

首先明确一点，**E2E（end to end）**并非只是在汽车领域应用，任何通信领域都会涉及，只不过是AutoSAR对这一协议/机制做了规范。

E2E，全称End to End，中文即端到端的通信保护，是一种针对安全相关数据，为防止通信链路中可能存在的故障（HW/SW）， 在通信节点之间执行的 一种数据保护协议/机制。其适用于多种网络结构：CAN、 CANFD、FlexRay、Ethernet等。



### 3.2 AUTOSAR Profile 1

**Profile 1** 是 Legacy Profile，仅出于兼容性原因进行维护， 仅仅使用在CP中 。

| Mechanism          | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| Counter            | 4bit (explicitly sent) representing numbers from 0 to 14 incremented on every send request. Both Alive Counter and  Sequence Counter mechanisms are provided by E2E Profile 1, evaluating the same 4 bits. |
| Timeout monitoring | Timeout is determined by E2E Supervision by means of evaluation of the Counter, by a nonblocking read  at the receiver. Timeout is reported by E2E Supervision to the caller by means of the status flags in  E2E_P01CheckStatusType. |
| Data ID            | 16 bit, unique number, included in the CRC calculation.  For dataIdMode equal to 0, 1 or 2, the Data ID is not transmitted, but included in the CRC computation (implicit trans-  mission). For dataIdMode equal to 3:  • the high nibble of high byte of DataID is not used (it  is 0x0), as the DataID is limited to 12 bits,  • the low nibble of high byte of DataID is transmitted explicitly and covered by CRC calculation when  computing the CRC over Data.  • the low byte is not transmitted, but it is included in  the CRC computation as start value (implicit trans-  mission, like for dataIDMode equal to 0, 1 or 2) . |
| CRC                | CRC-8-SAE J1850 - 0x1D (x8 + x4 + x3 + x2 + 1), but with  different start and XOR values (both start value and XOR  value are 0x00).  This CRC is provided by CRC Supervision. Starting with  AUTOSAR R4.0, the SAE8 CRC function of the CRC Supervision uses 0xFF as start value and XOR value. To  compensate a different behavior of the CRC Supervision,  the E2E Supervision applies additional XOR 0xFF operations starting with R4.0, to come up with 0x00 as start  value and XOR value.  Note: This CRC polynomial is different from the CRC-  polynomials used by FlexRay, CAN and LIN. |



E2E Profile 1应使用CRC-8-SAE J1850的多项式，即多项式为：`x8+x4+x3+x2+1`，但`起始值(start value)`和`XOR值`等于 **0x00**。

> `x8+x4+x3+x2+1`即100011101，通常写为`0x1D`,注意这里不是`0x11D`，可能是最高位必然为1，所以省去了。



其他Profile参考： https://blog.csdn.net/qfmzhu/article/details/122334722



## 四、 介绍常用函数

CAPL中与CRC有关的函数如下：

| Functions              | Short Description                              |
| :--------------------- | :--------------------------------------------- |
| `Crc_CalculateCRC8`    | 根据数据计算**CRC8** 的相应校验和(checksum)    |
| `Crc_CalculateCRC8H2F` | 根据数据计算**CRC8H2F** 的相应校验和(checksum) |
| `Crc_CalculateCRC16`   | 根据数据计算**CRC16** 的相应校验和(checksum)   |
| `Crc_CalculateCRC32`   | 根据数据计算**CRC32** 的相应校验和(checksum)   |
| `Crc_CalculateCRC32P4` | 根据数据计算**CRC32P4** 的相应校验和(checksum) |
| `Crc_CalculateCRC64`   | 根据数据计算**CRC64** 的相应校验和(checksum)   |

补充说明：
>Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。


### 4.1 函数:  `Crc_CalculateCRC8()`

这里的CRC8计算方法在**SAEJ1850** 中定义。

#### 函数语法

```c
long Crc_CalculateCRC8 (BYTE* data, 
                        dword dataSize, 
                        dword dataOffset, 
                        dword crcLength, 
                        dword crcStartValue, 
                        dword firstCall, 
                        dword* crcCalculated);
```

#### 函数功能描述

根据数据计算CRC8的相应校验和。CRC值的计算对应于**AUTOSAR Profile 1**。

#### 函数参数介绍


| 参数         | 含义                                                       |
| ------------ | ---------------------------------------------------------- |
| `dest` | 要计算校验和的负载数据(Payload data) |
| `dataSize` | 要计算的数据块(data block)的长度(以字节为单位) |
| `dataOffset` | 用于计算负载数据(payload data)中的CRC的起始索引(Start index) |
| `crcLength` | 计算CRC的数据长度 |
| `crcStartValue` | CRC初始值取决于它是第一次调用还是后续调用。如果**firstCall** 为**1** ，则忽略值。 |
| `firstCall` | 第一次调用或后续调用的标志。可能的值为**0(后续调用)** 或**1(第一次调用)** |
| `crcCalculated` | 计算后的CRC8值 |

#### 返回值介绍

| 返回值 | 含义                                                         |
| ------ | ------------------------------------------------------------ |
| 0      | Successful                                                   |
| -1     | Not successful: CRC length must not be 0                     |
| -2     | Not successful: Offset must not be greater or equal length   |
| -3     | Not successful: Length outside array range                   |
| -4     | Not successful: Summary of Length and offset are outside array range |

#### 举例说明

关于`Crc_CalculateCRC8()`函数说明的示例代码：

```c
// first CALL, Offset '0'
on key 'a'
{
  long retval;
  dword crc;
  byte data[9] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC8(data, elcount (data), 0, elcount (data), 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}

// first CALL, Offset '2', Length - 2
on key 'b'
{
  long retval;
  dword crc;
  byte data[11] = {0xAA ,0xAA,0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC8(data, elcount (data), 2, elcount (data) -2, 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}
```

键盘按下'a'或者'b'输出的结果都是：

```
CRC of data: 0x4B
```



### 4.2 函数:  `Crc_CalculateCRC8H2F()`

这里的`CRC8H2F`指的是： CRC8 0x2F polynomial 

函数作用： 根据数据计算CRC8H2F的相应校验和。CRC值的计算对应于**AUTOSAR Profile 2**。

#### 函数语法

```c
long Crc_CalculateCRC8H2F (BYTE* data, 
                           dword dataSize, 
                           dword dataOffset, 
                           dword crcLength, 
                           dword crcStartValue, 
                           dword firstCall, 
                           dword* crcCalculated);
```

函数的参数与返回值基本上等同于`Crc_CalculateCRC8()` 的说明，这里就不在赘述了。

#### 举例说明

关于`Crc_CalculateCRC8H2F()`函数说明的示例代码：

```c
// first CALL, Offset '0'
on key 'a'
{
  long retval;
  dword crc;
  byte data[9] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC8H2F(data, elcount (data), 0, elcount (data), 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}

// first CALL, Offset '2', Length - 2
on key 'b'
{
  long retval;
  dword crc;
  byte data[11] = {0xAA ,0xAA,0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC8H2F(data, elcount (data), 2, elcount (data) -2, 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}
```

键盘按下'a'或者'b'输出的结果都是：

```
CRC of data: 0xDF
```



### 4.3 函数:  `Crc_CalculateCRC16()`

函数作用： 根据数据计算CRC16的相应校验和。CRC值的计算对应于**AUTOSAR PROFILE_05**和**PROFILE_06**。

#### 函数语法

```c
long Crc_CalculateCRC16 (BYTE* data, 
                         dword dataSize, 
                         dword dataOffset, 
                         dword crcLength, 
                         dword crcStartValue, 
                         dword firstCall, 
                         dword* crcCalculated);
```

函数的参数与返回值基本上等同于`Crc_CalculateCRC8()` 的说明，这里就不在赘述了。

#### 举例说明

关于`Crc_CalculateCRC16()`函数说明的示例代码：

```c
// first CALL, Offset '0'
on key 'a'
{
  long retval;
  dword crc;
  byte data[9] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC16(data, elcount (data), 0, elcount (data), 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}

// first CALL, Offset '2', Length - 2
on key 'b'
{
  long retval;
  dword crc;
  byte data[11] = {0xAA ,0xAA,0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC16(data, elcount (data), 2, elcount (data) -2, 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}
```

键盘按下'a'或者'b'输出的结果都是：

```
CRC of data: 0x29B1
```



### 4.4 函数:  `Crc_CalculateCRC32()`

函数作用： 根据数据计算CRC32的相应校验和。CRC值的计算对应于**IEEE-802.3 CRC32**。

#### 函数语法

```c
long Crc_CalculateCRC32 (BYTE* data, 
                         dword dataSize, 
                         dword dataOffset, 
                         dword crcLength, 
                         dword crcStartValue, 
                         dword firstCall, 
                         dword* crcCalculated);
```

函数的参数与返回值基本上等同于`Crc_CalculateCRC8()` 的说明，这里就不在赘述了。

#### 举例说明

关于`Crc_CalculateCRC32()`函数说明的示例代码：

```c
// first CALL, Offset '0'
on key 'a'
{
  long retval;
  dword crc;
  byte data[9] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC32(data, elcount (data), 0, elcount (data), 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}

// first CALL, Offset '2', Length - 2
on key 'b'
{
  long retval;
  dword crc;
  byte data[11] = {0xAA ,0xAA,0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC32(data, elcount (data), 2, elcount (data) -2, 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}
```

键盘按下'a'或者'b'输出的结果都是：

```
CRC of data: 0xCBF43926
```





### 4.5 函数:  `Crc_CalculateCRC32P4()`

这里的`CRC32P4` 指的是： CRC32 0x1F4ACFB13 polynomial 

函数作用： 根据数据计算CRC32P4的相应校验和。CRC值的计算对应于**AUTOSAR Profile 4**。

#### 函数语法

```c
long Crc_CalculateCRC32P4 (BYTE* data, 
                           dword dataSize, 
                           dword dataOffset, 
                           dword crcLength, 
                           dword crcStartValue, 
                           dword firstCall, 
                           dword* crcCalculated);
```

函数的参数与返回值基本上等同于`Crc_CalculateCRC8()` 的说明，这里就不在赘述了。

#### 举例说明

关于`Crc_CalculateCRC32P4()`函数说明的示例代码：

```c
// first CALL, Offset '0'
on key 'a'
{
  long retval;
  dword crc;
  byte data[9] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC32P4(data, elcount (data), 0, elcount (data), 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}

// first CALL, Offset '2', Length - 2
on key 'b'
{
  long retval;
  dword crc;
  byte data[11] = {0xAA ,0xAA,0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC32P4(data, elcount (data), 2, elcount (data) -2, 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}
```

键盘按下'a'或者'b'输出的结果都是：

```
CRC of data: 0x1697D06A
```



### 4.6 函数:  `Crc_CalculateCRC64()`

函数作用： 根据数据计算CRC64的相应校验和。CRC值的计算对应于 **AUTOSAR Profile 7**。

#### 函数语法

```c
long Crc_CalculateCRC64 (BYTE* data, 
                         dword dataSize, 
                         dword dataOffset, 
                         dword crcLength, 
                         qword crcStartValue, 
                         dword firstCall, 
                         qword* crcCalculated);
```

函数的参数与返回值基本上等同于`Crc_CalculateCRC8()` 的说明，这里就不在赘述了。

#### 举例说明

关于`Crc_CalculateCRC64()`函数说明的示例代码：

```c
// first CALL, Offset '0'
on key 'a'
{
  long retval;
  qword crc;
  byte data[9] = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC64(data, elcount (data), 0, elcount (data), 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}

// first CALL, Offset '2', Length - 2
on key 'b'
{
  long retval;
  qword crc;
  byte data[11] = {0xAA ,0xAA,0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39};

  retval = Crc_CalculateCRC64(data, elcount (data), 2, elcount (data) -2, 0, 1, crc);
  write("CRC of data: 0x%X", crc);
}
```

键盘按下'a'或者'b'输出的结果都是：

```
CRC of data: 0xDF1939FA
```



