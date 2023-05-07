# CAN总线中的位填充(Bit Stuffing)与错误帧(Error Frame)



## 参考文档

以下是本文使用到的参考文档：

- [CAN总线错误解释-简单介绍](https://www.csselectronics.com/pages/can-bus-errors-intro-tutorial)
- [CAN总线错误帧详解](https://www.ednchina.com/technews/12812.html)



## 一、 位填充(Bit Stuffing)介绍

在了解CAN总线中的错误检测之前，首先需要了解什么是**位填充(Bit Stuffing)**。



### 1.1 什么是位填充(Bit Stuffing)

一句话概括： 当CAN节点**发送** 逻辑电平（显性dominant或隐性recessive）相同的五位时，它必须发送一位相反电平。 CAN**接收** 节点会自动删除这个新增的额外位。

下面用图解释什么是位填充(Bit Stuffing)：

![CAN-bus-bit-stuffing](.//Picture//CAN-bus-bit-stuffing.svg)

这个图的说明：

1. 上半部分是发送节点原本需要发送的内容，下半部分是加上**位填充(Bit Stuffing)** 后在CAN网络中真实的CAN报文。
2. 下图中红色的【S】表示的这是一个**填充位(Stuffing Bit)** ， 填充位必然和前面的bit位逻辑相反



关于显性(dominant)和隐性(recessive)的补充说明：

> CAN总线是双绞线，传输数据时，根据两根电缆之间的电压差进行传输，也称为**差分传输**。通过双绞线连接配合差分传输方式能够有效地抑制共模干扰，但是这就带来一个问题，**在没有数据传输时，两条线的电压相同，为隐性信号，逻辑信号为1**。一旦有数据传输，两条线就会出现电压不同的情况，从而**产生电压差**，CAN总线就会表现为**显性信号，逻辑信号为0**。
>
> 参考： https://zhuanlan.zhihu.com/p/447088312



### 1.2 位填充(Bit Stuffing)作用在CAN网络的哪些部分

在CAN标准的“BIT STREAM CODING”章节中规定了**需要填充的部分** :

> The frame segments START OF FRAME, ARBITRATION FIELD, CONTROL FIELD, DATA FIELD and CRC SEQUENCE are coded by the method of bit stuffing. Whenever a transmitter detects five consecutive bits of identical value in the bit stream to be transmitted it automatically inserts a complementary bit in the actual transmitted bit stream.

翻译后：

> 帧段**START OF frame(帧起始)**、**ARBITRATION FIELD(仲裁段)**、**CONTROL FIELD(控制段**)、**DATA FIELD(数据段)**、 **CRC SEQUENCE(CRC段)** 通过比特填充(Bit Stuffing)的方法进行编码。每当发射端在要发送的比特流中检测到具有相同值的五个连续比特时，它自动在实际发送的比特中插入互补比特。



在CAN标准的“BIT STREAM CODING”章节中规定的**不进行填充的部分 ** :

> The remaining bit fields of the DATA FRAME or REMOTE FRAME (CRC DELIMITER, ACK FIELD, and END OF FRAME) are of fixed form and not stuffed. The ERROR FRAME and the OVERLOAD FRAME are of fixed form as well and not coded by the method of bit stuffing.

翻译后：

> 数据帧或远程帧的剩余位字段【**CRC DELIMITER(CRC界定符)**、**ACK FIELD(ACK段)**、 **END of FRAME(帧结束)** 】为固定形式，不填充。 **ERROR FRAME(错误帧)** 、  **OVERLOAD FRAME(过载帧)** 也是固定形式的，并且不通过比特填充的方法进行编码。



为了便于大家对比这些帧段的位置，附上Vector制作的图一张：

![Data_Frame_in_Standard_and_Extended_Format](.//Picture//CAN_Framing_Data_Frame_in_Standard_and_Extended_Format.png)



### 1.3 位填充(Bit Stuffing)的目的是什么?

网上有很多描述，但是都过于复杂或者抽象， 我自己总结的简而言之的概括：

CAN协议中规定这个位填充(Bit Stuffing) 目的是：处理比如CAN消息中连续多个Byte的0，影响CAN网络中对于帧起始位置的判断。



## 二、 错误帧(Error Frame)介绍


### 2.1 错误帧(Error Frame)的帧结构

在CAN标准中规定的

> The ERROR FRAME consists of two different fields. The first field is given by the superposition of ERROR FLAGs contributed from different stations. The following second field is the ERROR DELIMITER.

翻译：

> ERROR FRAME(错误帧) 由两个不同的字段组成。第一个字段是由不同站点贡献的**错误标志(ERROR FLAG)** 的叠加给出的。下面的第二个字段是**错误界定符(ERROR DELIMITER)** 。



Vector制作了Error Frame形象化的结构图：

![CAN_Framing_Error_Frame](.//Picture//CAN_Framing_Error_Frame.png)

这部分看上比较简单， 但是很重要，我们需要先了解一部分基础知识：

1. 第一段错误标志，也就是上图中的(primary) Error Flag,  它通常被称之为：  **'primary' Active Error Flag**  ，之所以叫“Active”是因为它是连续的6个显性比特。 同时它一般来自于首先发现错误的节点（'discovering' node)
2. 第二段错误标志，也就是上图中的(secondary) Error Flag,   它通常被称之为： **'secondary' Active Error Flag(s)** ， 这部分比较复杂由0~6个显性比特位组成。 同时它一般来自于后续“反应过来的”节点（'reacting' node）。这一部分有时候也叫做“回显标志”
3. 错误界定符(Error Delimiter)：8个连续的隐性位。



### 2.2 举例说明错误帧(Error Frame)的帧结构

由于错误帧的(secondary) Error Flag的长度不确定，所以我们举3个例子说明什么情况下长度应该是多少。



#### 2.2.1 示例 1：错误标志(Error Flag)有6位

这是最简单的例子： 在这里，所有CAN节点同时发现CAN消息中存在错误，并同时抛出其错误标志。
结果是错误标志**全部重叠(all overlap)** ，并且显性比特的总序列(the total sequence of dominant bits)总共持续6个比特。在这种情况下，所有CAN节点都将认为自己是“发现(discovering)”CAN节点。

![CAN-bus-error-frame-12-bit-flag-example-1](.//Picture//CAN-bus-error-frame-12-bit-flag-example-1.svg)

> 这种类型的同时发现在实践中不太常见。然而，例如，它可能是由于Form 错误（例如CRC分隔符是显性的而不是隐性的），或者如果CAN发送器在写入CRC字段期间遇到位错误。



#### 2.2.2 示例 2：错误标志(Error Flag)有12位

在这里，CAN节点1发送了一个**显性比特(dominant bit)**，但将其读取为**隐性比特(recessive bit)**，这意味着它发现了一个**比特错误(Bit Error)**。它立即发送一个由6个显性比特组成的序列。
其他节点只有在读取了全部6个比特之后才发现**比特填充错误(Bit Stuffing Error)**，之后它们同时抛出它们的错误标志，从而产生6个显性比特的后续序列，即总共12个。


![CAN-bus-error-frame-6-bit-flag-example-2](.//Picture//CAN-bus-error-frame-6-bit-flag-example-2.svg)

#### 2.2.3 示例 3：错误标志(Error Flag)有9位

这里，CAN节点1先已经发送完了3个显性比特的序列，但是回读的时候在发现了一个比特错误(Bit Error)【就是下图中最上面的那个Bit Error】， 于是立马开始发送连续6个显性比特(dominant bits)以说明出现了错误。

一旦**主活动错误标志(the primary Active Error Flag)**进行到一半，节点2和3就识别出比特填充错误(Bit Stuffing Error)【原因是：在3个初始的显性比特后面跟着另外3个显性比特】，因此它们开始抛出它们的错误标志。结果是，来自错误标志的显性比特序列变为9比特长。


![CAN-bus-error-frame-9-bit-flag-example-3](.//Picture//CAN-bus-error-frame-9-bit-flag-example-3.svg)






### 2.3 错误帧(Error Frame)类型【错误检测(Error Detection)】

在CAN标准中定义了5种类型的错误：

- **BIT ERROR**:  位错误
- **STUFF ERROR**:  填充错误
- **CRC ERROR**:  CRC错误
- **FORM ERROR**:  格式错误
- **ACKNOWLEDGMENT ERROR**:  ACK错误

通过这5中错误类型，我们可以进行**错误检测(Error Detection)**， 下面进行详细介绍。


#### 2.3.1 **BIT ERROR**:  位错误

CAN标准原始的定义:
> A unit that is sending a bit on the bus also monitors the bus. A BIT ERROR has to be detected at that bit time, when the bit value that is monitored is different from the bit value that is sent. An exception is the sending of a ’recessive’ bit during the stuffed bit stream of the ARBITRATION FIELD or during the ACK SLOT. Then no BIT ERROR occurs when a ’dominant’ bit is monitored. A TRANSMITTER sending a PASSIVE ERROR FLAG and detecting a ’dominant’ bit does not interpret this as a BIT ERROR.

节点将自己发送到总线上的电平与同时从总线上回读到的电平进行比较，如果发现二者不一致，那么这个节点就会检测出一个位错误(BIT ERROR)。

实际上所谓“发出的电平与从总线上回读的电平不一致”，指的就是**节点向总线发出隐性位，却从总线上回读到显性位** 或者**节点向总线发出显性位，却从总线上回读到隐性位** 这两种情况。

有三种例外情况不属于位错误(BIT ERROR)：
- 在仲裁段(ARBITRATION FIELD)，节点向总线发送隐性位却回读到显性位，不认为是位错误，这种情况表示该节点仲裁失败；这属于ID仲裁区，此种情况属于仲裁失败，优先级较低而已，不算错误。
- 在ACK SLOT段，节点向总线发送隐性位却回读到显性位，不认为是位错误； 这种情况表示，该节点当前发送的这一帧报文至少被一个其它节点正确接收；此种情况一般是因为总线上只有一个节点，没有其他节点返回ACK，既然只有自己，也不会影响到别人，就没有必要算作错误了。
- 该节点发送被动错误标志(PASSIVE ERROR FLAG)，节点Node_A向总线发送连续六个隐性位（被动错误标志）却回读到显性位，不认为是位错误。因为被动错误标志是六个连续的隐性位，所以在总线上按照线与机制，有可能这六个连续隐性位被其它节点发送的显性电平“吃掉”；被动错误的发言权小于主动错误。



#### 2.3.2 **STUFF ERROR**:  填充错误

CAN标准原始的定义:
>  A STUFF ERROR has to be detected at the bit time of the 6th consecutive equal bit level in a message field that should be coded by the method of bit stuffing.

CAN协议要求出现5个连续相同电平之后，需要插入一个翻转电压，以避免时钟错误。

在需要执行位填充原则的帧段（数据帧遥控帧的SOF~CRC序列），检测到连续六个同性位，则检测到一个填充错误。




#### 2.3.3 **CRC ERROR**:  CRC错误

CAN标准原始的定义:
>  The CRC sequence consists of the result of the CRC calculation by the transmitter. The receivers calculate the CRC in the same way as the transmitter. A CRC ERROR has to be detected, if the calculated result is not the same as that received in the CRC sequence.

发送节点Node_A在发送数据帧或者遥控帧时，会计算出该帧报文的CRC序列。接收节点Node_B在接收报文时也会执行相同的CRC算法，如果接收节点Node_B计算出的CRC序列值与发送节点Node_A发来的CRC序列值不一致，那么接收节点就检测到一个CRC错误。



#### 2.3.4 **FORM ERROR**:  格式错误

CAN标准原始的定义:
>  A FORM ERROR has to be detected when a fixed-form bit field contains one or more illegal bits.

在一帧报文发送时，如果在必须发送预定值的区域内检测到了非法值，那么就检测到一个格式错误。
CAN报文中，有预定值的区域包括：

- 数据帧和遥控帧的CRC界定符、ACK界定符、EOF；
- 错误帧界定符
- 过载帧界定符



#### 2.3.5 **ACKNOWLEDGMENT ERROR**:  ACK错误

CAN标准原始的定义:
>  An ACKNOWLEDGMENT ERROR has to be detected by a transmitter whenever it does not monitor a ’dominant’ bit during the ACK SLOT.

按照CAN协议的规定，在一帧报文（数据帧或者遥控帧）发出之后，如果接收节点Node_B成功接收了该帧报文，那么接收节点Node_B就要在该帧报文ACK槽对应的时间段内向总线上发送一个显性位来应答发送节点Node_A。这样发送节点Node_A就会在ACK槽时间段内从总线上回读到一个显性位。因此：

当发送节点Node_A在ACK SLOT时间段内没有回读到显性位，那么发送节点Node_A就会检测到一个ACK应答错误。这表示没有一个节点成功接收该帧报文。



## 三、 CAN错误计数器【错误界定(Error Confinement)】

通过上面的方式，CAN可以检测出一部分错误，CAN的这些错误处理有助于销毁错误的消息，并使CAN节点能够重试错误消息的发送。
这确保了短暂的局部干扰（例如来自噪声）不会导致无效/丢失的数据。作为替代，发送端会尝试重新发送消息。如果它赢得了仲裁（并且没有错误），则消息将被成功发送。
然而，如果错误是由于传输节点中的系统故障(systematic malfunction)引起的呢？ 这可能会引发发送/销毁相同消息的无休止循环，从而干扰CAN总线。

这就是CAN**节点状态(node states)** 和**错误计数器(error counters)** 的作用所在, 下面进行详细的介绍。

### 3.1 CAN节点的节点状态(node states)

按照CAN协议的规定，CAN总线上的节点始终处于以下三种状态之一。

- **主动错误(Error Active)状态**
- **被动错误(Error Passive)状态**
- **总线关闭(Bus Off)状态**



为什么要设置这三种状态?
> 简而言之，CAN错误跟踪(error tracking)的目的是通过适当地减少有问题的CAN节点的权限来限制错误。



#### 3.1.1 CAN节点的节点状态(node states)的解释

**1）主动错误(Error Active)状态**

这是每个CAN节点的**默认状态**，节点处于主动错误(Error Active)状态可以正常通信；

处于主动错误状态的节点（可能是接收节点也可能是发送节点）在检测出错误时，发出**主动错误标志(Active Error Flags)**。

> **主动错误标志(Active Error Flags)**：6个连续的显性位；



**2）被动错误(Error Passive)状态**

节点处于被动错误(Error Passive)状态也可以正常通信；

处于被动错误状态的节点（可能是接收节点也可能是发送节点）在检测出错误时，但是会发出**被动错误标志(Passive Error Flags)**。

>  **被动错误标志(Passive Error Flags)**：6个连续的隐性位；



此外，CAN节点现在除了3位的间歇时间外，还必须等待额外的8位（也称为挂起传输时间Suspend Transmission Time），然后才能恢复数据传输（以允许其他CAN节点控制总线）



**3）总线关闭(Bus Off)状态**

如果节点处于总线关闭(Bus Off)状态，在这种状态下，CAN节点将自身与CAN总线断开，并且不能再传输数据或发出错误标志

处于总线关闭状态的节点，只能一直等待，在满足一定条件的时候，再次进入到主动错误(Error Active)状态。



#### 3.1.2 CAN节点的节点状态(node states)之间的切换

每个CAN控制器都会跟踪自己的状态并采取相应的行动。CAN节点根据其错误计数器（error counters）的值改变状态。具体而言，每个CAN节点都会跟踪传输错误计数器（Transmit Error Counter, TEC）和接收错误计数器（Receive Error Counter, REC）：

- 如果REC或TEC超过127，则CAN节点进入错误被动(Error Passive) 状态
- 如果TEC超过255，则CAN节点进入总线断开(Bus Off) 状态



在三种不同的状态之间相互切换如下图：

![CAN-error-handling-states-error-active-passive-bus-off](.//Picture//CAN-error-handling-states-error-active-passive-bus-off.svg)

> CAN控制器内置两个错误计数器：`[TEC]Tranmit Error Counter` 与    `[REC]Receive Error Counter`



### 3.2 错误计数器(error counters)的更改

在我们进入如何增加/减少错误计数器(error counters)的逻辑之前，让我们重新访问CAN错误帧以及主要/次要错误标志(primary/secondary error flags)。

从CAN错误帧图中可以明显看出，在其自己的6个显性比特序列之后观察到显性比特的CAN节点将知道其引发了**主要错误标志(primary error flag)**。在这种情况下，我们可以将此can节点称为错误的“发现者”。

起初，CAN节点可以反复发现错误，并通过在其他节点之前抛出错误标志来迅速做出反应，这听起来可能是积极的。然而，在实践中，发现者(the discoverer)通常也是导致错误的罪魁祸首，因此根据概述，它会受到更严厉的惩罚。



![CAN-bus-error-counter-transmit-receive-TEC-REC](.//Picture//CAN-bus-error-counter-transmit-receive-TEC-REC.svg)
