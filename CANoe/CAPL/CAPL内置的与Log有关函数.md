# CAPL内置的与Log有关函数

在CAPL中我们要经常和Log打交道，为了方便的写CAPL脚本，所以我整理了Vector官方提供的与Log有关的函数，并对常用的进行简单说明。

>  本文几乎全部摘录自Vector的官方文档，只是做了整理与翻译。



## 一、CAPL中与Log有关的函数

Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。

| Functions        | Short Description                                            |
| :--------------- | :----------------------------------------------------------- |
| `setLogFileName` | 设置日志文件的名称。                                         |
| `setPostTrigger` | 设置日志的后触发器(posttrigger)                              |
| `setPreTrigger`  | 设置日志记录的预触发器(pretrigger)                           |
| `startLogging`   | 立即启动所有日志记录块，绕过所有日志记录触发器设置           |
| `stopLogging`    | 立即停止所有日志记录块，绕过所有日志记录触发器设置           |
| `trigger`        | 激活/停用**所有的**日志记录(Logging)和触发器(Trigger)块(Blocks)的日志记录触发 |
| `triggerEx`      | 激活/停用**特定的**日志记录(Logging)和触发器(Trigger)块(Blocks)的日志记录触发 |
| `writeToLog`     | 将输出字符串写入ASCII日志文件                                |
| `writeToLogEx`   | 将输出字符串写入ASCII日志文件                                |



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



