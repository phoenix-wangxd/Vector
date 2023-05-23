# UDS的通过标识符读取数据服务(0x22)




## 一、 介绍通过标识符读取数据(ReadDataByIdentifier)

关于ISO 14229的通过标识符读取数据(ReadDataByIdentifier)一个比较好的介绍文档：

[汽车UDS诊断之通过标识符读取数据服务（0x22）深度剖析](https://blog.csdn.net/qq_40242571/article/details/120756736)


### 1.1 请求报文格式

通过标识符读取数据(ReadDataByIdentifier)服务，请求的报文格式：

![0x22_Request_Message_Definition](.//Picture//ReadDataByIdentifier_0x22//0x22_Request_Message_Definition.png)

数据标识符（Data Identifier）常简称为DID。

### 1.2 数据标识符（Data Identifier）规定

从上面可以看到DID可以自定义，但是如果没有约定，那么不同厂商之间肯定会有大量冲突，所以在ISO 14229-1协议的**C1 DID parameter definitions** 部分规定了DID的分配。下图是该分配表的前面部分：

![0x22_DID_Definitions_01](.//Picture//ReadDataByIdentifier_0x22//0x22_DID_Definitions_01.png)



### 1.3 否定响应（Negative Response Codes）规定

0x22服务支持的否定响应如下：

![0x22_Supported_NegativeResponseCodes](.//Picture//ReadDataByIdentifier_0x22//0x22_Supported_NegativeResponseCodes.png)



## 二、 常用的数据标识符(Data Identifier)

在ISO 14229-1协议的**C1 DID parameter definitions** 部分规定了大量的DID，但是我们常用的并没有那么多，所以这章摘录了常用的DID，然后对其使用进行简单举例。

### 2.1 常用的数据标识符（Data Identifier）

常用的数据标识符（Data Identifier）如下：

![0x22_DID_Definitions_02](.//Picture//ReadDataByIdentifier_0x22//0x22_DID_Definitions_02.png)



### 2.2  0xF1 90: VINDataIdentifier

查看VIN数据：

![0x22_F1_90](.//Picture//ReadDataByIdentifier_0x22//0x22_F1_90.png)

响应举例：

![0x22_F1_90_response](.//Picture//ReadDataByIdentifier_0x22//0x22_F1_90_response.png)



## 三、 其他服务

在ISO 14229-1协议中与**通过标识符读取数据服务(0x22)** 有关的服务有：

- **ReadMemoryByAddress (0x23)** service
- **ReadScalingDataByIdentifier (0x24)** service
- **ReadDataByPeriodicIdentifier (0x2A)** service： 服务端定期发送数据记录值
- **WriteDataByIdentifier (0x2E)** service
- **WriteMemoryByAddress (0x3D)** service

