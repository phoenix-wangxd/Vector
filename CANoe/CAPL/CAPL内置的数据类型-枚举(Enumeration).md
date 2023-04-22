# CAPL内置的数据类型--枚举(Enumeration)

为了更加优雅的使用CAPL语言，所以我们需要更加深入的了解一下CAPL内置的数据类型，本文介绍枚举(Enumeration)类型。

>  本文大部分摘录自Vector的官方文档，对于概念部分， 只是做了整理与翻译； 
>  对于代码部分：我自己做了一些实际的测试，并将这些示例代码写的更加实用化一些



## 一、枚举(Enumeration)类型简要说明

`枚举(Enumeration)`类型与旧版本的CANoe不兼容。因此，它们只能在具有CANoe 7.0版或更高版本的CAPL程序中使用。

### 1.1 枚举类型简要说明

枚举类型在CAPL中的定义方式在C语言中的类似:

```c
enum Colors { Red, Green, Blue };
```

切记：**在整个CAPL程序中，元素名称(Element names)必须是唯一的**。



固定整数值也可以指定给各个元素（这个和C语言也非常相似）：

```c
enum State { State_Off = -1, State_On = 1 };
```

如果没有赋值，第一个元素的值将为0，所有后续元素的值都将为前一个值加1。



补充说明：

1. 可以在任何可以声明变量的地方定义枚举类型。
2. 从7.1版本开始，您可以使用name方法获取值标识符。




## 二、 枚举(Enumeration)类型补充说明

### 2.1 枚举类型在CAPL中的语义说明

为了简化后面的代码部分，这一小节后面代码中均定义了下面的枚举结构：

```c
enum g_Gear_Post 
  {Gear_Post_Reserved=0, 
   Gear_Post_P, 
   Gear_Post_R, 
   Gear_Post_N, 
   Gear_Post_D };

enum g_Week
  {Mon = 1,Tues = 2,Wed = 3, Thurs = 4, Fri = 5, Sat = 6, Sun = 7 };
```

### 2.2. 如有必要，枚举类型会隐式转换为整数类型

例如，在使用算术运算时候，枚举类型会隐式转换为整数类型：

```c
int i=0;
enum g_Gear_Post gear;

gear = Gear_Post_N;
i = gear + 1;   // i目前的值为4
```



### 2.3. 枚举类型以使用计数类型

特别是在switch case语句中，可以使用计数类型：
```c
enum g_Gear_Post gear;
gear = Gear_Post_R;
switch (gear) {
  case Gear_Post_P:
    write("current Gear Post is: P");
    break;
  case Gear_Post_R:
    write("current Gear Post is: R");   // 输出这条内容
    break;
  case Gear_Post_N:
    write("current Gear Post is: N");
    break;
  case Gear_Post_D:
    write("current Gear Post is: D");
    break;
  default:
    write("current Gear Post is: Other");
    break;
}
```



### 2.4. 整数类型强转为枚举类型

要从整数类型(integer type)转换为枚举类型，或在两种不同的枚举类型之间转换，需要使用强制类型转换：

```c
enum g_Gear_Post gear;
enum g_Week week;

gear = (enum g_Gear_Post) 1;  // 如果不强制类型转化，则会编译报错
write("current Gear Post is: %d", gear); // 输出的结果是1

week = (enum g_Week) gear;   // 如果不强制类型转化，则会编译报错
write("current weekt is: %d", week);   // 输出的结果是1
```



### 2.5. 可以获取枚举类型的值标识符

您可以使用`name`方法获取枚举类型值标识符(identifier)：

```c
enum g_Gear_Post gear;
enum g_Week week;

gear = (enum g_Gear_Post) 1;  // 如果不强制类型转化，则会编译报错
write("current Gear Post is: %s", gear.Name()); // 占位符部分输出的结果是：Gear_Post_P

week = (enum g_Week) gear;   // 如果不强制类型转化，则会编译报错
write("current weekt is: %s", week.Name());     // 占位符部分输出的结果是：Mon
```

补充说明：

>  如果当前值没有可用的标识符(identifier)，则该值将转换为字符串。



### 2.5. 查枚举类型是否包含特定值

可以使用`containsValue`方法检查枚举类型是否包含特定值：

```c
enum g_Gear_Post gear;

if(gear.containsValue(4)){
  write("The name of value %d is %s", 4, ((enum g_Gear_Post)4).name());  // 这条会输出
}
if(gear.containsValue(5)){
  write("The name of value %d is %s", 5, ((enum g_Gear_Post)5).name());  // 这条不会输出
}
```



## 三、 数据库中的枚举(Enumeration)类型

在DBC数据库中定义的值表(Value tables)会自动在CAPL中定义为枚举类型。类型采用值表的名称，其元素来自同一个表。

下面示例代码的前提是： 在DBC文件中定义了名为`VtSig_Gear`的值表(Value table)，包含元素`Idle`、`Gear_1`、`Gear_2`等。

```c
variables {
  enum VtSig_Gear oldGear = Idle;
}

on signal Gear
{
  if (abs(this – oldGear) > 0 && this != Idle)
  {
    write("Jump in Gear!");
    oldGear = (enum VtSig_Gear) this;
  }
}
```

注意事项：

- 值表(Value table)中分配给数据库中多个值的元素不能用作枚举元素。
- 不能使用值表(Value table)中名称不是有效CAPL名称的元素。
- CAPL程序中的类型和变量的名称掩盖了值表(Value table)及其元素的名称。但是，您可以将值表的名称添加到元素中：`gear = VtSig_Gear::Idle`；



## 四、 系统变量中的枚举(Enumeration)类型

系统变量的值表(value tables)会自动定义枚举类型。该类型的前缀为 `VtSv_` ，后续的部分由**命名空间(namespace)**和**系统变量的名称**组成；其中所述各个部分通过**下划线**连接起来。

描述可以作为常量(constants)附加；如果必要的话，它们必须使用名称空间和变量的名称进行限定。

> 原文：
>
> Additionally value tables of system variables automatically define enumeration types. The type has the prefix **VtSv_** and as next consists of the namespace and the name of the system variable; wherein the single parts are connected by underscores. The descriptions may be attached as constants; if necessary they have to be qualified with namespace and name of the variable.



```c
variables {
   enum VtSv_Osek_NMState nmState = NM_On;
}

on key 't' {
   @sysvar::Osek::NMState = sysvar::Osek::NMState::NM_BusSleep;
}
```



## 五、CAPL中的枚举(Enumeration)类型


### 5.1.  枚举类型的定义
在CAPL中我们有三种方法定义枚举类型，如下。

**方法1： 先定义枚举类型，再定义枚举变量**

```c
variables
{
  enum Colors { Red, Green, Blue };  // 定义类型名称为Colors的枚举类型
  enum Colors color;   // 定义枚举类型Colors的枚举变量color
}
```

**方法2： 定义枚举类型的同时定义枚举变量**

```c
variables
{
  enum Colors { Red, Green, Blue } color; 
}
```


**方法3： 省略枚举名称，直接定义枚举变量**

```c
variables
{
  enum { Apple, Pear, Banana } fruit = Apple;
}
```


### 5.2.  枚举类型作为参数

枚举类型也可以用作函数中的参数和返回类型。要执行此操作，必须添加关键字`enum`。
```c
enum Colors NextColor(enum Colors c)
{
  if (c == Blue)
  {
    return Red;
  }
  else
  {
    return (enum Colors) (c + 1);
  }
}
```



## 六、总线中的枚举(Enumeration)类型

总线类型有一个预定义的枚举类型。它相当于CAPL的定义

```c
enum BusType
{
  eCAN      = 1,               // CAN bus
  eFlexRay  = 7,               // FlexRay bus
  eEthernet = 11,              // Ethernet network
  eAfdx     = 16,              // 
  eWildcard = 0xFFFFFFFF       // 
};
```

此枚举类型特别用于**PDU对象(PDU objects)**的`BusType`选择器。
