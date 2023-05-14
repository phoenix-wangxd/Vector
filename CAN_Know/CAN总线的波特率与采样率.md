# CAN控制器配置



## 参考文档

本文参考文档如下：

- CANoe的帮助文档： Network Hardware » CAN » CAN Controller Configuration



[How to Change the Baud Rate of a CAN bus with CAPL](https://support.vector.com/kb?id=kb_article_view&sysparm_article=KB0013440)









## 重要的the bit timing







## CANoe中的CAN控制器配置


the bit timing是在考虑the bit timing参数的情况下以图形方式显示的。
A bit time它被细分为三个段：SYNC（橙色）、TSEG1（蓝色）和TSEG2（绿色）。





### CAN Controller Mode

可以通过下拉列表的方式设置CAN控制器模式。下拉列表中有3个选项可用：

- **Normal**
  The CAN controller participates in bus communication.
- **Ack Off**
  The bus is influenced by the measurement since the CAN controller on the interface card represents the interface between the analysis software and the CAN bus. Particularly the CAN controller sends its acknowledge for correctly recognized messages by sending a dominant level (on the bus) in the corresponding slot of the CAN message. To reduce the influence on the system you can switch off this functionality. Thereby the node is no longer visible on the bus. Please keep in mind that – when you switched off acknowledge – communication on the bus only may happen if at least one other network node sends an acknowledge.
- **Restricted**
  This mode is only supported by CAN FD enabled hardware interfaces and drivers.
  It s possible to receive valid data and remote frames. On valid frames, the CAN controller sends an acknowledge. If the CAN controller recognizes an error, it will not send error frames or overload frames, but it switches to bus integration state. In this mode it is possible to perform measurements on the bus without a CAN interface affecting the measurement by Error Frames (e.g. measuring an Error Flag sent by a real ECU). Sending is not possible in this mode.
  A [Write Window notification](../../../Windows/Write/WriteWindowNotifications.htm) will be displayed if the CAN controller switches to bus integration state due to an error.

最常用的就是Normal了，其他的就不多介绍了。



### TX Self-ACK

Vector的硬件接口可以在传输can消息时自动生成确认(acknowledge)。这允许在不连接其他主动CAN控制单元(active CAN control units)的情况下模拟网络。在这种情况下，所使用的CAN通道仍必须接终端电阻。如果不支持**Self-ACK**，则在测量开始时， Write窗口中将显示一条错误消息。



### 采样点Sample Point

采样点(The Sample Point)是读取总线电平并将其解释为相应位的值的时间点。它的位置在TSEG1的末端。

![CANoe_CAN_Hardware_CAN_SamplePoint_1](.//Picture//Hardware//CANoe_CAN_Hardware_CAN_SamplePoint_1.png)



采样时间点（在TSEG1和TSEG2之间的边界处）根据配置的样本数量由一个或三个红色小三角形标识。

![CANoe_CAN_Hardware_CAN_SamplePoint_2](.//Picture//Hardware//CANoe_CAN_Hardware_CAN_SamplePoint_2.png)





The relationship between the bit length and the sampling point and the overall length of the represented bit time correspond to the percentage of the **sample point**.

比特长度(the bit length)和采样点(the sampling point)之间的关系以及所表示的bit time的总长度对应于采样点的百分比。



### 预览同步边缘Preview Synchronization Edge

To visualize the influence of the synchronization jump width (SJW) parameter, you can use the slider to adjust the position of the synchronization edge and to examine their influence on the bit timing.
In **CAN mode** you must activate the **Preview synchronization edge** option.

The position of the slider defines time point of a synchronization edge on the bus (i.e. the beginning of a bit) relatively to the bit time of the controller. The upper area of the figure shows the nominal bit timing, i.e. a bit on the bus is represented as it is expected by the controller. The lower area of the figure shows the internal controller timing, i.e. the bit time interval from the perspective of the controller. The length of this bit interval depends on the time point of the arriving synchronization edge:

- If the edge falls within the **Sync** range of nominal timing, the controller runs synchronously.
- If the edge falls within the **TSEG1** range of nominal timing, re-synchronization must be performed.
  In this case the **TSEG1** segment must be lengthened up to **SJW** (Synchronization Jump Width) BTL cycles.
- If the edge falls within the **TSEG2** range of nominal timing, re-synchronization must be performed.
  In this case the **TSEG2** segment must be shortened by up to **SJW** (Synchronization Jump Width) BTL cycles.
- If no edge falls within the nominal timing this bit time is not used for re-synchronization.





### 使用数据库设置
如果使用的数据库包含有关波特率(baud rate)和位计时(bit timings)的信息，则可以选择“使用数据库设置”选项来接受这些值。支持DBC和AUTOSAR ARXML格式。



## SSP-Offset

### SSP 解释
The **S**econdary **S**ampling **P**oint Offset (SSP) is used for the compensation of the **T**ransmitting Node **D**elay (TD). To compensate the TD the transmitter must be able to compare its transmitted bit to the current bit on the CAN network.
The SSP is then measured from the beginning of the transmitters received bit.
As of baud rates = 1Mbit/s the TD compensation is activated automatically. Therefore for the SSP offset a default value is used. The default value can be overwritten here.

二次采样点偏移（SSP）用于补偿发射节点延迟（TD）。为了补偿TD，变送器必须能够将其传输位与CAN网络上的当前位进行比较。
然后从发射机接收比特的开始测量SSP。
当波特率=1Mbit/s时，TD补偿会自动激活。因此，SSP偏移量使用默认值。此处可以覆盖默认值。





![CANoe_CAN_Hardware_CAN_SSP_1](.//Picture//Hardware//CANoe_CAN_Hardware_CAN_SSP_1.png)
