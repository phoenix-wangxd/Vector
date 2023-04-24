# CAPL中有关Message事件



## 一、 背景说明

为了更方便的介绍，所以我们需要一个前期准备工作。 首先需要建立一个简单的数据库文件（DBC文件），信息如下：

### 1.1. 节点（Node）
整个DBC文件中只有一个节点，节点名称为`Node1` .



### 1.2. 报文（Message）

在上述的`Node1` 节点中有两条报文：

| Message ID | Message名 | 类型    | 长度  |
| ---------- | --------- | ------- | ----- |
| 0x111      | Msg1      | 标准CAN | 8Byte |
| 0x112      | Msg2      | 标准CAN | 8Byte |

Msg1 与 Msg2 的属性相同，都为：

| 属性名称               | 对应的值 |
| ---------------------- | -------- |
| `GenMsgCycleTime`      | 1000     |
| `GenMsgCycleTimeFast`  | 0        |
| `GenMsgDelayTime`      | 0        |
| `GenMsgILSupport`      | Yes      |
| `GenMsgNrOfRepetition` | 0        |
| `GenMsgSendType`       | Cyclic   |
| `GenMsgStartDelayTime` | 0        |
| `NmMessage`            | No       |



### 1.2. 信号（Signal）

总共有4个Signal，信息如下：

| 信号名 | 所属Message名 | 开始比特(StartBit) | 信号长度(Bit) | 值类型   | 初始值 |
| ------ | ------------- | ------------------ | ------------- | -------- | ------ |
| Sig1_1 | Msg1          | 0                  | 8             | Unsigned | 0      |
| Sig1_2 | Msg1          | 8                  | 1             | Unsigned | 0      |
| Sig2_1 | Msg2          | 0                  | 8             | Unsigned | 0      |
| Sig2_2 | Msg2          | 8                  | 1             | Unsigned | 0      |






## 二、  修改Signal

### 2.1. 使用`this` 的错误场景1

#### 2.1.1. 错误的示例代码
错误的示例代码-使用`this`, 示例代码：

```c
on message Msg1
{
  write("Before Sig1_1 Value: 0x%x", this.Sig1_1);
  this.Sig1_1 += 1;
  write("After  Sig1_1 Value: 0x%x", this.Sig1_1);
}
```

编译后有告警，告警信息如下：

![Vector_CAPL_OnMessage_Example_1](.//Picture//Vector_CAPL_OnMessage_Example_1.png)

如果尝试运行代码，可以看到信息：

![Vector_CAPL_OnMessage_Example_2](.//Picture//Vector_CAPL_OnMessage_Example_2.png)


#### 2.1.2. 更改后的代码

示例代码：

```c
on message Msg1
{
  write("Before Sig1_1 Value: 0x%x", this.Sig1_1);
  $Msg1::Sig1_1 += 1;
  write("After  Sig1_1 Value: 0x%x", this.Sig1_1);
}
```

上述代码编译不会产生告警，运行信息如下:

![Vector_CAPL_OnMessage_Example_3](.//Picture//Vector_CAPL_OnMessage_Example_3.png)



### 2.2.  使用`this` 的错误场景2

#### 2.2.1. 错误的示例代码

示例代码：

```c
on message Msg1
{
  write("Before Sig1_1 Value: 0x%.2x", this.Sig1_1);
  Byte0_Add_Random_Numb(this);
  write("After  Sig1_1 Value: 0x%.2x", this.Sig1_1);
}

void Byte0_Add_Random_Numb(message * msg){
  dword x;
  x = random(20);   // generate random number in the interval [0;20)
  write("byte_0 is: %d, generate random number is: %lu", msg.byte(0), x);
  msg.byte(0)  += x; 
}
```

编译并没有报任何错误与告警，输出的内容如下：

![Vector_CAPL_OnMessage_Example_4](.//Picture//Vector_CAPL_OnMessage_Example_4.png)




#### 2.2.2. 更改后的代码

更改后的代码如下：

```c
on message Msg1
{
  write("Before Sig1_1 Value: 0x%.2x", this.Sig1_1);
  $Msg1::Sig1_1 = Byte0_Add_Random_Numb(this);
  write("After  Sig1_1 Value: 0x%.2x", this.Sig1_1);
}

byte Byte0_Add_Random_Numb(message * msg){
  dword x;
  x = random(20);   // generate random number in the interval [0;20)
  write("byte_0 is: %d, generate random number is: %lu", msg.byte(0), x);
  return msg.byte(0) + x;
}
```

编译后运行，为了更加直观的说明问题，我将Sig1_1 的变化图形画出来了，如下：

![Vector_CAPL_OnMessage_Example_5](.//Picture//Vector_CAPL_OnMessage_Example_5.png)

最高点跳下来是因为越界了，1个Byte最大可以到255。
