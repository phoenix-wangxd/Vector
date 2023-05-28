# UDS的安全访问服务(0x27)与CAPL实现自动处理



在实际的诊断中我们要经常和安全访问(Security Access)打交道，为了方便的处理这些问题，写CAPL脚本是一个很好的方案，所以我整理了Vector官方提供的与安全访问(Security Access)有关的函数，并对常用的进行简单说明。

>  本文CAPL函数有关几乎全部摘录自Vector的官方文档，只是做了整理与翻译。



## 一、 介绍安全访问(Security Access)

关于ISO 14229的安全访问（Security Access）一个比较好的介绍文档： [安全访问（ISO14229系列之27服务）](https://blog.csdn.net/weixin_44536482/article/details/93340252)

当客户端连接到服务端（即ECU）时，客户端有一个会话（session）和一个安全级别（security level）。



### 1.1 不同的会话(Session)模式

默认情况下，服务器通过为新客户端分配**默认会话(Default Session)** 来迎接新客户端，在该会话中，只有少数特定服务可以访问，如读取DTC。

但是还有些操作可能涉及到安全或者其他方面的原因，不允许在默认会话(Default Session)中使用，因此如果需要更高的权限，就必须切换到其他的会话中。

在ISO14229中规定了那些服务可以在默认会话中使用，那些不可以在默认会话中使用, 如下：
![14229_Services_allowed_Session_1](.//Picture//14229_Services_allowed_Session_1.png)

如果需要从默认会话(Default Session)切换到其他会话中使用UDS的`10`服务,  我们本文介绍的诊断会话(**extendedDiagnosticSession**) 是ISO 14229规定的必须要提供的会话模式，该会话模式代号通常是`03`。  也即是说如果要切换到该会话，使用命令为`10 03`.



### 1.2 安全访问(Security Access)的工作流程

因为诊断会话(**extendedDiagnosticSession**) 中包含高权限的操作，因此切换到这个会话后，必须要执行**解锁(unlock)** 操作才能进行后续的使用。所谓的**解锁(unlock)** 操作需要使用UDS提供的安全访问(Security Access)服务，也就是UDS的27服务。

0x27 安全访问(Security Access)服务的典型工作流程如下：

1. Client先主动发送一个:   **请求种子(Seed)** 的消息
2. ECU（也就是Server端）收到来自Client的请求后，ECU会发送**种子(Seed)**
3. Client在收到ECU发送过来的**种子(Seed)** 后，客户端对种子(Seed)进行计算，并发送计算后的 **密钥(Key)**
4. ECU在收到**密钥(Key)** 后对其进行校验，如果**密钥(Key)** 是有效的，那么ECU会将自己解锁，并向Client发送积极响应；否则返回否定响应



#### 1.2.1 安全访问(Security Access)的步骤1：客户端发送请求种子(Seed)

Client端发送请求**种子(Seed)** 的消息格式如下：

![14229_0x27_Services_Send_Seed_1](.//Picture//14229_0x27_Services_Send_Seed_1.png)

虽然第二个参数可以是`0x01`、`0x03`、`0x05`、`0x07`等奇数，但是我们最常用的还是`0x01`， 另外`securityAccessDataRecord`通常为空，所以Client最常用的请求Seed的报文为：`27 01`



#### 1.2.2 安全访问(Security Access)的步骤2：ECU发送种子(Seed)

ECU端在收到步骤1的请求消息后，如果请求格式正确，那么会发送积极响应，也就是发送**种子(Seed)** ， 消息格式如下：

![14229_0x27_Services_Send_Seed_2](.//Picture//14229_0x27_Services_Send_Seed_2.png)

第2个参数一般和Client发送请求时的`SubFunction`是一致的，也就是最常用的`0x01`； 

第3个以及后面的参数`securitySeed`通常为2、4个字节。

所以ECU最常用的发送Seed的报文为：`67 01 XX XX`或者`67 01 XX XX XX XX`



#### 1.2.3 安全访问(Security Access)的步骤3：客户端发送密钥(Key)

Client端发送**密钥(Key)** 的消息格式如下：

![14229_0x27_Services_Send_Key_1](.//Picture//14229_0x27_Services_Send_Key_1.png)

虽然第二个参数可以是`0x02`、`0x04`、`0x06`、`0x08`等偶数(必须为发送Seed时使用的`SubFunction`加1)，但是我们最常用的还是`0x02`， 也就是最常用的请求报文为：`27 02 + securityKey`



#### 1.2.4 安全访问(Security Access)的步骤4：ECU发送最终的响应

ECU在收到**密钥(Key)** 后对其进行校验，于是就分为两种情况：

- 情况1： 如果**密钥(Key)** 是有效的，那么ECU会将自己解锁，并向Client发送积极响应。 这种情况下的报文格式比较简单，类似于上面的Table 44。 但是我们最常见的报文还是`67 02`
- 情况2： 如果**密钥(Key)** 是无效的，返回否定响应，格式如下：

![14229_0x27_Services_NRC_1](.//Picture//14229_0x27_Services_NRC_1.png)
![14229_0x27_Services_NRC_2](.//Picture//14229_0x27_Services_NRC_2.png)


### 1.3 不同的安全等级(Security level)

**安全等级(Security level)** 是客户端通过提供安全密钥来解锁服务器内的功能而获得的状态。UDS被设计为允许多达64个安全级别，这些级别是在服务端中设置的布尔标志。

这些安全级别以及它们解锁的内容不是由UDS定义的，而是由ECU制造商定义的。安全级别可以解锁整个服务、子功能或对特定值的访问。例如，写入车辆识别码（VIN）可能需要特定的安全级别，该级别不同于写入最大速度或超越车辆IO所需的安全级别。



下图摘自ISO 14229-1， 描述了SecurityAccess处理的状态图(state chart)：

![14229_0x27_SecurityLevel_1](.//Picture//14229_0x27_SecurityLevel_1.png)

> 上图中的1-10含义，可以参考ISO 14229-1 中的**“Table I.2 — State transitions – disjunctive normal form representation”**



在**默认会话(Default Session)** 中不允许解锁**安全等级(Security level)** 。要获得一些权限，客户端必须首先切换到启用SecurityAccess服务的非默认会话。只有这样，客户端才能执行握手，从而解锁所需的功能。

在ISO 14229中对于安全等级有两个比较重要的描述：

1. 在任何时刻，只有一个安全级别处于活动(active)状态
2. 安全级别(security level)编号是随意的，不同级别之间不意味着有任何关系



## 二、 介绍常用函数

CAPL中与CRC有关的函数如下：

| Functions                        | Short Description                                            |
| :------------------------------- | :----------------------------------------------------------- |
| `diagGenerateKeyFromSeed`        | 生成一个密钥(Key)以在ECU内执行安全的诊断功能                 |
| `diagStartGenerateKeyFromSeed`   | 使用 Seed & Key DLL从种子(Seed)开始生成安全密钥(security key) |
| `TestWaitForGenerateKeyFromSeed` | 使用配置的 Seed & Key DLL从种子(Seed)生成安全密钥(security key) |
| `_Diag_GenerateKeyResult`        | 显示使用`DiagStartGenerateKeyFromSeed`启动的安全密钥计算的结果 |


补充说明：
>Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。



### 2.1 函数:  `diagGenerateKeyFromSeed()`

#### 函数功能描述

创建一个**密钥(key)** 以在设备内执行**安全的诊断功能(secured diagnostic functions)**。
**密钥(key)** 将与设备的**种子(Seed)** 一起定义。
如果计算耗时超过1毫秒，则应使用：`diagStartGenerateKeyFromSeed`、`_Diag_GenerateKeyResult`结合来完成。

#### 函数语法

```c
long diagGenerateKeyFromSeed(byte seedArray[], 
                             dword seedArraySize, 
                             dword securityLevel, 
                             char variant[], 
                             char ipOption[], 
                             byte keyArray[], 
                             dword maxKeyArraySize, 
                             dword& keyActualSizeOut); // form 1

long DiagGenerateKeyFromSeed(char ecuQualifier[], 
                             byte seedArray[] , 
                             dword seedArraySize, 
                             dword securityLevel, 
                             char variant[], 
                             char option[] , 
                             byte keyArray[], 
                             dword maxKeyArraySize, 
                             dword& keyActualSizeOut); // form 2
```

#### 函数参数介绍


| 参数         | 含义                                                       |
| ------------ | ---------------------------------------------------------- |
| `seedArray`      | 用于生成密钥(key)的**种子(Seed)** |
| `seedArraySize`  | `SeedArray` 参数的字节数    |
| `securityLevel`  | 创建密钥(Key)使用的安全级别 |
| `variant`        | 诊断描述(diagnostic description)的变体(Variant)【通俗来讲，是诊断的受体ECU的名称】 |
| `ipOption`       | 官方文档写的太晦涩了，通俗来讲【诊断的受体ECU的代号】 |
| `keyArray`       | 使用自定义的DLL创建的**密钥(Key)** |
| `maxKeyArraySize` | `keyArray`参数允许的最大字节数 |
| `keyActualSizeOut` | `keyArray`参数实际使用的字节数      |
| `ecuQualifier`   | 相应诊断描述的诊断配置对话框中设置的ECU或Target的限定符(Qualifier) |

上述参数中`variant`变量的值可以从CANoe的诊断界面中获取，如下：

![CANoe_Diag_ECU_qualifier_1](.//Picture//CANoe_Diag_ECU_qualifier_1.png)

上述参数中`option`变量的值可以从函数`diagGetCurretnEcu()` 的返回中获取，如下：

```c
on diagResponse *
{
  char ecu[100];
  diagGetCurrentEcu(ecu, elcount(ecu));
  write("Received response from %s", ecu);
}

on key 'a'
{
  // Diagnostic description with ECU qualifier 'FunctionalGroup' configured for Functional Group Requests (FGR)
  diagRequest FunctionalGroup.DefaultSession_Start req1;

  diagSendRequest(req1); // Request is sent to functional group, therefore multiple ECUs may respond
}
```

#### 返回值介绍


| 返回值     | 含义                                                    |
| --------- | ------------------------------------------------------ |
| 0         | If computation was started                             |
| otherwise | 为了进行进一步的错误分析，您可以使用回调函数`_diag_GetError`   |

#### 举例说明

此示例示意性地显示了在CAPL测试模块中使用`DiagGenerateKeyFromSeed`和回调函数。

```c
Variables
{
  ...
  //actual size of Seed and Key Arrays depend on ECU
  byte gSeedArray[2];                       // 如果是4个字节，数组长度为4
  int gSeedArraySize    = 2;                // 如果是4个字节，这个值改为4
  int gSecurityLevel    = 0x20;             // 这个值往往为0x01
  char gVariant[200]    = "Variant1";       // 基本不影响计算结果
  char gOption[200]     = "option";         // 基本不影响计算结果，一般由OEM定义
  byte gKeyArray[255];                      // 如果是4个字节，数组长度为4
  int  gMaxKeyArraySize = 255;              // 如果是4个字节，这个值改为4
  dword gActualSizeOut     = 0;             // 如果是4个字节，这个值改为4
  char gDebugBuffer[2000];
  diagRequest SecurityAccess::SecuritySeed::Request gSeedReq;
  diagResponse SecurityAccess::SecuritySeed::Request gSeedResp;
  diagRequest SecurityAccess::SecurityKey::Send gKeyReq;
  ...
}

//Unlock ECU by calling customer specific SeedKey DLL (e.g. in a CAPL test module)
{
  ...
  //Request seed from ECU
  diagSendRequest(gSeedReq);
  //Wait until request has been sent completely
  testWaitForDiagRequestSent(gSeedReq, 1000);
  //Wait for response and write seed from response parameter to array
  testWaitForDiagResponse(gSeedReq, 1000);
  diagGetLastResponse (gSeedReq, gSeedResp);
  diagGetParameterRaw (gSeedResp, "Seed", gSeedArray, elcount(gSeedArray));
  //Calculate key
  // _Diag_GetError is called when an error occurs
  if( 0 == diagGenerateKeyFromSeed (gSeedArray, gSeedArraySize, gSecurityLevel, gVariant, gOption, gKeyArray, gMaxKeyArraySize, gActualSizeOut))
  {
    //Write result to diagnostic request
    diagSetParameterRaw(gKeyReq, "Key", gKeyArray, gActualSizeOut);
    //Send Key to unlock ECU
    testWaitForDiagRequestSent(gKeyReq, 1000);
  }

//Callback function for error handling (optional)
_diag_GetError (char buffer[])
{
  //called if error in diagGenerateKeyFromSeed occurs
  snprintf(gDebugBuffer,elcount(gDebugBuffer),"%s", buffer);
  write("CALLBACK %s", gDebugBuffer);
}
```





### 2.3 函数:  `diagStartGenerateKeyFromSeed()`

#### 函数功能描述

使用种子(Seed)和密钥(Key)的DLL文件，从**种子(Seed) **开始生成**安全密钥(security key)**。如果无法启动计算，则返回一个错误。

通过调用函数`_Diag_GenerateKeyResult`来显示计算结果。请注意，生成安全密钥(security key)的计算时间可能会超过1ms，这将导致CANoe中的实时事件(real-time event)处理出现问题。因此，计算是在后台进行的，即不能立即获得结果。

在测试节点中，可以使用函数`TestWaitForGenerateKeyFromSeed`。

如果保证计算时间远小于1毫秒，则可以使用`diagGenerateKeyFromSeed`。



#### 函数语法

```c
long diagStartGenerateKeyFromSeed(byte seedArray[], 
                                  dword seedArraySize, 
                                  dword securityLevel); // form 1

long diagStartGenerateKeyFromSeed(byte seedArray[], 
                                  dword seedArraySize, 
                                  dword securityLevel , 
                                  char variant[], 
                                  char option[]); // form 2

long diagStartGenerateKeyFromSeed(char ecuQualifier[], 
                                  byte seedArray[], 
                                  dword seedArraySize, 
                                  dword securityLevel); // form 3

long diagStartGenerateKeyFromSeed(char ecuQualifier[], 
                                  byte seedArray[], 
                                  dword seedArraySize, 
                                  dword securityLevel, 
                                  char variant[], 
                                  char option[]); // from 4
```

#### 函数参数介绍


| 参数            | 含义                                                         |
| --------------- | ------------------------------------------------------------ |
| `seedArray`     | ECU返回的种子(Seed)字节                                      |
| `seedArraySize` | `SeedArray` 参数的字节数                                     |
| `securityLevel` | 创建密钥(Key)使用的安全级别                                  |
| `variant`       | 诊断描述(diagnostic description)中定义的Variant 限定符。在form 1中，该值将是为诊断描述配置的变量 |
| `option`        | 未来该选项可以转发到DLL。如果不存在或传入空字符串，则该值可能从通信状态产生，例如ECU所处的诊断会话。 |
| `ecuQualifier`  | 相应诊断描述的诊断配置对话框中设置的ECU或Target的限定符(Qualifier) |

#### 返回值介绍


| 返回值    | 含义                                                         |
| --------- | ------------------------------------------------------------ |
| 0         | If computation was started                                   |
| otherwise | 详见 `CAPL Functions`--> `Diagnostics` --> `Error Codes` |

#### 举例说明

按下`u`键后解锁ECU：

```c
_Diag_GenerateKeyResult( long result, BYTE computedKey[])
{
  diagRequest SendKeyLevel1 rqSendKey;

  if( 0 != result)
  {
    write( "Error: computing key returned %d", result);
    return;
  }

  // Success, i.e. a key was computed, so send it to the ECU

  rqSendKey.SetParameterRaw("Key", computedKey, elcount( computedKey));
  rqSendKey.SendRequest();
}

On DiagResponse RequestSeedLevel1
{
  BYTE seed[4];
  count = this.GetParameterRaw("Seed", seed, elcount(seed));
  // _Diag_GetError is called when an error occurs
  DiagStartGenerateKeyFromSeed(seed, elcount(seed), 1);
}

_Diag_GetError (char buffer[])
{
  //called if error in DiagGenerateKeyFromSeed occurs
  write("Diagnostic Error: %s", buffer);
}

On key 'u' // unlock
{
  diagRequest RequestSeedLevel1 rqRequestSeed;
  rqRequestSeed.SendRequest();
}
```



### 2.4 函数:  `TestWaitForGenerateKeyFromSeed()`

#### 函数功能描述

使用配置的**Seed&Key** DLL 从种子(seed)生成安全密钥(security key)。对DLL的调用可能需要更多的时间，因此测试模块可能希望等待结果，以免干扰测试的实时执行(real-time execution)。



#### 函数语法

```c
long TestWaitForGenerateKeyFromSeed(byte seedArray[], 
                                    dword seedArraySize, 
                                    dword securityLevel, 
                                    byte keyArray[], 
                                    dword maxKeyArraySize, 
                                    dword& keyArraySizeOut, 
                                    dword appTimeout_ms); // form 1

long TestWaitForGenerateKeyFromSeed(byte seedArray[], 
                                    dword seedArraySize, 
                                    dword securityLevel, 
                                    char variant[], 
                                    char option[], 
                                    byte keyArray[], 
                                    dword maxKeyArraySize, 
                                    dword& keyArraySizeOut, 
                                    dword appTimeout_ms); // form 2

long TestWaitForGenerateKeyFromSeed(char ecuQualifier[], 
                                    byte seedArray[], 
                                    dword seedArraySize, 
                                    dword securityLevel, 
                                    byte keyArray[], 
                                    dword maxKeyArraySize, 
                                    dword& keyArraySizeOut, 
                                    dword appTimeout_ms); // form 3

long TestWaitForGenerateKeyFromSeed(char ecuQualifier[], 
                                    byte seedArray[], 
                                    dword seedArraySize, 
                                    dword securityLevel, 
                                    char variant[], 
                                    char option[], 
                                    byte keyArray[], 
                                    dword maxKeyArraySize, 
                                    dword& keyArraySizeOut, 
                                    dword appTimeout_ms); // form 4
```

#### 函数参数介绍


| 参数              | 含义                                                         |
| ----------------- | ------------------------------------------------------------ |
| `seedArray`       | ECU返回的种子(Seed)                                          |
| `seedArraySize`   | `SeedArray` 参数中的字节数                                   |
| `securityLevel`   | 应解锁哪个安全级别(security level)？                         |
| `variant`         | 指示当前ECU variant的可选参数。在form 1中，该值不必由CAPL程序提供，而是取自诊断描述配置。 |
| `option`          | 可选参数，提供影响密钥计算的附加信息，例如当前激活的诊断会话。在form 1中，该值不必由CAPL程序提供，但如果配置和设置，则从当前ECU状态中获取 |
| `keyArray`        | 计算的结果被写入这个数组                                     |
| `maxKeyArraySize` | DLL返回的`keyArray`参数中允许的最大字节数                    |
| `keyArraySizeOut` | DLL返回的`keyArray`参数实际使用的字节数                      |
| `appTimeout_ms` | 函数等待DLL中的计算函数返回的最长时间(以毫秒为单位);  如果DLL需要更长的时间，则会报告超时。 |
| `ecuQualifier`    | 相应诊断描述的诊断配置对话框中设置的ECU或Target的限定符(Qualifier) |

#### 返回值介绍


| 返回值    | 含义                                         |
| --------- | ------------------------------------------  |
| 1    | 密钥（Key）生成成功             |
| 0    | 超时–DLL没有及时返回密钥 |

#### 举例说明

 `TestWaitForGenerateKeyFromSeed` 函数示例代码:

```c
Testfunction ComputeKeyInExtendedSession( BYTE seed[], BYTE key[])
{
  DWORD keyLenOut;
  keyLenOut = 0;
  DiagSetCurrentSession(0x03); // extended session
  // The key computation may use the current session as optional argument
  TestWaitForGenerateKeyFromSeed( seed, elcount( seed), 1, key, elcount(key), keyLenOut, 1000);
}
```



### 2.5 函数:  `_Diag_GenerateKeyResult()`

#### 函数功能描述

显示使用`DiagStartGenerateKeyFromSeed`函数启动的安全密钥(security key)计算的结果。

#### 函数语法

```c
void _Diag_GenerateKeyResult(long result, 
                             BYTE computedKey[]);
```

#### 函数参数介绍


| 参数      | 含义                                              |
| --------- | ------------------------------------------------ |
| result      | **0**: Success   **other**: Error code         |
| `computedKey` | Seed & Key DLL 返回的密钥Key, 如果有的话 |

#### 举例说明

示例代码见 `DiagStartGenerateKeyFromSeed` 函数的介绍



