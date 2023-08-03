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



## 二、 Write格式表达式Write Format Expressions

Windows和Linux之间的合法格式表达式和差异列表：

| CAPL Type                                                    | Display Description                                          | Format Windows | Format Linux |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :------------- | :----------- |
| int                                                          | signed display                                               | %d             | %d           |
| long                                                         | signed display                                               | %ld            | %d           |
| int64                                                        | signed display                                               | %I64d or %lld  | %ld or %lld  |
| byte/word                                                    | unsigned display                                             | %u             | %u           |
| dword                                                        | unsigned display                                             | %lu            | %u           |
| qword                                                        | unsigned display                                             | %I64u or %llu  | %lu or %llu  |
| byte/word/int                                                | hexadecimal display                                          | %x             | %x           |
| dword/long                                                   | hexadecimal display                                          | %lx            | %x           |
| qword/int64                                                  | hexadecimal display                                          | %I64x or %llx  | %lx or %llx  |
| byte/word/int                                                | hexadecimal display (upper case)                             | %X             | %X           |
| dword/long                                                   | hexadecimal display (upper case)                             | %lX            | %X           |
| qword/int64                                                  | hexadecimal display (upper case)                             | %I64X or %llX  | %lX or %llX  |
| byte/word/int                                                | octal display                                                | %o             | %o           |
| dword/long                                                   | octal display                                                | %lo            | %o           |
| qword/int64                                                  | octal display                                                | %I64o or %llo  | %lo or %llo  |
| float/double                                                 | floating point display                                       | %g or %f       | %g or %f     |
| character display                                            | %c                                                           | %c             |              |
| string display                                               | %s                                                           | %s             |              |
| display of %-character                                       | %%                                                           | %%             |              |
| dword                                                        | 32-bit pointer (without implicit pointer format 0xABABABAB)  | %p             | %08x         |
| 32-bit pointer (with implicit pointer format 0xABABABAB)     | %#p                                                          | %p             |              |
| qword                                                        | 64-bit pointer (without implicit pointer format 0xABABABABABABABAB) | %I64p          | %016lx       |
| 64-bit pointer (with implicit pointer format 0xABABABABABABABAB) | %#I64p                                                       | %p             |              |



注意点：

> %n格式无效，一定不能使用。



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



## 三、 写入日志文件

这里主要介绍 `writeToLog()`、 `writeToLogEx()`两个函数, 这两个函数的作用都是写一些字符串到日志文件中。



### 3.1. 函数: `writeToLog()`

#### 函数语法

```c
void writeToLog(char format[], ...);
```

#### 函数功能描述

将输出字符串写入**ASCII**或**BLF**日志文件。Write是基于C函数`printf`的。
编译器无法检查格式字符串。非法的格式条目将导致未定义的结果。与`writeToLogEx`函数不同，注释字符（“//”）和每行开头的时间戳将被打印出来。

注意点：

> 结果字符串的最大长度限制为1024个字符。
> 由于BLF不是一种人类可读的格式，因此无法在BLF日志文件中直接看到输出字符串，而只能在转换为ASCII日志文件后才能看到。

#### 函数参数介绍

函数的参数就是格式化的字符串，可以参考"Write Format Expressions"部分来编写。

### 举例说明

示例代码：

```c
on key 'a'
{
  MarkLogFile(123);
}

void MarkLogFile(int marker) {
  // marks line of ASCII logging file with an integer 
  writeToLog("===> %d",marker);
}
```



### 3.2. 函数: `writeToLogEx()`

#### 函数语法

```c
void writeToLogEx(char format[], ...);
```

#### 函数功能描述

将输出字符串写入**ASCII**或**BLF**日志文件。Write是基于C函数`printf`的。
编译器无法检查格式字符串。非法的格式条目将导致未定义的结果。与`writeToLog`函数不同，注释字符（“//”）和时间戳都不会打印在一行的开头。

注意点：

> 结果字符串的最大长度限制为1024个字符。
> 将具有**不带注释字符的自行生成行的ASCII文件**导入CANoe可能会导致问题。
> 由于BLF不是一种人类可读的格式，因此无法在BLF日志文件中直接看到输出字符串，而只能在转换为ASCII日志文件后才能看到。

#### 函数参数介绍

函数的参数就是格式化的字符串，可以参考"Write Format Expressions"部分来编写。

### 举例说明

示例代码：

```c
on key 'a'
{
  MarkLogFileWithTimeString();
}

// write marker with current date and time to logging file
void MarkLogFileWithTimeString(void)
{
  char timeBuffer[64];
  getLocalTimeString(timeBuffer);
  writeToLogEx("===> %s",timeBuffer);
}
```





## 四、 分离日志文件

这小节是摘录自：“How to Separate CAN Log Files for Each Test Case”， **KB0014084**

### Question: 

Is it possible to have separate CAN log files for each test case, if I want to create separate CAN log files?

### Answer: 

Yes it is, try this example CAPL code to achieve this requirement:

This creates a sample script and is for your reference. Follow steps 1 - 4 to configure the logging block in the CANoe:



实现代码：


```C
includes
{
}

variables
{
  const cDatePostFixLength = 11;
  const cMaxTestCaseTitleLength = 100;
  const cLogfileNameLength = cDatePostFixLength+cMaxTestCaseTitleLength;  

  char cDatePostfix[cDatePostFixLength+1] = "_{Date}.blf"; // added one byte for null-termination
  char cLoggingBlockName[9] = "Logging1";                  // added one byte for null-termination
}

PrepareLogfileNameAndStartLogging(char loggingBlock[])
{
  char logfileName[cLogfileNameLength+1];        // added one byte for null-termination
  char testCaseTitle[cMaxTestCaseTitleLength+1]; // added one byte for null-termination 

  testGetCurrentTestCaseTitle(testCaseTitle, elCount(testCaseTitle)); 

  strncpy(logfileName, testCaseTitle, elCount(logfileName));
  strncat(logfileName, cDatePostfix, elCount(logfileName));
  write(logfileName); // optional

  setLogFileName(loggingBlock, logfileName);

  startLogging(loggingBlock);
}

testcase TestCase1()
{
  PrepareLogfileNameAndStartLogging(cLoggingBlockName); 

  testWaitForTimeout(1000);  // placeholder for test contents 

  stopLogging(cLoggingBlockName);
}

testcase TestCase2()
{
  PrepareLogfileNameAndStartLogging(cLoggingBlockName); 

  testWaitForTimeout(1000);  // placeholder for test contents 

  stopLogging(cLoggingBlockName);
} 

void MainTest ()
{
  TestCase1();

  TestCase2();
}
```

