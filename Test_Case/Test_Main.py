# -*- coding: utf-8 -*-
# @Time : 2021\1\13 0013 10:45
# @Author : JacksonCui
# @File : Test_Main.py
# @Software: PyCharm
import pytest,sys
from Project.Common.Utils import Utils
from Project.Common.DoConfig import DoConf
from Project.Common.DoRequests import DoRequests
from Project.Common.DoAssert import DoAssert
from Project.Common.FilePath import CaseFile_path
from Project.Common.Dologs import Logger

# 日志
logger = Logger()
class CasePrepare():
    def __init__(self):
    # 准备用例数据
        logger.info('Preparing case data')
        self.conf = DoConf()
        self.server = self.conf.get_value_from_section('project', 'server')
        self.sheetname_list = self.conf.get_value_from_section('RunningConfig','sheetname')

        self.ui_sheetname = Utils.spilt_sheet(self.sheetname_list,'ui_')
        self.api_sheetname = Utils.spilt_sheet(self.sheetname_list,'api_')
        self.tag_list = self.conf.get_value_from_section('RunningConfig','Tag').split(',')
        self.tag = Utils.get_eval('tag',*self.tag_list)

        if self.api_sheetname != '':
            self.apiCaseinfo = eval(f'Utils.get_Caselist(CaseFile_path,"{self.api_sheetname}"{self.tag})')
            # 检查用例数据
            try:
                Utils.check_case_data(self.apiCaseinfo)
            except:
                logger.exception("execute task failed. the exception as follows:")
        else:
            self.apiCaseinfo = []
            logger.info('='*5+'  API test is not selected this time  '+'='*5)
        if self.ui_sheetname != '':
            self.UICaseinfo = eval(f'Utils.get_Caselist(CaseFile_path,"{self.ui_sheetname}"{self.tag})')
            # 检查用例数据
            try:
                Utils.check_case_data(self.UICaseinfo)
            except:
                logger.exception("execute task failed. the exception as follows:")
        else:
            self.UICaseinfo = []
            logger.info('=' * 5 + '  UI test is not selected this time  ' + '=' * 5)

CP = None
var = None
#开始测试
class Test_Main():
    global CP
    global var
    CP = CasePrepare()
    # 用户自定义变量栈

    var = {}
    def setup_class(self):
        # 准备用例数据
        global CP
        global var
        CP = CasePrepare()
        # 用户自定义变量栈
        var = {}
    @pytest.mark.api
    @pytest.mark.parametrize('caseInfo', CP.apiCaseinfo)
    def test_api(self, caseInfo):
        #URL合成
        url = CP.server + caseInfo['uri']
        logger.info('Preparing session...')
        #session准备
        session_list = Utils.get_session_list(caseInfo['session'])

        #根据excel表决定是否带session
        DR = DoRequests(CP.server,session_list)
        #将自定义变量栈中的变量全部赋值到本次用例中
        logger.info('User defined variable is putting in Stack...')
        caseInfo['TestData'] = Utils.put_Vars(caseInfo['TestData'],var)
        #接收请求响应
        logger.info('Receiving response...')
        resp = DR.do_Request(url,caseInfo['TestData'],caseInfo['Method'],caseInfo['headers'])
        #将本次用例的响应结果添加到自定义变量栈中
        var.update(Utils.get_Vars(resp,caseInfo['variable']))
        #断言
        logger.info('asserting...')
        DoAssert.doAssert(Utils.get_dict_value(caseInfo['Expect']), Utils.getJsonPathValue(resp,Utils.get_dict_key(caseInfo['Expect'])),caseInfo['AssertType'])
        logger.info(f'{caseInfo["CaseID"]} Finished')
    @pytest.mark.ui
    @pytest.mark.parametrize('caseInfo', CP.UICaseinfo)
    def test_UI(self,caseInfo):

        __import__('Project.Common.UI_KeyWord')
        module = sys.modules["Project.Common.UI_KeyWord"]
        keyword_class = getattr(module, 'WebUIOperation')
        extractor_class = getattr(module, 'WebUIExtractor')

        # 分别执行所有关键字
        for Keyword_dic in caseInfo['TestKeyword']:
            keyword = Utils.get_dict_key(Keyword_dic)
            # IP合成
            if 'open_browser' not in keyword:
                args = Utils.get_dict_value(Keyword_dic)
            else:
                args = CP.server + Utils.get_dict_value(Keyword_dic)

            if hasattr(keyword_class, keyword):

                if hasattr(extractor_class, keyword):
                    Utils.UI_executer(args,extractor_class,keyword,var)

                else:
                    keyword_fun = getattr(keyword_class, keyword)
                    keyword_args = args.split(',')
                    args_list = []
                    # 去除参数中所有的空格
                    for i in keyword_args:
                        j = i.strip()
                        args_list.append(j)
                    # 将变量栈赋值到本次关键字函数的参数列表中
                    args_list = Utils.put_re_Vars(args_list, var)
                    # 运行关键字
                    # 无参数关键字
                    if keyword_args == [''] or keyword_args == []:
                        keyword_fun()
                    # 有参数关键字
                    else:
                        keyword_fun(*args_list)

            else:
                logger.exception(f'Your keyword {keyword} is not written correctly')
    def teardown_class(self):
        global CP
        global var
        del CP
        del var
if __name__ == '__main__':
    pytest.main(['vs',__file__])