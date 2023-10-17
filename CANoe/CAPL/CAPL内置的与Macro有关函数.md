# CAPL内置的与Macro有关函数



## 0、 参考文档

本文参考文档
- 本文函数部分摘录自Vector的官方文档，做了整理与翻译，增加了自己的理解， 并将代码改造的更加优雅实用一些。
- 



## 一、 介绍常用函数

CAPL中与宏有关的函数如下：

| Macro                   | 简短的描述                                                   |
| :---------------------- | :----------------------------------------------------------- |
| %BASE_FILE_NAME%        | 刚编译的.can文件的名称（例如SomeFile.can）；在“include File”中特别有用 |
| %BASE_FILE_NAME_NO_EXT% | 刚编译但没有文件扩展名的.can文件的名称（例如SomeFile）；在“include File”中特别有用 |
| %BUS_TYPE%              | 节点分配到的通道的总线类型(Bus type)                         |
| %CHANNEL%               | 节点分配到的通道的编号(Channel)                              |
| %FILE_NAME%             | 当前文件的名称（例如SomeIncludeFile.cin）                    |
| %FILE_NAME_NO_EXT%      | 没有文件扩展名的当前文件的名称（例如SomeIncludeFile）        |
| %LINE_NUMBER%           | 文件中包含该宏的行号（CANoe 13.0可用）                       |
| %NETWORK_NAME%          | 节点分配到的网络的名称                                       |
| %NODE_NAME%             | 节点的名称                                                   |


补充说明：
>Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。



### 注意：

- 宏 `%NODE_NAME%`,   `%BUS_TYPE%`,  `%CHANNEL%` and   `%NETWORK_NAME%` 仅在Simulation Setup中有用;  尽管如此，他们在其他地方也被允许
- 网关相关的宏 `%BUS_TYPE%`,   `%CHANNEL%`  和  `%NETWORK_NAME%` 分别表征第一总线/通道类型和第一网络。



### 关于文件名称的宏的举例说明

- 宏`%BASE_FILE_NAME%` 和`%BASE_FILE_NAME_NO_EXT%`,  主要在当该文件是被别的文件include进去的时候， 这两个宏可以显示最原始的调用文件的名称
- 宏`%FILE_NAME%` 和`%FILE_NAME_NO_EXT%`,  这两个宏单纯的显示当前的文件名称，不在乎是被谁include的



文件示例结构：

![capl_test_marco](.//Picture//capl_test_marco.png)

示例代码：

```c
on start
{
  Write("Current File Name:  %FILE_NAME%,   %FILE_NAME_NO_EXT%");
  Write("Current Base File Name:  %BASE_FILE_NAME%,   %BASE_FILE_NAME_NO_EXT%");
}
```

执行出来的效果：

```
Current File Name:  test_include_file.cin,   test_include_file
Current Base File Name:  Node1.can,   Node1
Current File Name:  Node1.can,   Node1
Current Base File Name:  Node1.can,   Node1
```





### 几个常用宏的举例说明

创建一个系统变量: `sysvar::MySpace::VarString`， 变量类型为String。 然后示例代码如下：

```c
write("The node name is %NODE_NAME%");
sysSetVariableString(sysvar::MySpace::VarString, "%CHANNEL%");
write("Activated functionality in network %NETWORK_NAME% (Channel %BUS_TYPE%%CHANNEL%)");
```

在我电脑中的测试结果是：

```
The node name is Node1
Activated functionality in network CAN (Channel CAN1)
```





### 新增的宏: %LINE_NUMBER%

对于只能在CANoe13以上使用的宏%LINE_NUMBER%， 如果在低版本中使用，并不会编译错误，只是运行的结果会不符合期望。 

```c
  #if TOOL_MAJOR_VERSION >= 13
    write("The current version of CANoe is greater than or equal to 13;   Current Line Number: %LINE_NUMBER% ");
  #else
    write("The current version of CANoe is less than 13;   Current Line Number: %LINE_NUMBER% ");
  #endif
```

在CANoe15中运行这段代码，显示的效果：

```
The current version of CANoe is greater than or equal to 13;   Current Line Number: 11 
```

如果在小于CANoe13版本中运行这段代码，显示的效果（没有测试过）：

```
The current version of CANoe is less than 13;   Current Line Number: INE_NUMBER
```



