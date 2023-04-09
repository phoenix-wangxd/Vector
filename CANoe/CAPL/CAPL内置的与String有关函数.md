# CAPL内置的与String有关函数

在CAPL中我们要经常和字符串打交道，为了方便的写CAPL脚本，所以我整理了Vector官方提供的与String有关的函数，并对常用的进行简单说明。

>  本文绝大部分摘录自Vector的官方文档，只是做了整理与翻译； 另外增加了一些我的理解。



## 一、CAPL中与String有关的函数

### 1.1 字符串字面量(String Literal)

**字符串字面量(string literal)** 是一个**带引号**的字符串, 比如：  "This is a character string"

注意：
>  与C语言中一样，当在**char数组(char arrays)** 中存储**字符串字面量(string literals)** 时，数组末尾的一个char需要为字符串终止字符（/0）保留，即char数组需要比纯字符串长度长一个元素。

#### 转义序列
某些字符显示为字符串中带有前反斜杠（转义序列）的字符组合，例如：

| Description           | Display Inside Character Strings |
| :-------------------- | :------------------------------- |
| New line **(新的一行)** | `\n`                               |
| Tabulator **(制表符)** | `\t`                               |
| Backslash **(反斜线)** | `\\`                               |
| Carriage return **(回车)** | `\r`                               |
| Backspace **(退格符)** | `\b`                               |
| Double quotation mark **(双引号)** | `\"`                               |
| Single quotation mark **(单引号)** | `\'`                               |



### 1.2 常用字符串函数

Windows和Linux支持这些CAPL功能。Linux下的功能尚未经过全面测试。

第一部分：

| Functions       | Short Description                                        |
| :-------------- | :------------------------------------------------------- |
| `_atoi64`       | Converts a string to a 64bit integer.                    |
| `_gcvt`         | Converts a number to a string.                           |
| `atodbl`        | Converts a string into a double number.                  |
| `atol`          | Converts a string to a LONG number.                      |
| `ConvertString` | Converts a string from one encoding to another encoding. |
| `DecodeString`  | Decodes the byte array input from the encoding codepage. |
| `EncodeString`  | Encodes the string input with the encoding codepage.     |
| `ltoa`          | Converts a number to a string.                           |


第二部分：

| Functions          | Short Description                                            |
| :----------------- | :----------------------------------------------------------- |
| `mbstrlen`         | 返回字符串的长度(位置以**字符(characters)** 为单位)          |
| `mbstrncmp`        | 比较两个字符串(位置以**字符(characters)** 为单位)            |
| `mbstrncmp_off`    | 比较两个字符串(位置以**字符(characters)** 为单位)，可以指定偏移量 |
| `mbstrncpy`        | 将一个字符串复制到另一个字符串(位置以字符为单位)             |
| `mbstrncpy_off`    | 将一个字符串复制到另一个字符串(位置以字符为单位)，可以指定偏移量 |
| `mbstrstr`         | 在另一个字符串中搜索一个字符串(位置以字符为单位)             |
| `mbstrstr_off`     | 在另一个字符串中搜索一个字符串(位置以字符为单位)，可以指定偏移量 |
| `mbsubstr_cpy`     | 将一个子字符串复制到另一个字符串(位置以字符为单位)           |
| `mbsubstr_cpy_off` | 将一个子字符串复制到另一个字符串(位置以字符为单位)，可以指定偏移量 |



第三部分：

| Functions     | Short Description                                            |
| :------------ | :----------------------------------------------------------- |
| `snprintf`    | 将格式化的字符串打印为字符数组(character array)              |
| `strlen`      | 获取字符串的长度(位置以**字节(bytes)** 为单位)               |
| `strncat`     | 将一个字符串追加到另一个字符串                               |
| `strncmp`     | 比较两个字符串(位置以**字节(bytes)** 为单位)                 |
| `strncmp_off` | 比较两个字符串(位置以**字节(bytes)** 为单位)，可以指定偏移量 |
| `strncpy`     | 将一个字符串复制到另一个字符串(位置以字节为单位)             |
| `strncpy_off` | 将一个字符串复制到另一个字符串(位置以字节为单位)，可以指定偏移量 |
| `strstr`      | 在另一个字符串中搜索一个字符串(位置以字节为单位)             |
| `strstr_off`  | 在另一个字符串中搜索一个字符串(位置以字节为单位)，可以指定偏移量 |
| `strtod`      | 将字符串转换为浮点数                                         |
| `strtol`      | 将字符串转换为32位整型(integer)                              |
| `strtoll`     | 将字符串转换为64位整型(integer)                              |
| `strtoul`     | 将字符串转换为无符号32位整型(integer)                        |
| `strtoull`    | 将字符串转换为无符号64位整型(integer)                        |

第四部分：

| Functions           | Short Description                                            |
| :------------------ | :----------------------------------------------------------- |
| `substr_cpy`        | 将一个子字符串复制到另一个字符串(位置以字节为单位)           |
| `substr_cpy_off`    | 将一个子字符串复制到另一个字符串(位置以字节为单位)，可以指定偏移量 |
| `str_match_regex`   | 检查字符串是否与正则表达式模式完全匹配                       |
| `str_replace`       | 将字符串中出现的所有文本替换为另一个字符串。将字符串的一部分替换为另一个字符串。 |
| `str_replace_regex` | 将字符串中出现的所有模式替换为另一个字符串                   |
| `strstr_regex`      | 在字符串中使用正则表达式模式进行搜索                         |
| `strstr_regex_off`  | 在字符串中使用正则表达式模式进行搜索，可以指定偏移量         |
| `toLower`           | 将字符或字符串转换为小写                                     |
| `toUpper`           | 将字符或字符串转换为大写                                     |



#### 字符(character)与字节(bytes)的关系
根据字符串编码(string encoding)规则，一个**字符(character)** 可能需要几个**字节(bytes)**，例如Windows ANSI（932）编码中的日语字符或UTF-8编码中的任何特殊字符。

**使用说明：**

- 如果你使用标准的ASCII表中的字符，可以使用以`str`开头的函数， 它们全部以**字节(byte)** 为单位
- 如果你需要使用特殊字符（如：不在ASCII表中的字符）， 你应该使用以`mb`开头的函数进行代替，它们全部以**字符(character)** 为单位，适用于这种特殊编码的情况 。



## 二、 字符串长度

这里主要介绍  `strlen()` 、`mbstrlen()`、 `elCount()`三个函数

### 2.1 函数:  `strlen()`  与`mbstrlen()` 

- `strlen()` 函数的名称应该是： **string(字符串)** + **length(长度)** 的缩写
- `mbstrlen() `函数的名称应该是： **MultiByte(多字节)** + **string(字符串)** + **length(长度)** 的缩写


#### 函数语法

```c
long strlen(char s[]);    // 获取单字节字符串长度

long mbstrlen(char s[]);  // 获取多字节字符串长度
```

#### 函数参数说明

入参s, 代表的是需要获取长度的字符串对象s

#### 函数功能描述

- **strlen()** 函数的返回值是入参(字符串s)的长度（以**字节(bytes)** 为单位）
- **mbstrlen()** 函数的返回值是入参(字符串s)的长度（以**字符(characters)** 为单位）

#### 举例说明

关于`strlen()` 与 `elCount()` 的示例代码：

```c
long length;
char buffer[100] = "CANalyzer";
write("strlen:%d",strlen(buffer));    // 结果是strlen:9
write("elCount:%d",elCount(buffer));  // 结果是elCount:100
```
关于`mbstrlen()` 与 `strlen()` 的示例代码：

```c
long length;
char s1[10] = "door";
char s2[10] = "Tür";
write("%d %d", mbstrlen(s1), strlen(s1)); // 4 4   因为这里都是标准的ASCII字符，所以1个字符占1个Byte
write("%d %d", mbstrlen(s2), strlen(s2)); // 3 [3 or 4 depending on file encoding]  这里用了非标准字符
```


### 2.2 函数:  `elCount()` 

函数的名称应该是： **elements(元素)** + **count(计数)** 的缩写

#### 函数语法

```c
long elcount(...); // if used with arrays which are function parameters

dword elcount(...); // in all other cases
```

#### 函数参数说明

任意类型的**数组(array)**， 因此这个函数不止可以用在string中。

#### 函数功能描述

确定**数组(array)** 的元素个数

#### 返回值介绍

元素的个数

#### 举例说明

关于`elCount()` 的示例代码：

```c
void bsp(int ar[]) {
  int i;
  for(i=0; i < elCount(ar); i++)
    ...
}

void bsp2(byte ar[][]) {
  int i, j;
  for(j=0; j < elCount(ar); j++ )
    for(i=0; i<= elCount(ar[j]); i++ )
      ...
}
```



## 三、 比较两个字符串

这里主要介绍 `strncmp()` /`strncmp_off()`； `mbstrncmp()`/ `mbstrncmp_off()`四个函数，它们的作用类似，主要是在类型、是否偏移上存在不同点。

### 3.1 函数:  `strncmp()`

`strncmp()`函数的名称应该是： **string(字符串)** + **compare(比较)** 的缩写

#### 函数语法

```c
long strncmp(char s1[], char s2[], long len); // form 1

long strncmp(char s1[], char s2[], long s2offset, long len); // form 2
```

#### 函数参数说明

| 参数     | 参数含义                          |
| -------- | --------------------------------- |
| s1       | First string                      |
| s2       | Second string                     |
| s2offset | s2中的偏移量（以**bytes**为单位） |
| len      | 要比较的最大**字节数(bytes)**     |

#### 函数功能描述

此函数将**s1**与**s2**进行比较，最多可使用**len**个字符。

form 2的比较从**s2**的**s2offset**处开始。

#### 返回值介绍

| 返回值 | 返回值说明                                    |
| ------ | --------------------------------------------- |
| -1     | if s1 is less than s2(字符串**s1**小于**s2**) |
| 1      | if s2 is less than s1(字符串**s2**小于**s1**) |
| 0      | if the strings are equal(两个字符串相同)      |

#### 举例说明

关于`strncmp()` 的示例代码：

```c
on key 's'
{
  char s1[7] = "Vector";
  char s2[7] = "Vector";
  if(strncmp(s1,s2,strlen(s1)))
    write("not equal");
  else
    write("equal");
}
```



### 3.2 函数:  `strncmp_off()`

`strncmp_off()`函数的名称应该是： **string(字符串)** + **compare(比较)** + **offset(偏移)** 的缩写

#### 函数语法

```c
long strncmp_off(char s1[], long s1offset, char s2[], long s2offset, long len);
```

#### 函数参数说明

| 参数     | 参数含义                                |
| -------- | --------------------------------------- |
| s1       | First string                            |
| s2       | Second string                           |
| s1offset | 字符串s1中的偏移量（以**bytes**为单位） |
| s2offset | 字符串s2中的偏移量（以**bytes**为单位） |
| len      | 要比较的最大**字节数(bytes)**           |

#### 函数功能描述

此函数将**s1**与**s2**进行比较，最多可使用**len**个字符。

比较从: **s1**的**s1offset**  与  **s2**的**s2offset** 位置处开始。

#### 返回值介绍

| 返回值 | 返回值说明                                    |
| ------ | --------------------------------------------- |
| -1     | if s1 is less than s2(字符串**s1**小于**s2**) |
| 1      | if s2 is less than s1(字符串**s2**小于**s1**) |
| 0      | if the strings are equal(两个字符串相同)      |

#### 举例说明

关于`strncmp_off()` 的示例代码：

```c
char s1[18] = "Vector Informatik";
char s2[11] = "Informatik";
if (strncmp_off(s1, 7, s2, 0, strlen(s2)) == 0)
   write("Equal!");
else
   write("Unequal!");
```



### 3.3 函数:  `mbstrncmp()`与`mbstrncmp_off()`

#### 函数语法

```c
long mbstrncmp(char s1[], char s2[], long len); // form 1

long mbstrncmp(char s1[], char s2[], long s2offset, long len); // form 2

long mbstrncmp_off(char s1[], long s1offset, char s2[], long s2offset, long len); // form 3
```

#### 函数参数说明

| 参数     | 参数含义                           |
| -------- | ---------------------------------- |
| s1       | First string                       |
| s2       | Second string                      |
| len      | 要比较的最大**字符数(characters)** |
| s1offset | s1中的偏移量（以**字符(characters)** 为单位） |
| s2offset | s2中的偏移量（以**字符(characters)** 为单位）  |

#### 函数功能描述

此函数将**s1** 与 **s2** 进行比较，最多可使用**len** 个字符。

比较从: **s1** 的**s1offset**  与  **s2**的**s2offset** 位置处开始。

#### 返回值介绍

| 返回值 | 返回值说明                                    |
| ------ | --------------------------------------------- |
| -1     | if s1 is less than s2(字符串**s1**小于**s2**) |
| 1      | if s2 is less than s1(字符串**s2**小于**s1**) |
| 0      | if the strings are equal(两个字符串相同)      |

#### 举例说明

关于`mbstrncmp_off()` 的示例代码：

```c
char s[50] = "'Tür' is the german word for 'door'.";
write("%d", mbstrncmp_off(s, 13, "german", 0, 6));     // 0  采用了form 3
```



## 四、 字符串拼接、拷贝

这里主要介绍以下三类函数：

-  拼接：`strncat()`
-  拷贝： `strncpy()`、 `strncpy_off()` 、`mbstrncpy()`、 `mbstrncpy_off()`
-  拷贝：`substr_cpy()`、`substr_cp_off()`、`mbsubstr_cpy()`、 `mbsubstr_cpy_off()`

### 4.1 函数:  `strncat()`

`strncat()`函数的名称应该是： **string(字符串)** + **number(个数)** + **concatenate(连接)** 的缩写

#### 函数语法

```c
void strncat(char dest[], char src[], long len);
```

#### 函数参数说明

| 参数     | 参数含义                          |
| ---- | ------------------------------------------------------------ |
| dest | Target string to which characters are appended.              |
| src  | Appended string.                                             |
| len  | Maximum length of composite string including terminating '\0'. |

#### 函数功能描述

此函数将**src**附加到**dest**。len表示添加后的字符串的最大长度。该函数可确保存在一个终止的“\0”。

因此，最多可以复制 `len - strlen(dest) - 1` 个字符。

注意：

> 与C语言中的`strncat`函数不同，`len`表示添加后的字符串的最大长度，包括终止的“\0”，而不是要附加的字符数。

#### 举例说明

关于`strncpy()` 与`strncat()`的示例代码：

```c
char s[20];
strncpy(s, "Vector", 10); // s is "Vector"
strncat(s, " CANoe", 19); // s is "Vector CANoe"
strncpy(s, "Vector", 10); // s is "Vector"
strncat(s, " CANoe", 11); // s is "Vector CAN"
```



### 4.2 函数:  `strncpy()`与`strncpy_off()`

`strncpy()`函数的名称应该是： **string(字符串)** + **number(个数)** + **copy(拷贝)** 的缩写

#### 函数语法

```c
void strncpy(char dest[], char src[], long max);

void strncpy_off(char dest[], long destOffset, char src[], long max);
```

#### 函数参数说明


| 参数       | 参数含义                                                     |
| ---------- | ------------------------------------------------------------ |
| dest       | Destination buffer（目标缓冲区）                             |
| destOffset | Offset in destination buffer（目标缓冲区中的偏移量）         |
| src        | Source string                                                |
| max        | 用于确定复制的最大字节数。不得大于**dest**的大小。最多复制**max-1**个字节。如果**src**短于此，则会继续复制，直到遇到终止的“\0”为止。 |


#### 函数功能描述

- `strncpy`函数将`src`复制到`dest`。`max`表示`dest`的大小（以Byte为单位）。该函数可确保存在一个终止的“\0”。因此，最多可复制 **max-1** 个字节。
- `strncpy_off`函数的`max`表示`dest`的大小（以Byte为单位）。该函数可确保存在一个终止的“\0”。因此，最多可复制`max-1-destOffset`字节。从`destOffset`开始，`dest`中的字节被覆盖。


#### 举例说明

关于`strncpy()` 与`strncpy_off()`的示例代码：

```c
variables {
   char s1[7] = "Vector";
   char s2 [32];
}
on key 'z'
{                                 // Output to the Write-Window:
   strncpy (s2,s1,elcount(s2));
   write ("Result: %s",s2);       // Result: Vector
}

char s[6] = "Hello";
strncpy_off(s, 1, "e", elcount(s)); // s: He
```



### 4.3 函数:  `mbstrncpy()`与`mbstrncpy_off()`

`mbsubstr_cpy()`函数的名称应该是：  **MultiByte(多字节)** + **string(字符串)** + **number(个数)** + **copy(拷贝)** 的缩写

#### 函数语法

```c
void mbstrncpy(char dest[], char src[], long len);

void mbstrncpy_off(char dest[], long destOffset, char src[], long len);
```

#### 函数参数说明

| 参数     | 参数含义                         |
| -------- | -------------------------------- |
| dest       | Destination buffer（目标缓冲区）                                  |
| src        | Source string                                                |
| len        | 要复制的**字符数(characters)**，如果输入`-1`则尽可能多地复制 |
| destOffset | 目标缓冲区的**字符数(characters)** 偏移量 |


#### 函数功能描述

- `mbstrncpy`函数将`src`复制到`dest`。`len`表示应复制的字符数；使用`-1`表示应尽可能多地复制到`dest`中（最大值直到`src`结束）。该函数确保有一个终止的0字节；但与`strncpy`不同的是，该字节不计入`len`。
- `mtrncpy_off`从字符偏移`destOffset`开始覆盖目标缓冲区中的字符。


#### 举例说明

关于`mbstrncpy_off()`的示例代码：

```c
char s1[50] = "eine grüne "; // german for 'a green'
char s2[10] = "Türen"; // german for 'doors'
mbstrncpy_off(s1, 11, s2, 3);
write("%s", s1); // eine grüne Tür (german for 'a green door')
```



### 4.4 函数:  `substr_cpy()`与`substr_cpy_off()`

`substr_cpy()`函数的名称应该是：  **Sub..(子)** + **string(字符串)** + **copy(拷贝)** 的缩写

#### 函数语法

```c
void substr_cpy(char dest[], char src[], long srcStart, long len, long max);

void substr_cpy_off(char dest[], long destOffset, char src[], long srcStart, long len, long max);
```

#### 函数参数说明


| 参数       | 参数含义                                                     |
| ---------- | ------------------------------------------------------------ |
| dest       | Destination buffer（目标缓冲区）                             |
| destOffset | Offset in bytes in destination buffer（目标缓冲区中的偏移量, 以bytes为单位） |
| src        | Source string                                                |
| srcStart   | Start index in bytes in **src** of substring                 |
| len        | Length of the substring in bytes, or -1 to copy the string until the end |
| max        | Size of **dest** in bytes                                    |


#### 函数功能描述

- `substr_cpy`函数将`src`的子字符串复制到`dest`。`max`表示`dest`的大小（以字节为单位）。该函数可确保存在一个终止的“\0”。因此，最多可复制`max-1`个字节。
- `substr_cpy_off`函数的`max`表示`dest`的大小（以字节为单位）。该函数可确保存在一个终止的“\0”。因此，最多可复制`max-1-destOffset`字节。从`destOffset`开始，`dest`中的字节被覆盖。


#### 举例说明

关于`substr_cpy()` 与 `substr_cpy_off()` 的示例代码：

```c
char s1[7];
char s2[18] = "Vector Informatik";
substr_cpy(s1, s2, 0, 6, elcount(s1)); // s1: Vector

char s1[9] = "New CAPL";
char s2[18] = "Vector Informatik";
substr_cpy_off(s2, 7, s1, 4, -1, elcount(s2)); // s2: Vector CAPL
```



### 4.5 函数:  `mbsubstr_cpy()`与`mbsubstr_cpy_off()`

`mbsubstr_cpy()`函数的名称应该是：  **MultiByte(多字节)** + **Sub..(子)** + **string(字符串)** + **copy(拷贝)** 的缩写

#### 函数语法

```c
void mbsubstr_cpy(char dest[], char src[], long srcStart, long len);

void mbsubstr_cpy_off(char dest[], long destOffset, char src[], long srcStart, long len);
```

#### 函数参数说明

| 参数       | 参数含义                                                 |
| ---------- | -------------------------------------------------------- |
| dest | Destination buffer（目标缓冲区） |
| src        | Source string                                                |
| srcStart   | Start index in **characters** in **src** of substring        |
| len        | 要复制的**字符数(characters)**，输入`-1`表示尽可能多地复制 |
| destOffset | 目标缓冲区中的偏移量（以**characters** 为单位） |

#### 函数功能描述

- `mbsubstra_cpy`将`src`的子字符串复制到`dest`。`len`表示应复制的字符数；使用`-1`表示应尽可能多地复制到`dest`中（最大值直到`src`结束）。该函数确保有一个终止的0字节；但与`substra_cpy`/`substra_cpy_off`相反，该字节不计入`len`。
- `mbsubstra_cpy_off`从字符偏移destOffset开始覆盖目标缓冲区中的字符。


#### 举例说明

关于`mbsubstr_cpy_off()` 的示例代码：

```c
char s1[50] = "eine grüne "; // german for 'a green'
char s2[20] = "schöne Türen"; // german for 'beautiful doors'
mbsubstr_cpy_off(s1, 11, s2, 7, 3);
write("%s", s1); // eine grüne Tür (german for 'a green door')
```



## 五、 字符串搜索、匹配

这里主要介绍以下三类函数：

-  普通搜索：  `strstr()`、 `strstr_off()` 、`mbstrstr()`、 `mbstrstr_off()`
-  正则搜索：`strstr_regex()`、 `strstr_regex_off()`
-  正则匹配： `str_match_regex()`

### 5.1 函数:  `strstr()`与`strstr_off()`

`strstr()`函数的名称应该是：  **string(字符串)** + **in(在...内)**  + **string(字符串)** 缩写

#### 函数语法

```c
long strstr(char s1[], char s2[]);

long strstr_off(char s1[], long offset, char s2[]);
```

#### 函数参数说明

| 参数 | 参数含义                                                     |
| ---- | ------------------------------------------------------------ |
| s1     | First string                                                 |
| s2     | Second string                                                |
| offset | 在**s1**的这个偏移量【以字节(bytes)为单位】处开始搜索 |

#### 函数功能描述

在字符串**s1**中搜索字符串**s2**

#### 函数返回值描述

-  如果在字符串**s1**中找到字符串**s2**， 则返回找到的第一个位置
-  如果在字符串**s1**中未找到字符串**s2**，则返回值为 **-1**。


#### 举例说明

关于`strstr()` 的示例代码：

```c
long pos;
char s1[18] = "Vector Informatik";
char s2[11] = "Informatik";
pos = strstr(s1, s2); // pos = 7
```



### 5.2 函数:  `mbstrstr()`与`mbstrstr_off()`

`strstr()`函数的名称应该是：  **MultiByte(多字节)** + **string(字符串)** + **in(在...内)**  + **string(字符串)** 缩写

#### 函数语法

```c
long mbstrstr(char s1[], char s2[]);

long mbstrstr_off(char s1[], long offset, char s2[]);
```

#### 函数参数说明

| 参数   | 参数含义                                                     |
| ------ | ------------------------------------------------------------ |
| s1     | First string                                                 |
| s2     | Second string                                                |
| offset | 在**s1**的这个偏移量【以**字符(characters)** 单位】处开始搜索 |

#### 函数功能描述

在字符串**s1**中搜索字符串**s2**

#### 函数返回值描述

-  如果在字符串**s1**中找到字符串**s2**， 则返回找到的第一个位置
-  如果在字符串**s1**中未找到字符串**s2**，则返回值为 **-1**。

#### 举例说明

关于`mbstrstr()` 的示例代码：

```c
long pos;
char s[50] = "'Tür' is german for 'door'";
pos = mbstrstr(s, "german");
write("%d", pos); // 9
```



### 5.3 函数:  `strstr_regex()`与`strstr_regex_off()`

#### 函数语法

```c
long strstr_regex(char s[], char pattern[]);

long strstr_regex_off(char s[], long offset, char pattern[]);
```

#### 函数参数说明

| 参数   | 参数含义                                              |
| ------ | ----------------------------------------------------- |
| s       | String to be searched.                                       |
| offset  | 在s参数的偏移处(offset)开始搜索                              |
| pattern | 搜索的正则表达式; 对于正则表达式，使用与Perl编程语言相同的语法 |


#### 函数功能描述

在字符串中使用正则表达式模式进行搜索

#### 函数返回值描述

-  如果在字符串**s1**中找到**正则表达式模式**， 则返回找到的第一个位置
-  如果在字符串**s1**中未找到**正则表达式模式**，则返回值为 **-1**。


#### 举例说明

关于`strstr_regex()` 与`strstr_regex_off()`的示例代码：

```c
char buffer[70] = "Vector Informatik";
long res;
res = strstr_regex(buffer, "Inf[a-z]*"); // 7
res = strstr_regex_off(buffer, res + 1, "Inf[a-z]*"); // -1
```



### 5.4 函数:  `str_match_regex()`

#### 函数语法

```c
long str_match_regex(char s[], char pattern[]);
```

#### 函数参数说明


| 参数   | 参数含义                                                     |
| ------ | ------------------------------------------------------------ |
| s       | String to be checked.                                        |
| pattern | 进行字符串匹配的正则表达式；对于正则表达式，使用与Perl编程语言相同的语法。 |


#### 函数功能描述

检查字符串是否与正则表达式模式完全匹配。

#### 函数返回值描述

- 如果字符串与正则表达式匹配成功，则为1；
- 如果字符串与正则表达式匹配不成功，则为0。


#### 举例说明

关于`str_match_regex()`的示例代码：

```c
char buffer[70] = "Vector Informatik";
long res;
res = str_match_regex(buffer, "Vector [A-Za-z]*"); // 1
res = str_match_regex(buffer, "Inf[a-z]*"); // 0
```



## 六、 字符串替换

这里主要介绍以下两类函数：

-  普通替换：`str_replace()`
-  正则替换：`str_replace_regex()`

### 6.1 函数:  `str_replace()`

#### 函数语法

```c
long str_replace(char s[], char searched[], char replacement[]); // form 1

long str_replace(char s[], long startoffset, char replacement[], long length); // form 2
```

#### 函数参数说明


| 参数   | 参数含义                                                   |
| ------ | ---------------------------------------------------------- |
| s           | 要修改的字符串(String)      |
| searched    | 应替换的文本(Text)             |
| startoffset | 开始替换字符的偏移量 |
| replacement | 替换原始字符的文本(Text) |
| length      | 要替换的最大字符数(characters) |


#### 函数功能描述

形式1：将字符串中出现的所有文本替换为另一个字符串。
形式2：将字符串的一部分替换为另一个字符串。

#### 函数返回值描述

- 如果替换成功，则为**1**
- 如果结果字符串对于缓冲区s来说太长，则为**0**。

#### 举例说明

关于`str_replace()`的示例代码：

```c
char buffer[70] = "Vector Informatik";
str_replace(buffer, "Informatik", "CANoe");
write(buffer);
str_replace(buffer, 7, "CANalyzer", 10);
write(buffer);
```



### 6.2 函数:  `str_replace_regex()`

#### 函数语法

```c
long str_replace_regex(char s[], char pattern[], char replacement[]);
```

#### 函数参数说明

| 参数        | 参数含义                                                     |
| ----------- | ------------------------------------------------------------ |
| s           | 要修改的字符串(String)                                       |
| pattern     | 正则表达式，用于确定s中应替换的部分；对于正则表达式，使用与Perl编程语言相同的语法 |
| replacement | Replacement for the parts which match the pattern.           |

#### 函数功能描述

形式1：将字符串中出现的所有文本替换为另一个字符串。

形式2：将字符串的一部分替换为另一个字符串。

#### 函数返回值描述

如果成功，则为**1**，如果结果字符串对于缓冲区s来说太长，则为**0**。

#### 举例说明

关于`str_replace_regex()`的示例代码：

```c
char buffer[70] = "Vector Informatik";
str_replace_regex(buffer, "Inf[a-z]*", "CANoe");
write(buffer);
```



## 七、 字符串其他常用函数

由于CAPL是一种类C的语言，为了说明部分函数，所以我们要先介绍该函数在C语言中的实现。


### 7.1 C语言中的  `sprintf()` 与  `snprintf()`

在C语言中`sprintf()`函数与`snprintf()`函数的语法如下：

```C
int sprintf ( char * str, const char * format, ... );

int snprintf ( char * s, size_t n, const char * format, ... );
```

#### 函数功能描述

在C语言中`sprintf()`函数的功能：

> **Write formatted data to string**
> 使用与`printf()`上使用`format`时打印的文本相同的文本编写字符串，但内容不是打印的，而是以C字符串的形式存储在参数`str`指向的缓冲区中。
> 缓冲区(buffer)的大小应该足够大，可以包含整个结果字符串（请参阅`snprintf`以获得更安全的版本）。
> 在写入的内容之后会自动附加一个终止的空字符。
> 在`format`参数之后，函数需要至少与格式化所需的附加参数一样多。

在C语言中`snprintf()`函数的功能：

> **Write formatted output to sized buffer**
>
> 使用与`printf`上使用`format`时打印的文本相同的文本编写一个字符串，但内容不是打印的，而是以C字符串的形式存储在s指向的缓冲区中（取参数`n`作为要填充的最大缓冲区容量）。
> 如果生成的字符串长度超过`n-1`个字符，则会丢弃剩余的字符并不对其进行存储，而是根据函数返回的值进行计数。
> 在写入的内容之后会自动附加一个终止的空字符。
> 在format参数之后，函数需要至少与格式化所需的附加参数一样多。

#### 举例说明

关于`sprintf()` 的示例代码：

```C
/* sprintf example */
#include <stdio.h>

int main ()
{
  char buffer [50];
  int n, a=5, b=3;
  n=sprintf (buffer, "%d plus %d is %d", a, b, a+b);
  printf ("[%s] is a string %d chars long\n",buffer,n);
  return 0;
}
```

输出结果：

```
[5 plus 3 is 8] is a string 13 chars long
```



关于`snprintf()` 的示例代码：

```c
/* snprintf example */
#include <stdio.h>

int main ()
{
  char buffer [100];
  int cx;

  cx = snprintf ( buffer, 100, "The half of %d is %d", 60, 60/2 );

  if (cx>=0 && cx<100)      // check returned value

    snprintf ( buffer+cx, 100-cx, ", and the half of that is %d.", 60/2/2 );

  puts (buffer);

  return 0;
}
```

输出结果：

```
The half of 60 is 30, and the half of that is 15.
```



### 7.2 CAPL函数:  `snprintf()`

`snprintf()`函数的名称应该是：  **string(字符串)** + + **number(个数)** + **printf(格式化打印)** 的缩写

#### 函数语法

```c
long snprintf(char dest[], long len, char format[], ...);
```

#### 函数参数说明


| 参数   | 参数含义                                                     |
| ------ | ------------------------------------------------------------ |
| dest   | 要打印到的字符缓冲区(Character buffer)                       |
| len    | 打印到缓冲区的最大字符数，包括终止的“\0”。最大为缓冲区的大小。 |
| format | 打印到缓冲区的格式化字符串(Formatted string)                 |

注意：
> CAPL支持最多64个参数的函数调用。

#### 函数功能描述

这个函数对应于C语言中的`sprintf()`/`snprintf()`函数， 详见上面介绍的C语言中的函数的功能。

#### 函数返回值描述

写入的字符数


#### 举例说明

关于`snprintf()` 的示例代码：

```c
char buffer[100], str[7] = "Vector";
long i;
i = snprintf(buffer,elcount(buffer),"String: %s\n", str);
write("Output:\n%s : Character count = %d\n", buffer, i);
```

