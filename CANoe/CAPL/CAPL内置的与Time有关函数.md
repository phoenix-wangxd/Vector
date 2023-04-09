# CAPL内置的时间函数

在CAPL中我们要经常和时间打交道，为了方便的写CAPL脚本，所以我整理了Vector官方提供的与时间有关的函数，并对常用的进行简单说明。

>  本文几乎全部摘录自Vector的官方文档，只是做了整理与翻译。

## 一、CAPL中与时间管理有关的函数

Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。

| Functions                       | Short Description                                            |
| :------------------------------ | :----------------------------------------------------------- |
| `addTimeToMeasurementStartTime` | 计算测量开始的绝对日期/时间加上偏移量                        |
| `cancelTimer`                   | Stops an active timer                                        |
| `convertGPSTimestamp`           | 将GPS时间戳转换为基于UTC的日期和时间信息                     |
| `convertTimestamp`              | 将时间戳转换为单独的部分                                     |
| `convertTimestampNS`            | 将时间戳转换为单独的部分                                     |
| `convertTimestampToNS`          | 将以天、小时、分钟和秒为单位的时间戳转换为纳秒时间戳         |
| `convertUTCDateToUnixTimestamp` | 将给定的UTC时间和日期转换为UNIX时间戳（自1970-01-01以来的秒数） |
| `EnvVarTimeNS`                  | 返回环境变量**envVariable**的时间戳（以纳秒为单位）          |
| `getDrift`                      | Determines the constant deviation when Drift is set.         |
| `getGPSTimeString`              | Copies a printed representation of the GPS time stamp represented as UTC date and time into the supplied character buffer. |
| `getJitterMax`                  | 确定设置抖动(Jitter)时允许偏差的上限                         |
| `getJitterMin`                  | 确定设置抖动(Jitter)时允许偏差的下限                         |
| `getLocalTime`                  | 返回当前日期和时间的详细信息                                 |
| `getLocalTimeString`            | 复制当前日期和时间的打印表示                                 |
| `getMeasurementStartTime`       | 返回有关开始测量的绝对时间的详细信息                         |
| `isTimerActive`                 | 返回值指示特定计时器是否处于活动状态                         |
| `MessageTimeNS`                 | 返回以纳秒为单位的时间戳                                     |
| `setDrift`                      | 为网络节点的计时器设置恒定偏差                               |
| `setJitter`                     | 设置网络节点的计时器的抖动间隔(Jitter interval)              |
| `setTimer`                      | Sets a timer.                                                |
| `setTimerCyclic`                | Sets a cyclical timer.                                       |
| `timeDiff`                      | 消息之间或消息与当前时间之间的时间差（毫秒）                 |
| `timeNow`                       | 提供当前模拟时间[10微秒]                                     |
| `timeNowFloat`                  | 提供当前模拟时间[10微秒]                                     |
| `timeNowInt64`                  | 提供当前模拟时间[纳秒]                                       |
| `timeNowNS`                     | 提供当前模拟时间[纳秒]                                       |
| `timeToElapse`                  | 返回一个值，该值指示在调用计时器上的事件过程之前还要经过多少时间 |



## 二、 获取当前的模拟时间

这里主要介绍 `timeNow()`、 `timeNowFloat()`、 `TimeNowNS()` 三个函数，它们的作用几乎相同，主要是返回值类型不同。

### 2.1 函数:  `timeNow()`

返回当前模拟时间（最长时间：.**2^32*10微秒** = 11小时55分49秒672毫秒96微秒）

#### 函数语法

```c
dword timeNow();
```

#### 函数功能描述

模拟时间(The simulation time)可以与网络接口的硬件结果相关联。这个时间的分辨率取决于所使用的硬件（通常是一毫秒或更好）。

根据硬件配置的不同，模拟时间(The simulation time)可能有两种情况:

- 将与网络接口计算的消息时间相同。
- 消息时间将具有更高的准确性(accuracy)

#### 返回值介绍

模拟时间（单位：10微秒）

#### 举例说明

示例代码：

```c
float x;
x = timeNow()/100000.0; //current time in seconds
```




### 2.2 函数:  `timeNowFloat()`

这个函数与`timeNow()`函数功能几乎完全相同，只有返回值类型有点不同，语法如下：

```c
float timeNowFloat();
```

示例代码：

```c
float x;
x = timeNowFloat()/100000.0; //current time in seconds
```



### 2.3 函数:  `TimeNowNS()`

这个函数与`timeNowFloat()`函数功能相同，提供当前模拟时间，但是以**纳秒**为单位，语法如下：

```c
float TimeNowNS();
```



## 三、获取机器的绝对时间以及测量的绝对时间

这里主要介绍：

1.  `getLocalTime()`、 `getLocalTimeString()`  它们的作用几乎相同，主要是返回值类型不同。
2.  `getMeasurementStartTime()`、 `addTimeToMeasurementStartTime()` 它们通常配合使用，记录测量的绝对时间。




### 3.1. 函数: `getLocalTime()`

#### 函数语法

```c
void getLocalTime(long time[]);
```

#### 函数功能描述

以`long`类型的数组(array)返回当前日期和时间的详细信息。

> **分布式模式(distributed mode)使用的注意事项:**
> 此函数始终返回用户计算机的本地时间。

#### 函数参数介绍

类型为`long`的数组(array)，至少有9个条目。
数组的条目将填充以下信息：

| Index | Information                                                  |
| :---- | :----------------------------------------------------------- |
| 0     | Seconds (0 - 59)                                             |
| 1     | Minutes (0 - 59)                                             |
| 2     | Hours (0 - 23)                                               |
| 3     | Day of month (1 - 31)                                        |
| 4     | Month (0 - 11)                                               |
| 5     | Year (0 - xxx, offset of 1900, e.g. 117 = 2017)              |
| 6     | Day of week (0 - 6, sunday is 0)                             |
| 7     | Day of Year (0 - 365)                                        |
| 8     | Flag for daylight saving time (0 - 1, 1 = daylight saving time) |

### 举例说明

示例代码：

```c
long tm[9];
getLocalTime(tm);
// now tm contains the following entries:
// tm[0] = 3; (seconds)
// tm[1] = 51; (minutes)
// tm[2] = 16; (hours)
// tm[3] = 21; (day of month)
// tm[4] = 7; (month stating with 0)
// tm[5] = 98; (year)
// tm[6] = 5; (weekday)
// tm[7] = 232;(day of year)
// tm[8] = 1; (Summer time)
```



### 3.2 函数:  `getLocalTimeString()`

#### 函数语法

```c
void getLocalTimeString(char timeBuffer[]);
```

#### 函数功能描述

将当前日期和时间的打印表示复制到提供的字符缓冲区中。字符串的格式为`ddd mmm dd hh:mm:ss jjj`（例如"Fri Aug 21 15:22:24 1998"）。

> **分布式模式(distributed mode)使用的注意事项:**
> 此函数始终返回用户计算机的本地时间。



#### 函数参数介绍

| 参数         | 含义                                                       |
| ------------ | ---------------------------------------------------------- |
| `timeBuffer` | 将写入字符串的缓冲区(buffer)。此缓冲区必须至少有26个字符长 |

#### 举例说明

示例代码：

```c
char timeBuffer[64];

getLocalTimeString(timeBuffer);
// now timeBuffer contains for example. "Fri Aug 21 15:22:24 1998"
```



### 3.3 函数:  `getMeasurementStartTime()`

#### 函数语法

```c
long getMeasurementStartTime(long time[]);
```

#### 函数功能描述

返回有关开始测量的绝对时间的详细信息。

> **注意事项:**
> 在CANoe的offline模式下，函数返回日志文件中存储的最早开始时间。

#### 函数参数介绍

只有一个参数`time`， 它的类型为 `long`类型的数组(array) ，至少有8个条目。数组的条目将填充以下信息：

| Index | Information                                     |
| :---- | :---------------------------------------------- |
| 0     | Milliseconds (0 - 999)                          |
| 1     | Seconds (0 - 59)                                |
| 2     | Minutes (0 - 59)                                |
| 3     | Hours (0 - 23)                                  |
| 4     | Day of month (1 - 31)                           |
| 5     | Month (0 - 11)                                  |
| 6     | Year (0 - xxx, offset of 1900, e.g. 117 = 2017) |
| 7     | Day of week (0 - 6, Sunday is 0)                |

#### 返回值介绍

1 if successful, 0 if not (e.g. array to small).


#### 举例说明

示例代码：

```c
on errorframe
{
  long time[8];
  addTimeToMeasurementStartTime(timeNowNS(), time);
  write("ErrorFrame occured on %02d/%02d/%02d %02d:%02d:%02d.%-3d",
  time[5]+1, time[4], time[6]-100, time[3], time[2], time[1], time[0]);
  getMeasurementStartTime(time);
  write("Measurement was started on %02d/%02d/%02d %02d:%02d:%02d.%-3d",
  time[5]+1, time[4], time[6]-100, time[3], time[2], time[1], time[0]);
}

// Output e.g.:
// ErrorFrame occured on 08/15/17 14:39:46.787
// Measurement was started on 08/15/17 14:39:29.547
```



### 3.4 函数:  `addTimeToMeasurementStartTime()`

#### 函数语法

```c
long addTimeMeasurementStartTime(int64 timeSpan, long time[]);
```

#### 函数功能描述

计算测量开始的绝对日期/时间加上偏移量（例如时间戳）。

#### 函数参数介绍

- 参数`timeSpan` : 要添加到测量开始时间的时间，例如测量帧的时间戳。

- 参数`time` : 与 `getMeasurementStartTime()` 函数中的入参完全一致



另外，函数的返回值与示例代码，均可参考 `getMeasurementStartTime()` 函数中的说明。



## 四、时间转换

这里主要介绍 `convertTimestamp()`,  `convertTimestampNS()` 两个函数。

### 4.1. 函数: `convertTimestamp()` 

#### 函数语法

```c
void convertTimestamp(dword timestamp, 
                      dword& days, byte& hours, byte& minutes, 
                      byte& seconds, word& milliSeconds, 
                      word& microSeconds);
```

#### 函数功能描述

将时间戳转(time stamp)换为单独的部分（最长时间：.**2^32*10微秒**=11小时55分49秒672毫秒96微秒）。

#### 函数参数介绍

| 参数         | 含义                                   |
| ------------ | -------------------------------------- |
| timestamp    | 以10微秒为单位的时间戳                 |
| days         | 接收的时间戳的天数                     |
| hours        | 接收的时间戳的小时数（介于0和23之间）  |
| minutes      | 接收的时间戳的分钟数（介于0和59之间）  |
| seconds      | 接收的时间戳的秒数（介于0和59之间）    |
| milliseconds | 接收的时间戳的毫秒数（介于0和999之间） |
| microseconds | 接收的时间戳的微秒（介于0和999之间）   |

示例代码可以参见函数`convertTimestampNS()`中的介绍。



### 4.2. 函数: `convertTimestampNS()`

#### 函数语法

```c
void convertTimestampNS(qword timestamp, 
                        dword& days, byte& hours, byte& minutes, 
                        byte& seconds, word& milliSeconds, 
                        word& microSeconds, word& nanoSeconds);
```

#### 函数功能描述

将时间戳转(time stamp)换为单独的部分。

#### 函数参数介绍

| 参数         | 含义                                   |
| ------------ | -------------------------------------- |
| timestamp    | 以纳秒为单位的时间戳                   |
| days         | 接收的时间戳的天数                     |
| hours        | 接收的时间戳的小时数（介于0和23之间）  |
| minutes      | 接收的时间戳的分钟数（介于0和59之间）  |
| seconds      | 接收的时间戳的秒数（介于0和59之间）    |
| milliseconds | 接收的时间戳的毫秒数（介于0和999之间） |
| microseconds | 接收的时间戳的微秒（介于0和999之间）   |
| nanoseconds  | 接收的时间戳的纳秒（介于0和999之间）   |

#### 举例说明

示例代码：

```C
on envVar EnvGearUp
{
   dword d;
   byte h, m, s;
   word ms, us, ns;
   convertTimestampNS(timeNowNS(), d, h, m, s, ms, us, ns);
   write("Gear up at %d days, %d::%d::%d,%d.%d.%d", d, h, m, s, ms, us, ns);
}
```

