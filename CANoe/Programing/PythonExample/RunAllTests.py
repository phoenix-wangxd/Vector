# -----------------------------------------------------------------------------
# Example: Test Feature Set via Python
# 
# This sample demonstrates how to start the test modules and test 
# configurations via COM API using a Python script.
# The script uses the included PythonBasicEmpty.cfg configuration but is  
# working also with any other CANoe configuration containing test modules  
# and test configurations. 
# 
# Limitations:
#  - only the first test environment is supported. If the configuration 
#    contains more than one test environment, the other test environments 
#    are ignored
#  - the script does not wait for test reports to be finished. If the test
#    reports are enabled, they may run in the background after the test is 
#    finished
# -----------------------------------------------------------------------------
# Copyright (c) 2017 by Vector Informatik GmbH.  All rights reserved.
# -----------------------------------------------------------------------------

import msvcrt
import os
import time

from win32com.client import *
from win32com.client.connect import *


def do_events():
    pythoncom.PumpWaitingMessages()
    time.sleep(.1)


def do_events_until(cond):
    while not cond():
        do_events()


class CanoeSync(object):
    """ CANoe Application对象的包装器(Wrapper)类 """
    Started = False
    Stopped = False
    ConfigPath = ""

    def __init__(self):
        app = DispatchEx('CANoe.Application')
        app.Configuration.Modified = False
        ver = app.Version
        print('Loaded CANoe version ',
              ver.major, '.',
              ver.minor, '.',
              ver.Build, '...', sep='')
        self.App = app
        self.Measurement = app.Measurement
        self.Running = lambda: self.Measurement.Running
        self.WaitForStart = lambda: do_events_until(lambda: CanoeSync.Started)
        self.WaitForStop = lambda: do_events_until(lambda: CanoeSync.Stopped)
        WithEvents(self.App.Measurement, CanoeMeasurementEvents)

        self.Configuration = None
        self.TestSetup = None
        self.TestModules = None
        self.TestConfigs = None

    def load_cfg(self, cfg_path):
        # current dir must point to the script file
        cfg = os.path.join(os.curdir, cfg_path)
        cfg = os.path.abspath(cfg)
        print('Opening: ', cfg)
        self.ConfigPath = os.path.dirname(cfg)
        self.Configuration = self.App.Configuration
        self.App.Open(cfg)

    def load_test_setup(self, testsetup):
        """
        第一种自动化测试： 加载测试模块(Test-->Test Modules)的配置文件
        """
        self.TestSetup = self.App.Configuration.TestSetup
        path = os.path.join(self.ConfigPath, testsetup)
        testenv = self.TestSetup.TestEnvironments.Add(path)
        testenv = CastTo(testenv, "ITestEnvironment2")
        # TestModules property to access the test modules
        self.TestModules = []
        self.traverse_test_item(testenv, lambda tm: self.TestModules.append(CanoeTestModule(tm)))

    def load_test_configuration(self, testcfgname, testunits):
        """
        第二种自动化测试： 添加1个测试配置(Test-->Test Units-->Test Configurations),
        并使用存在的测试单元(test units)列表对其进行初始化
        """
        tc = self.App.Configuration.TestConfigurations.Add()
        tc.Name = testcfgname
        tus = CastTo(tc.TestUnits, "ITestUnits2")
        for tu in testunits:
            tus.Add(tu)
        # TestConfigs property to access the test configuration
        self.TestConfigs = [CanoeTestConfiguration(tc)]

    def start(self):
        if not self.Running():
            self.Measurement.start()
            self.WaitForStart()

    def stop(self):
        if self.Running():
            self.Measurement.stop()
            self.WaitForStop()

    def run_test_modules(self):
        """ 启动所有测试模块(Test-->Test Modules)并等待所有模块完成 """
        # start all test modules
        for tm in self.TestModules:
            tm.start()

        # wait for test modules to stop
        while not all([not tm.Enabled or tm.IsDone() for tm in APP.TestModules]):
            do_events()

    def run_test_configs(self):
        """ 启动所有测试配置(Test-->Test Units-->Test Configurations)并等待所有配置完成 """
        # start all test configurations
        for tc in self.TestConfigs:
            tc.start()

        # wait for test modules to stop
        while not all([not tc.Enabled or tc.IsDone() for tc in APP.TestConfigs]):
            do_events()

    def traverse_test_item(self, parent, testf):
        for test in parent.TestModules:
            testf(test)
        for folder in parent.Folders:
            found = self.traverse_test_item(folder, testf)


class CanoeMeasurementEvents(object):
    """ CANoe测量事件(Measurement events)的句柄(Handler) """

    def on_start(self):
        CanoeSync.Started = True
        CanoeSync.Stopped = False
        print("< measurement started >")

    def on_stop(self):
        CanoeSync.Started = False
        CanoeSync.Stopped = True
        print("< measurement stopped >")


class CanoeTestModule:
    """ CANoe的 TestModule对象(Test-->Test Modules)的包装器(Wrapper)类 """

    def __init__(self, tm):
        self.tm = tm
        self.Events = DispatchWithEvents(tm, CanoeTestEvents)
        self.Name = tm.Name
        self.IsDone = lambda: self.Events.stopped
        self.Enabled = tm.Enabled

    def start(self):
        if self.tm.Enabled:
            self.tm.start()
            self.Events.WaitForStart()


class CanoeTestConfiguration:
    """ CANoe的 TestConfiguration 对象(Test-->Test Units-->Test Configurations)的包装器(Wrapper)类 """

    def __init__(self, tc):
        self.tc = tc
        self.Name = tc.Name
        self.Events = DispatchWithEvents(tc, CanoeTestEvents)
        self.IsDone = lambda: self.Events.stopped
        self.Enabled = tc.Enabled

    def start(self):
        if self.tc.Enabled:
            self.tc.start()
            self.Events.WaitForStart()


class CanoeTestEvents:
    """ 用于处理测试事件(the test events)的实用程序(Utility)类 """

    def __init__(self):
        self.started = False
        self.stopped = False
        self.WaitForStart = lambda: do_events_until(lambda: self.started)
        self.WaitForStop = lambda: do_events_until(lambda: self.stopped)

    def on_start(self):
        self.started = True
        self.stopped = False
        print("<", self.Name, " started >")

    def on_stop(self, reason):
        self.started = False
        self.stopped = True
        print("<", self.Name, " stopped >")


if __name__ == '__main__':
    # 打开一个空的CANoe工程（尚未启动Measurement）
    # 如果当前电脑中存在多个CANoe版本，那将会打开最后安装的CANoe软件版本或者最后注册的CANoe的软件版本，
    # 如果想要打开指定的CANoe软件版本，需要在执行该步骤之前对想要打开的CANoe软件版本进行注册，然后再执行该步骤
    # 以管理员身份运行指定版本的RegisterComponents.exe程序即可完成注册
    APP = CanoeSync()

    # 加载一个示例版的CANoe工程（即CANoe配置文件）， 一般我们自己创建的CANoe工程都会有一个.cfg的配置文件
    APP.load_cfg('CANoeConfig\PythonBasicEmpty.cfg')

    # 加载1个测试模块(Test-->Test Modules)的配置文件
    APP.load_test_setup('TestEnvironments\Test Environment.tse')

    # 加载1个测试配置(Test-->Test Units-->Test Configurations)，同时添加一系列的test_units
    APP.load_test_configuration('TestConfiguration',
                                ['TestConfiguration\EasyTest\EasyTest.vtuexe'])

    # 正式开始测量(Measurement)
    APP.start()

    # 开始运行测试模块(Test-->Test Modules)
    APP.run_test_modules()

    # 开始运行测试配置(Test-->Test Units-->Test Configurations)
    APP.run_test_configs()

    # 等待按下任意键来结束程序
    print("Press any key to exit ...")
    while not msvcrt.kbhit():
        do_events()

    # 停止测量(Measurement)
    APP.stop()
