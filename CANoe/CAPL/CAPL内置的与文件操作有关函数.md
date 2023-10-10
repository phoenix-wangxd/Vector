# CAPL内置的与文件操作有关函数



## 0、 参考文档

本文参考文档
- 本文函数部分摘录自Vector的官方文档，做了整理与翻译，增加了自己的理解， 并将代码改造的更加优雅实用一些。



## 一、说明

通常需要在覆盖多个测量的一段时间内保存变量或测量值。为此，CAPL中提供了文件功能。
虽然文件访问操作通常被认为是易于使用和可靠的，但它们相当缓慢。因此，在测量过程中，不应在时间关键阶段进行文件访问。建议主要在`on-preStart`和`on-stop`事件处理程序中使用CAPL文件访问。



## 二、 文件搜索过程(File Search Procedure)

### 2.1 单主机环境(Single Host Environment)

文件搜索过程用于确定绝对文件路径, 写入和读取文件有不同的过程。

#### 读取访问时的文件搜索顺序(File Search Order on Read Access)

1. 如果在CANoe模拟(simulation)或测试(test)启动时候使用CAPL文件功能，首先会在**预定义的用户文件(pre-defined user files)**列表（`Configuration|Options|Extensions|User Files`）中查找文件名，并采用指定的路径。
2. 如果在**预定义的用户文件列表(pre-defined user files)**中找不到文件名，并且以前调用过CAPL函数`setFilePath`，请使用以`setFilePath`为基础指定的目录来确定绝对路径。
3. 如果在打开文件进行读取访问之前没有调用`setFilePath`，请在第一个数据库的目录中搜索该文件。
4. 如果在那里找不到文件，将使用其他数据库的目录。
5. 如果仍然找不到该文件，将使用配置文件(the configuration file)的目录。



#### 写入访问时的文件搜索顺序(File Search Order on Write Access)

1. 如果在CANoe模拟(simulation)或测试(test)启动时候使用CAPL文件功能，首先会在**预定义的用户文件列表(pre-defined user files)**（`Configuration|Options|Extensions|User Files`）中查找文件名，并采用指定的路径。
2. 如果在**预定义的用户文件(pre-defined user files)**列表中找不到文件名，并且以前调用过CAPL函数`setFilePath`或`setWritePath`，请使用以`setFilePath`/`setWritePath`为基础指定的目录来确定绝对路径。
3. 如果在打开文件进行写访问之前没有调用`setFilePath`/`setWritePath`，则将使用配置目录(the configuration directory)作为基准来确定绝对路径。



### 2.2 分布式仿真环境(Distributed Simulation Environment)

在分布式模式(distributed mode)或独立模式(standalone mode)下，需要在`Configuration|Options|Extensions|User Files`下预先定义CANoe模拟或测试设置中CAPL程序中要读取的所有文件。测量开始时，它们被复制到远程设备上的一个特殊同步目录中。在远程RT内核上调用的CAPL文件函数将给定的文件名隐式解析为基于此同步目录的文件路径。

仅用于写入访问的文件也可以如上所述预定义。如果它们尚未预定义，则将被隐式注册为当前测量的用户文件。测量结束时，在远程设备上创建或更改的所有文件都会传输回用户计算机。

需要文件名的CAPL函数也接受文件名前面的路径。如果文件名已经注册，则会忽略路径组件。在隐式注册的用户文件的情况下，文件路径被解释为在测量端将文件复制到的用户计算机上的文件路径。

在分布式环境中，CAPL函数`setFilePath`、`setWritePath`和`getAbsFilePath`不可用。






## 三、 介绍常用函数

CAPL中与文件有关的函数如下：

| Functions              | Short Description                                  |
| :--------------------- | :------------------------------------------------- |
| `fileClose`            | 关闭指定的文件                                     |
| `fileGetBinaryBlock`   | 以二进制格式从指定文件中读取字符                   |
| `fileGetString`        | 从指定的文件中读取字符串                           |
| `fileGetStringSZ`      | 从指定的文件中读取字符串                           |
| `filePutString`        | 在指定的文件中写入字符串                           |
| `fileRewind`           | 将位置指针重置为文件的开头                         |
| `fileWriteBinaryBlock` | 在指定的文件中写入字节                             |
| `getOfflineFileName`   | 返回当前使用的离线源文件的完整路径                 |
| `getNumOfflineFiles`   | 返回已配置的离线源文件数                           |
| `getAbsFilePath`       | 获取相对于当前配置定义的路径的完整路径名           |
| `getProfileArray`      | 【配置文件】从指定文件中的指定节中读取给定变量的值 |
| `getProfileFloat`      | 【配置文件】同上                                   |
| `getProfileInt`        | 【配置文件】同上                                   |
| `getProfileString`     | 【配置文件】同上                                   |
| `getUserFilePath`      | 获取用户文件(user file)的绝对路径                  |
| `Open`                 | 此函数用于打开名为filename的文件                   |
| `openFileRead`         | 打开文件进行读取访问                               |
| `openFileWrite`        | 打开文件进行写入访问                               |
| `RegisterUserFile`     | 动态注册用户文件(user file)                        |
| `setFilePath`          | 设置目录(directory)的读写路径                      |
| `setWritePath`         | 设置函数`openFileWrite`的写入路径                  |
| `writeProfileFloat`    | 【配置文件】打开文件，搜索节并写入变量             |



补充说明：

>Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。



### 3.1 函数:  `setFilePath()` 

除了在**预定义的用户文件列表(pre-defined user files)**（`Configuration|Options|Extensions|User Files`）中定义要读写的文件名、文件路径外，我们可以使用`setFilePath()` 函数灵活控制我们需要操作的文件。

#### 函数语法

```c
void setFilePath (char Path[],  dword mode);
```

#### 函数功能描述

此函数用于设置目录的读写路径(Path)。路径(Path)可以是绝对的，也可以是相对于当前活动配置的。



#### 函数参数介绍


| 参数       | 含义                                                         |
| ---------- | ------------------------------------------------------------ |
| `Path`     | 需要设置的路径，可以是绝对路径，也可以是相对路径             |
| `mode`     | `0`:  Sets path for **read** functions;     `1`:  Sets path for **write** functions;     `2`:  Sets path for **both** types of functions |

>  注意， 如果mode参数选择为1时候， 效果完全等同于直接使用`setWritePath`函数

####  举例说明

参考下面的读写配置文件





## 四、 介绍常用的与读写配置文件有关的函数



### 4.1 函数:  `writeProfileInt()`等

写入配置文件的三种方式：`writeProfileInt()`、 `writeProfileFloat()`、  `writeProfileString()`

在调用此函数之前，必须由函数`setWritePath`设置写入路径。否则将使用配置目录。必须将相对文件名传递给函数。



#### 函数语法

```c
long writeProfileString(char section[], 
                        char entry[], 
                        char value[], 
                        char filename[]);  //form 1

long writeProfileString(char section[], 
                        char entry[], 
                        char value[], 
                        char filename[], 
                        dword utf16);      // form 2
```

#### 函数功能描述

打开`filename`，搜索`section`部分，并写入具有`value`的变量`entry` 。如果`entry`已存在，则覆盖旧值。

函数结果是写入的字符数，或者在出现错误时为0。



#### 函数参数介绍


| 参数         | 含义                                                       |
| ------------ | ---------------------------------------------------------- |
| `section` | 以字符串形式显示文件的节（section）       |
| `entry`  | 字符串形式的变量名称（Variable name）         |
| `value`  | 字符串形式的值                |
| `filename` | 字符串形式的文件名称                          |
| `utf16`  | 如果设置了此标志，则如果文件是新写入的，则文件将被UTF-16LE编码，或者如果相应的BOM也存在，则文件被如此解释。 |



####  举例说明

需要注意的是： `writeProfile` 系列函数并不支持写数组的功能，我们可以通过写string的方式，将数组键值对进行写入。

示例代码如下：

```c
variables
{
  char Test_Config_File_Dir[20] = "D:\\Vector";
  char Test_Config_File_Name[20] = "My_Config.ini";
}


On key 'q'
{ 
  //define symbolic values for read/write access mode
  dword FILE_PATH_R   = 0;
  dword FILE_PATH_W   = 1;
  dword FILE_PATH_RW  = 2;
  
  // 设置需要写入的section
  char Tmp_Section_Student[20] = "Student";
  char Tmp_Section_Teacher[20] = "Teacher";  
  char Tmp_Section_Class[20] = "Class";    
  
  // 设置操作的文件路径
  setFilePath(Test_Config_File_Dir , FILE_PATH_RW);
  // 在章节Tmp_Section_Student中写入字符串
  writeProfileString (Tmp_Section_Student,"name","zhang.san",Test_Config_File_Name);
  // 在章节Tmp_Section_Student中写入浮点数
  writeProfileFloat (Tmp_Section_Student,"height", 141.5, Test_Config_File_Name);
  // 在章节Tmp_Section_Student中写入整形
  writeProfileInt (Tmp_Section_Student, "age", 12, Test_Config_File_Name);
  // 在章节Tmp_Section_Student中写入数组【以字符串的形式】
  writeProfileString (Tmp_Section_Student,"int_array","10,11,20,100",Test_Config_File_Name);
  
  // 在章节Tmp_Section_Teacher中写入字符串
  writeProfileString (Tmp_Section_Teacher,"name","li.si",Test_Config_File_Name);
  // 在章节Tmp_Section_Teacher中写入浮点数
  writeProfileFloat (Tmp_Section_Teacher,"height", 171.6, Test_Config_File_Name);
}
```

按下`q`键后，在目录`D:\\Vector`中，创建了一个名为`My_Config.ini`的文件，内容如下：

```ini
[Student]
name=zhang.san
height=141.5
age=0xc
int_array=10,11,20,100
[Teacher]
name=li.si
height=171.6
```



### 4.2 函数:  `getProfileInt()`等

读取配置文件的三种方式：`getProfileInt()`、 `getProfileFloat()`、  `getProfileString()`、 `getProfileArray()`

在调用此函数之前，必须由函数`setWritePath`设置写入路径。否则将使用配置目录。必须将相对文件名传递给函数。



#### 函数语法

```c
long getProfileString(char section[], 
                      char entry[], 
                      char def[], 
                      char buff[], 
                      long buffsize, 
                      char filename[]);   // form 1

long getProfileString(char section[], 
                      char entry[], 
                      char def[], 
                      char buff[], 
                      long buffsize, 
                      char filename[], 
                      dword utf16);       // form 2
```

#### 函数功能描述

在的`filename`中`section`部分下搜索变量`entry`。其内容`value`被写入缓冲区`buff`。其长度必须以缓冲区(buffer)大小正确传递。
如果找不到文件或`entry`，则将默认值`def`复制到缓冲区(buffer)。

如果读取的字符串长度比缓冲区长，则该字符串将被剪切为缓冲区长度。

#### 函数参数介绍


| 参数         | 含义                                                         |
| ------------ | ------------------------------------------------------------ |
| `section`    | 以字符串形式显示文件的节（section）                          |
| `entry`      | 字符串形式的变量名称（Variable name）                        |
| `def`        | 以字符串形式给出：出现错误时的默认值                         |
| `buff`       | 以字符串形式给出：读入字符的缓冲区                           |
| `buffersize` | `buff`参数的大小（以字节为单位）（最多1022个字符）           |
| `filename`   | 字符串形式的文件名称                                         |
| `utf16`      | 如果设置了此标志，则文件将被解释为UTF-16LE编码，如果相应的BOM也存在。写入buff的字符串将转换为CAPL编码。 |



####  举例说明

在目录`D:\\Vector`中，创建了一个名为`My_Config.ini`的配置文件，内容：

```ini
[Student]
name=zhang.san
height=141.5
age=0xc
int_array=10,11,20,100
[Teacher]
name=li.si
height=171.6
```

> 这个文件就是上面上面章节的write函数添加的。

读取配置文件的示例代码如下：

```c
variables
{
  char Test_Config_File_Dir[20] = "D:\\Vector";
  char Test_Config_File_Name[20] = "My_Config.ini";
}


On key 'q'
{   
  int i;
  char cTmp50[50];   // 临时变量，用于存放读取到的字符数组
  int ret;           // 函数返回值
  float ret_float;   // 浮点型数据函数返回值
  
  // 设置需要读取的section
  char Tmp_Section_Student[20] = "Student";
  
  
  // 设置操作的文件路径
  setFilePath(Test_Config_File_Dir , 2);

  // 读取字符串，返回值是字符串长度
  ret = getProfileString(Tmp_Section_Student, "  name", "not find", cTmp50, elCount(cTmp50), Test_Config_File_Name);
  Write("string length is :%d, get string is :%s",ret, cTmp50);
  
  // 读取整型，返回值是结果
  ret = getProfileInt(Tmp_Section_Student, "age ", 0, Test_Config_File_Name); 
  Write("get int value is:%d",ret);
  
  // 读取浮点型，返回值是结果
  ret_float = getProfileFloat(Tmp_Section_Student, "height  ", 0, Test_Config_File_Name); 
  Write("get float value is:%f",ret_float);
  
  // 读取数字数组，返回值是数字数组长度
  ret = getProfileArray(Tmp_Section_Student, "int_array", cTmp50, elCount(cTmp50), Test_Config_File_Name); 
  Write("get Array length is:%d",ret);
  for(i=0;i<ret;i++){
    Write("get Array[%d] value is:%d",i,cTmp50[i]);     
  }
}
```

按下`q`键后，Write窗口输出的内容如下：

```ini
string length is :9, get string is :zhang.san
get int value is:12
get float value is:141.500000
get Array length is:4
get Array[0] value is:10
get Array[1] value is:11
get Array[2] value is:20
get Array[3] value is:100
```



