# -*- coding: utf-8 -*-
# @Time : 2021\2\10 0010 0:24
# @Author : JacksonCui
# @File : main.py
# @Software: PyCharm
from PyQt5 import QtCore,QtWidgets
from PyQt5.Qt import *
import sys, os, time
from Project.Common.DoConfig import DoConf
from GUI.XYRunner import Ui_Form
from Project.Test_Case.run import Run
from Project.Common.FilePath import CaseFile_path, logger_path, config_path
from  GUI.Tool import QSSTool

class Runthread_Log(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread_Log, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        f = open(logger_path, 'r', encoding='utf-8')

        while 1:
            where = f.tell()
            line = f.readline()
            if not line:
                time.sleep(1)
                f.seek(where)
            else:
                self._signal.emit(line)


class Runthread_Run(QtCore.QThread):

    def __init__(self):
        super(Runthread_Run, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        self.r = Run()
        self.r.runWithoutAllure()

class Runthread_Allure(QtCore.QThread):
    #  通过类成员对象定义信号对象
    def __init__(self):
        super(Runthread_Allure, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        self.conf = DoConf()
        self.allure_results_Path = self.conf.get_value_from_section('project', 'allure_results_Path')
        os.system(f'allure serve {self.allure_results_Path}')

class Runthread_Conf(QtCore.QThread):
    file_time = pyqtSignal()

    def __init__(self,status):
        super(Runthread_Conf, self).__init__()
        self.path = config_path
        # 死循环状态
        self.status = status
        # 默认文件最后修改时间
        self.endTime = os.path.getmtime(self.path)
    def __del__(self):
        self.wait()

    def run(self):
        if self.status == 'open_conf':
            os.startfile(config_path)
        while True:
            # 判断文件修改时间
            if self.endTime != os.path.getmtime(self.path):
                self.endTime = os.path.getmtime(self.path)
                # 发送文件修改信号
                self.file_time.emit()
            self.sleep(1)
class Window(QWidget, Ui_Form, QThread):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('XYRunner')
        self.resize(712, 631)
        self.setupUi(self)
        self.thread = None  # 初始化线程
        for arg in sys.argv:
            if arg == '-v':
                print('version:1.0.0')
                sys.exit()
            elif arg == '-r':
                Run.runWithoutAllure()
                sys.exit()
            elif arg == '-oc':
                os.startfile(CaseFile_path)
                sys.exit()
            elif arg == '-oconf':
                os.startfile(config_path)
                sys.exit()
            elif arg == '-ol':
                os.startfile(logger_path)
                sys.exit()
            elif arg == '-a':
                conf = DoConf()
                allure_results_Path = conf.get_value_from_section('project', 'allure_results_Path')
                os.system(f'allure serve {allure_results_Path}')
            elif arg == '-help' or arg == '-h':
                print("usage: XYRunner [option] Try `XYRunner -h' for more information.\n"
                      "其中[option]包括：\n"
                      "-v       输出产品版本并退出\n"
                      "-r       按照配置文件，不启动Allure服务开始测试\n"
                      "-a       启动Allure服务\n"
                      "-oc       打开测试用例文件\n"
                      "-oconf       打开配置文件\n"
                      "-ol       打开日志文件\n"
                      "-help or -h       获取帮助\n"
                      "有关详细信息，请访问GitHub：https://github.com/JacksonCui76/XYRunner")
                sys.exit()

    def start_test(self):
        # 日志线程
        self.thread_log = Runthread_Log()
        self.thread_log._signal.connect(self.append_line)  # 进程连接回传到GUI的事件
        self.thread_log.start()
        # 配置文件线程
        self.thread_conf = Runthread_Conf('run')
        self.thread_conf.file_time.connect(self.restart)  # 进程连接回传到GUI的事件
        self.thread_conf.start()
        # 测试线程
        self.thread_run = Runthread_Run()
        self.thread_run.start()

    def open_casefile(self):
        os.startfile(CaseFile_path)

    def open_conf(self):
        self.thread = Runthread_Conf('open_conf')
        # 连接信号
        self.thread.file_time.connect(self.restart)  # 线程连接回传到GUI的事件
        # 开始线程
        self.thread.start()

    def restart(self):
        result = QtWidgets.QMessageBox.question(self,
                                                "重启确认",
                                                '配置文件被修改，需要重启XYRunner生效，是否重启？',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            qApp.exit(1224)
        else:
            pass
    def open_log(self):
        # 创建线程
        self.thread = Runthread_Log()
        # 连接信号
        self.thread._signal.connect(self.append_line)  # 进程连接回传到GUI的事件
        # 开始线程
        self.thread.start()

    def append_line(self, line):
        self.textBrowser_2.append(line)

    def open_rlt(self):
        # 创建线程
        self.thread = Runthread_Allure()
        # 开始线程
        self.thread.start()

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '警告', '退出后测试将停止,\n你确认要退出吗？',
                                           QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    # 创建一个应用程序对象
    app = QApplication(sys.argv)
    # QSSTool.qss2obj('./style.qss',app)
    # app.setStyleSheet(qdarkgraystyle.load_stylesheet_pyqt5())
    window = Window()
    if len(sys.argv) == 1:
        window.show()
    # 应用程序执行，进入到消息循环
    current_exit_code = sys.exit(app.exec_())
