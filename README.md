# XYRunner
HTTP和GUI自动化测试软件
Chapter 1 安装和启动

XYRunner 作为一个测试软件，用于接口和 UI 自动化测试，你只需要修改一个表格文档即可管理所有的测试用例。也只需要修改一个配置文件即可全局管理软件配置。 
XYRunner 使用了经典的 pytest + Allure 报告，报告十分美观。
你的注意力仅仅需要放在测试用例的编写即可。
1.1安装XYRunner
1.在你的 windows 环境下解压 XYRunner.zip 即可。

2.验证  XYRunner 是否安装正确。在 XYRunner 安装目录内运行 CMD：


1.2界面介绍
双击运行 XYRunner.exe 后，会出现两个界面，一个控制台用于显示当前运行情况，一个主界面。

Chapter 2 用法

2.1通过XYRunner -[option] 调用XYRunner
你可以通过XYRunner的用命令行来调用测试：


这种调用方式几乎等同于直接点击 Start Test ,但需要注意的是这种通过 XYRunner 来调用的方式若没有在当前目录运行 CMD 则必须将当前目录添加到系统环境变量。

2.2-[option]具体参数
2.3配置文件



配置文件中包括 [project] [projectDB] [comments] [RunningConfig] 

 [project] 中的 server 需要添加本次测试的服务器地址，注意：最后不要带斜杠。

 [project] 中的 allure_results_Path 需要添加本次测试的服务测试报告数据的绝对路径，注意：如果用 jinkens + allure 来进行持续集成，则需要把 allure_results_Path 路径下的所有文件复制到jinkens的项目路径的allure-results文件夹下。

[projectDB]  是本次项目的数据库地址配置。

[comments] 中的 dictCol 是测试用例表格中需要转化为字典的列的名称。注意：千万别修改，修改后 XYRunner 无法获取你的用例。


[RunningConfig] 的 sheetname 是本次运行用例的shee表名称，注意：不填则无用例。


[RunningConfig] 的 Tag 是本次测试需要执行的用例标签。注意：不填则全部执行。


[RunningConfig] 的 marker 是选择本次测试是执行 UI 还是 API 测试， 注意：不填则都需要执行。

日志说明

日志分为4个等级：

Allure 服务说明

启动 Allure 服务 会通过本程序开启一个 flask 服务，地址会显示在控制台。

注意：打开 Allure 服务使用的是配置文件中的 allure_results_Path 路径下的的数据。
