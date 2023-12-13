# CANdelaStudio入门



# 0：CANdelaStudio使用小Tip



## 0.1 打开软件与文件

在打开 CANdelaStudio软件时：官方推荐使用“开始”菜单中的图标打开CANdelaStudio软件，这样可以避免打开德文版本的CANdelaStudio软件。比如双击 CANdelaStudio 15 English 图标，就可以打开英文版的CANdelaStudio软件。



在打开CDD/CDDT文件时,  官方推荐先打开 CANdelaStudio软件，然后在“File”-->“Open”选择需要打开的CDD/CDDT文件； 而不推荐在Windows的文件管理器中直接双击CDD/CDDT文件来进行打开，这样可能会引起一些不必要的问题。



## 0.2 查看软件版本信息

如果想要查看CANdelaStudio软件信息：

![CANdelaStudio_Product_Infomation](.//Picture//CANdelaStudio_Product_Infomation.png)



## 0.3 许可证的不同

不同CANdelaStudio许可证的区别：

![CANdelaStudio_License_Diff](.//Picture//CANdelaStudio_License_Diff.png)



## 0.4 不同的视图

两种不同的视图：

- **Standard View**：标准视图，所以的License都支持
- **Expert View**：专家试图，只有Admin权限才有这个视图

如果你有Expert View权限，强烈推荐使用Expert View来打开文件，因为这样可以看到更多的数据和更多的选项。



# 一：CDD与CDDT的对比

首先要清楚， 只有CANdela Studio Admin许可证才能编辑CDDT文件，其余均不能编辑CDDT文件。



## 1.1 CDD与CDDT文件的使用场景

CDD与CDDT文件可以在ECU开发的多个阶段进行使用，同一需求，制作的CDD/CDDT可以导入多种开发阶段，继而保证数据的一致性。

![CANdelaStudio_Process](.//Picture//CANdelaStudio_Process.png)



## 1.2 CDD与CDDT的不同

CDDT是 CDD Template的缩写， 也就是CDD的模板文件， 从上图可以看到CDDT是制作CDD的原材料，那么为什么要拆分CDD与CDDT呢？



那些数据应该在CDDT中定义，哪些数据应该在CDD中定义，下图以22服务为例进行了一个简单的说明：

![CANdelaStudio_Template_Concept_3](.//Picture//CANdelaStudio_Template_Concept_3.png)

 

# 二：编辑CDDT文件

首先要清楚， 只有CANdela Studio Admin许可证才能编CDDT文件。



## 2.1 CDDT模板文件

如果你有OEM提供的CDDT模板文件，则可以直接使用该文件； 如果没有，可以使用Vector提供的示例CDDT模板文件，打开方法如下：

![CANdelaStudio_CDDT_Edit_1](.//Picture//CANdelaStudio_CDDT_Edit_1.png)

常用的是中间的 `Vector_UDS_14.1.cddt` 文件， 我们需要自己点击“New”，然后找到模板，点击“Open”即可。



