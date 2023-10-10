# CAPL内置的与TestReport有关函数



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

