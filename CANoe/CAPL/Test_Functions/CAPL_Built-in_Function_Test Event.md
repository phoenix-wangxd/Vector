# CAPL内置的与Test 事件有关函数



## 0、 参考文档

本文参考文档
- 本文函数部分摘录自Vector的官方文档，做了整理与翻译，增加了自己的理解， 并将代码改造的更加优雅实用一些。



## 一、说明

待补充



## 三、 介绍与TestReportAdd有关的函数

CAPL中与文件有关的函数如下：

| Functions              | Short Description                        |
| :--------------------- | :--------------------------------------- |
| `TestReportAddMiscInfoBlock` | 为测试报告中的附加信息对生成一个新的信息块 |
| `TestReportAddMiscInfo` | 在测试报告中新增一条附加信息对 |
| `TestReportAddEngineerInfo` | 在测试报告的`TestEngineer`区域中添加测试工程师信息 |
| `TestReportAddSetupInfo` | 在测试报告的`TestSetUp`区域中添加对应信息 |
| `TestReportAddSUTInfo` | 在测试报告的`device (SUT) `区域中添加SUT信息 |
| `TestReportAddExternalRef` | 向报告添加外部引用（URL、DOORS或eASEE链接） |
| `TestReportAddImage` | 在测试报告添加图片 |
| `TestReportAddWindowCapture` | 在测试报告中添加窗口的截屏 |



###  3.1.  `TestReportAdd*` 举例说明

和`TestReportAdd` 有关的函数：

```c
MainTest()
{
  ...
  // add information to SUT information table
  TestReportAddSUTInfo("Serial No.", "A012345BC");
  TestReportAddSUTInfo("Manufactured", "2003-10-02");
  // add information to test engineer information table
  TestReportAddEngineerInfo("Test Engineer", "S. Grey");
  TestReportAddEngineerInfo("Stuff No.", "12345");
  // add information to test setup information table
  TestReportAddSetupInfo("Tester", "TH12");
  ...
  // add html line to report, e.g. a link to the homepage
  TestReportAddExtendedInfo("html", "<A HREF=\"http://www.vector.com\">Homepage</A>");
  ...
}

testcase Configure_Powermanagement()
{
  ...
  // add info block to test case in report
  TestReportAddMiscInfoBlock("Used Test Parameters");
  TestReportAddMiscInfo("Max. voltage", "19.5 V");
  TestReportAddMiscInfo("Max. current", "560 mA");
  ...
  // add image to report, scale down to reasonable size
  TestReportAddImage("Oscilloscope Snapshot", "osc_01.png", "400px", "");
}
```







## 四、 新增功能



### 4.1 函数:  `TestWaitForSignalChange()`等

等待信号中值发生改变的事件

注意： 该函数在CANoe15及后才可使用

#### 函数语法

```c
long TestWaitForSignalChange(Signal aSignal, dword aTimeout);
```

#### 函数功能描述

Waits for an event from a signal which value is changed.

#### 函数参数介绍


| 参数       | 含义                                             |
| ---------- | ------------------------------------------------ |
| `aSignal`  | 待查询信号 Signal to be queried                  |
| `aTimeout` | 最长等待时间（毫秒） Maximum waiting time in ms. |

#### 函数返回值介绍


| 参数 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| `-2` | 信号无效 Signal is not valid                                 |
| `-1` | 一般错误 General error                                       |
| `0`  | 等待状态因超时而退出 Wait state is exited due to a timeout   |
| `1`  | 由于条件满足而退出等待状态  Wait state is exited due to condition fulfillment |

####  举例说明

示例代码如下：

```c
// waits 1000ms for change of signal "Velocity"
long result;
result = TestWaitForSignalChange(Node_SUT::Velocity, 1000);
```



### 4.2 函数:  `TestWaitForSignalUpdate()`等

等待信号更新而产生的事件

注意： 该函数在CANoe15及后才可使用

#### 函数语法

```c
long TestWaitForSignalUpdate (Signal aSignal, dword aTimeout);
```

#### 函数功能描述

Waits for an event from a signal.

#### 函数参数介绍


| 参数       | 含义                                             |
| ---------- | ------------------------------------------------ |
| `aSignal`  | 待查询信号 Signal to be queried                  |
| `aTimeout` | 最长等待时间（毫秒） Maximum waiting time in ms. |

#### 函数返回值介绍


| 参数 | 含义                                                         |
| ---- | ------------------------------------------------------------ |
| `-2` | 信号无效 Signal is not valid                                 |
| `-1` | 一般错误 General error                                       |
| `0`  | 等待状态因超时而退出 Wait state is exited due to a timeout   |
| `1`  | 由于条件满足而退出等待状态  Wait state is exited due to condition fulfillment |

####  举例说明

示例代码如下：

```c
// waits 1000ms for update of signal "Velocity"
long result;
result = TestWaitForSignalUpdate(Node_SUT::Velocity, 1000);
```

