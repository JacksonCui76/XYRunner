# -*- coding: utf-8 -*-
# @Time : 2021\1\14 0014 10:18
# @Author : JacksonCui
# @File : Utils.py
# @Software: PyCharm
import re, time, jsonpath, random, sys
from Project.Common.DoExcel import DoExcel
from Project.Common.DoConfig import DoConf
from Project.Common.Dologs import Logger

# 日志
logger = Logger()


class Utils:
    # 获取当前时间
    @classmethod
    def get_time(cls):
        return time.strftime('%Y%m%d_%H%M', time.localtime())

    # 将字符串转换为字典
    @classmethod
    def chageTodict(cls, info):
        """

        :param info: 用例数据 字符串 mobile=18328070206&key=register
        :return:字典 {'username': 'password', 'Wanda': '123456'}
        """
        # logger.info(f'正在运行函数：{sys._getframe().f_code.co_name}')
        if '&' in info and '=' in info:
            key = []
            value = []
            key_value_list = info.strip().split('&') #['mobile=18328070206','key=register']
            for key_value in key_value_list:
                key += re.findall(r".*?(.*?)=", key_value)
                value += re.findall(r"=(.*)\n?", key_value)
        elif '(' in info and ')' in info:
            info_list = info.strip().split(
                '\n')  # info_list=['open_browser(/web/feng/backstage/login.html, Chrome)','get_page_source(@{name},<span>(x*?)</span>,@{pwd},<span>(x*?)</span>)']
            li_keyword = []

            for key_args in info_list:

                if '[' not in key_args and '//' not in key_args and '@{' not in key_args:
                    key_args_dict = {}
                    key = re.findall(r".*?(.*?)\(", key_args)[0]
                    value = re.findall(r"\((.*)\)", key_args)[0]
                    key_args_dict[key] = value
                    li_keyword.append(key_args_dict)

                elif '[' in key_args and '//' in key_args and '@{' not in key_args:
                    key_args_dict = {}
                    key = re.findall(r".*?(.*?)\(", key_args)[0]
                    value = re.findall(r"\((.*)\)", key_args)[0]
                    key_args_dict[key] = value
                    li_keyword.append(key_args_dict)


                elif '[' in key_args and '/' in key_args and '@{' not in key_args:
                    key_args_dict = {}
                    key = re.findall(r".*?(.*?)\(", key_args)[0]
                    value = re.findall(r"\((.*)\)", key_args)[0]
                    key_args_dict[key] = value
                    li_keyword.append(key_args_dict)
                elif '[' in key_args and '@{' in key_args:
                    key_args_dict = {}
                    key = re.findall(r".*?(.*?)\(\[", key_args)[0]
                    value = '[[' + re.findall(r"\(\[(.*)\]\)", key_args)[0] + ']]'
                    key_args_dict[key] = value
                    li_keyword.append(key_args_dict)

            return li_keyword
        else:
            key = re.findall(r".*?(.*?)=", info)
            value = re.findall(r"=(.*)\n?", info)

        if len(key) == 0 or len(value) == 0:
            return None
        di = {}
        for i in range(len(key)):
            di[key[i]] = value[i]
        return di

    # 将excel表每一行都转化为字典,通过列数转化
    @classmethod
    def get_Caselist_back(self, filepath, sheetname, **kwgs):
        """

        :param filepath: 用例文件路径 str
        :param sheetname: sheet名字 str
        :param kwgs: 需要转换为字典的测试数据的列数 例：col=7,col=8
        :return: 列表套字典[{}{}]
        [
        {'CaseID': '0001', 'Version': 'V1.0', 'Method': 'GET', 'uri': 'cinema-stage/admin/login', 'headers': 'content-type: application/json; charset=UTF-8', 'Tag': 'backstage,login', 'Description': '正确的数据登录', 'TestData': {'username': 'Wanda', 'password': '123456'}, 'Expect': 'code=success'},
        {'CaseID': '0002', 'Version': 'V1.1', 'Method': 'GET', 'uri': 'cinema-stage/admin/login', 'headers': 'content-type: application/json; charset=UTF-9', 'Tag': 'backstage,login', 'Description': '错误的密码登录', 'TestData': {'username': 'Wanda', 'password': '123457'}, 'Expect': 'code=fail'}
        ]


        """
        # 读取文件
        try:
            excel = DoExcel(filepath)
        except:
            logger.exception('execute task failed. the exception as follows:')
        # 获取sheet对象
        sheet_list = sheetname.strip().split(',')
        row = 0
        # 建立需要返回的列表
        new_li = []
        for sheet in sheet_list:
            try:
                locals()[sheet] = excel.get_sheet_by_name(sheet)
            except:
                logger.exception
                logger.exception(f'{sheet}Not exist!')
            # 获取行数
            rows = locals()[sheet].nrows

            # 遍历excel的每一行

            for row in range(1, rows):
                dict = {}
                li = locals()[sheet].row_values(row)
                # 取出首行
                title_list = locals()[sheet].row_values(0)
                # 遍历除了首行之外的所有行，只取出对应的tag
                # 将其与首行转化为与首行对应的字典
                for i in range(0, len(title_list)):
                    changeCol_list = []
                    for key, value in kwgs.items():
                        if 'col' in key:
                            try:

                                changeCol_list.append(int(value))
                            except:
                                logger.exception(
                                    'The format of the column you need to convert to a dictionary is incorrect')
                    if i in changeCol_list:
                        try:
                            TestData = Utils.chageTodict(li[i])

                            dict[title_list[i]] = TestData

                        except:
                            logger.exception('Your test data format is wrong')
                    else:
                        dict[title_list[i]] = li[i]

                # 全部测试数据已取出

                new_li.append(dict)
                # print(new_li)
        # 删除对应标签以外的用例
        expect = set()
        for key, value in kwgs.items():
            if 'tag' in key:
                expect.add(value)
        count = 0
        for j in range(0, len(new_li)):
            rlt = set(new_li[count]['Tag'].split('\n'))

            if expect & rlt == set() and expect != {''}:

                new_li.remove(new_li[count])
            elif expect == {''}:
                count += 1
            else:
                count += 1
        return new_li

    # 将excel表每一行都转化为字典,通过配置文件转化
    @classmethod
    def get_Caselist(self, filepath, sheetname, **kwgs):
        """

        :param filepath: 用例文件路径 str
        :param sheetname: sheet名字 str
        :param kwgs: 需要转换为字典的测试数据的列数 例：tag
        :return: 列表套字典[{}{}]
        [
        {'CaseID': '0001', 'Version': 'V1.0', 'Method': 'GET', 'uri': 'cinema-stage/admin/login', 'headers': 'content-type: application/json; charset=UTF-8', 'Tag': 'backstage,login', 'Description': '正确的数据登录', 'TestData': {'username': 'Wanda', 'password': '123456'}, 'Expect': 'code=success'},
        {'CaseID': '0002', 'Version': 'V1.1', 'Method': 'GET', 'uri': 'cinema-stage/admin/login', 'headers': 'content-type: application/json; charset=UTF-9', 'Tag': 'backstage,login', 'Description': '错误的密码登录', 'TestData': {'username': 'Wanda', 'password': '123457'}, 'Expect': 'code=fail'}
        ]


        """
        # logger.info(f'正在运行函数：{sys._getframe().f_code.co_name}')
        # 读取文件

        try:
            excel = DoExcel(filepath)
        except:
            logger.exception('execute task failed. the exception as follows:')
        # 获取sheet对象
        sheet_list = sheetname.strip().split(',')
        row = 0
        # 建立需要返回的列表
        new_li = []
        for sheet in sheet_list:
            try:
                locals()[sheet] = excel.get_sheet_by_name(sheet)
            except:
                logger.exception(f'{sheet}Not exist!!,DETAILS:')
            # 获取行数
            rows = locals()[sheet].nrows

            # 遍历excel的每一行

            for row in range(1, rows):
                dict = {}
                li = locals()[sheet].row_values(row)
                # 取出首行
                title_list = locals()[sheet].row_values(0)
                # 遍历除了首行之外的所有行，只取出对应的tag
                # 将其与首行转化为与首行对应的字典
                for i in range(0, len(title_list)):
                    dict[title_list[i]] = li[i]

                # 全部测试数据已取出
                for key, value in dict.items():
                    conf = DoConf()
                    if key in conf.get_value_from_section('comments', 'dictCol').split(','):
                        dictData = Utils.chageTodict(value)
                        dict[key] = dictData

                new_li.append(dict)
                # print(new_li)
        # 删除对应标签以外的用例
        expect = set()
        for key, value in kwgs.items():
            if 'tag' in key:
                expect.add(value)
        count = 0
        for j in range(0, len(new_li)):
            rlt = set(new_li[count]['Tag'].split('\n'))

            if expect & rlt == set() and expect != {''}:

                new_li.remove(new_li[count])
            elif expect == {''}:
                count += 1
            else:
                count += 1
        return new_li

    # 将配置文件中的tag和col转化为python语言
    @classmethod
    def get_eval(cls, tagname, *args):
        '''

        :param tagname: 需要传入参数的标签名 字符串 例如：tag,col
        :param args: 需要传入的具体值 字符串 'login','backstage'
        :return: 字符串 类似于',tag0=login,tag1=backstage'
        '''
        # logger.info(f'正在运行函数：{sys._getframe().f_code.co_name}')
        rlt = f",{tagname}0='{args[0]}',"
        for i in range(1, len(args)):
            rlt += f"{tagname}{i}='{args[i]}',"
        rlt = rlt[:-1]
        return rlt

    # 将sheet表中的api和UI分流
    @classmethod
    def spilt_sheet(cls, sheet_str, type):

        """

        :param sheet_str: 'api_backstage,api_feng,UI_backstage'
        :param type: str 'ui' or 'api'
        :return: str 'api_backstage,api_feng' or 'UI_backstage'
        """
        sheet_list = sheet_str.split(',')
        sheet_Str = ''
        for sheetName in sheet_list:
            if type in sheetName.lower():
                sheet_Str += sheetName + ','

        return sheet_Str[:-1]

    # 检查excel表的数据
    @classmethod
    def check_case_data(cls, Caselist):
        """
        检查excel表的数据是否填写错误
        :param Caselist: 测试数据
        :return: bool值
        """
        '''
        需要检查的字段：Method、uri、headers、Tag、TestData、session、SessionData、Expect、AssertType,varible      
        '''
        # logger.info(f'正在运行函数：{sys._getframe().f_code.co_name}')
        count = 0
        if len(Caselist[0]) > 11:
            for li in Caselist:

                # Method
                if li['Method'].lower() not in (
                'get', 'g', 'post', 'po', 'put', 'pu', 'delete', 'del', 'postfile', 'pt', 'post_file'):
                    logger.warning(f"No.{li['CaseID']}'s method is Wrong")
                    count += 1

                # uri
                elif re.findall('^/', li['uri']) != ['/']:
                    logger.warning(f"No.{li['CaseID']}'s uri Must start with '/'!")
                    count += 1

                # headers
                elif li['headers']:
                    if 'content-type' not in Utils.get_dict_key(li['headers']).lower():
                        logger.warning(
                            f"No.{li['CaseID']}'s request header must be separated with ':' or cancelled with 'headers = default'!")
                        count += 1

                # Tag
                elif li['Tag'].split('\n') == ['']:
                    logger.warning(f"No.{li['CaseID']}'s Unmarked tag will not be executed!")

                # TestData
                elif type(li['TestData']) != dict and li['TestData'] is not None:
                    logger.warning(f"No.{li['CaseID']}'s TestData Not converted to dictionary or not empty!")
                    count += 1

                # Expect
                elif type(li['Expect']) != dict and li['Expect'] is not None:
                    logger.warning(
                        f"No.{li['CaseID']}'s Expect Not converted to dictionary, please check the configuration file and select the corresponding column!")
                    count += 1

                # AssertType
                elif li['AssertType'] not in ('response', 'None', 'length', 'rp', 'len') and li['AssertType'] is not None:
                    logger.warning(f"No.{li['CaseID']}'s AssertType method is wrong !!")
                    count += 1

                # varible
                elif type(li['variable']) != dict and li['variable'] is not None:
                    logger.warning(f"No.{li['CaseID']}'s TestData Not converted to dictionary or not empty!")
                    count += 1
        else:
            for li in Caselist:
                if type(li['TestKeyword']) != list:
                    logger.warning(f"No.{li['CaseID']}'s TestKeyword Not converted to dictionary or not empty!")
                    count += 1

        if count == 0:
            logger.info('=' * 10 + '  The test data is basically correct, and the test is about to start  ' + '=' * 10)
        else:
            logger.exception(f"A total of {count} cells format error, please modify!")

    # 获取字典的No.一个值
    @classmethod
    def get_dict_value(cls, dic):
        if type(dic) == dict:
            return list(dic.values())[0]
        else:
            return ''

    # 获取字典No.一个键
    @classmethod
    def get_dict_key(cls, dic):
        if type(dic) == dict:
            return list(dic.keys())[0]
        else:
            return ''

    # 获取postfile的参数
    @classmethod
    def get_post_parma(cls, Testdata):
        """

        :param Testdata: excel表里Testcase字段转换后的字典
        :return:两个字典 postfile的params，files
        """
        # logger.info(f'正在运行函数：{sys._getframe().f_code.co_name}')
        # 数据检测
        if Testdata:
            params = {}
            files = {}
            for key, value in Testdata.items():
                if ',' in value:
                    li = value.split(',')
                    try:
                        files[li[0]] = (li[1], open(li[2], "rb"), li[3])
                    except:
                        logger.exception(
                            'Your postfile request parameter is wrong, please refer to the field description')
                else:
                    params[key] = value
        else:
            logger.exception('No parameters were added to your postfile request')
        return params, files

    # 通过jsonpath获取用户自定义变量键值
    @classmethod
    def get_Vars(cls, resp, varible):
        """

        :param resp: 本次请求后获取的响应 字典
        :param varible: excel表单独的一行varible字段的字典
        :return: {'变量名':'值'} 字典
        """
        '''
        resp = {'code':'success',
            'list':{
                'zhangdan':{'code':'success1','asd':2},
                'lisi':{'code':'success2', 'asd':4},
                    }
                }

        varible = {'@{code}':'$.code'}
        var_dict = {'code': 'success2', 'message': False}
        '''
        # 建立需要返回的字典
        var_dict = {}
        if varible:
            for Var, JP in varible.items():
                try:
                    JP = str(JP)
                    R_Value = jsonpath.jsonpath(resp, JP)

                    if jsonpath.jsonpath(resp, JP):
                        var_dict[Var] = jsonpath.jsonpath(resp, JP)[random.randint(0, len(R_Value) - 1)]
                    else:
                        var_dict[Var] = jsonpath.jsonpath(resp, JP)
                except:
                    logger.exception(f'{JP} is wrong!!')
        return var_dict

    # 将用户自定义变量赋值到用例的测试数据中
    @classmethod
    def put_Vars(cls, Testdata, Var):
        """

        :param Testdata:  {'username': '&{code}', 'password': '123457'} 每一条测试数据 字典
        :param Var:{'&{code}': 'success', '&{message}': False} 用户自定义变量栈
        :return:{'username': 'success', 'password': '123457'}
        """
        if Testdata is not None:
            for T_key, T_value in Testdata.items():
                for V_key, V_value in Var.items():
                    if T_value == V_key:
                        Testdata[T_key] = V_value
        return Testdata

    # 通过jsonpath获取期望位置
    @classmethod
    def getJsonPathValue(cls, resp, JP):
        """

        :param jsonpath: str jsonpath
        :param resp 结果响应 字典
        :return: value str
        """

        if JP:
            R_value = None
            try:
                JP = str(JP)
                value = jsonpath.jsonpath(resp, JP)
            except:
                logger.exception(f'Please check the response>>{resp}\njsonpath>>{JP}')
            if value:
                R_value = value[random.randint(0, len(value) - 1)]
                return R_value
            else:
                return R_value

    # 通过正则表达式获取用户自定义变量键值
    @classmethod
    def get_re_Vars(cls, resp, varible):
        """

        :param resp: 本次请求后获取的响应 字符串
        :param varible: args_list 列表 [['@{name}','<span>(x*?)</span>'],['@{pwd}','<span>(x*?)</span>']]
        :return: var_str = 字典
        """
        '''
        resp = 页面源码
        varible = ['@{neme}','re表达式']
        var_dict = {'@{name}': 'success', '@{message}': False}
        '''
        # 将列表转化为字典
        try:
            varible = dict(varible)
        except:
            logger.exception(f'{varible} is wrong!!')
        # 建立需要返回的字典
        var_dict = {}
        if varible:

            for Var, RP in varible.items():
                R_Value = []
                R_V = re.findall(RP, resp)
                R_Value.append(R_V[random.randint(0, len(R_V) - 1)])
                if R_Value != [] and R_Value != ['']:

                    var_dict[Var] = re.findall(RP, resp)
                else:
                    var_dict[Var] = False
            return var_dict

    @classmethod
    def put_re_Vars(cls, args_list, Var):
        """

        :param args_list:列表 ['id','login-username','@{code}']

        :param Var:{'@{code}': '123', '@{message}': False} 用户自定义变量栈
        :return:列表 ['id','login-username','123']
        """
        R_args_list = []
        for args in args_list:
            if args in Var:
                if Var[args]:
                    R_args_list.append(Var[args])
                else:
                    R_args_list.append(args)
            else:
                R_args_list.append(args)
        return R_args_list

    @classmethod
    def UI_executer(cls, args, extractor_class, keyword, var):
        """

        :param args: 参数列表 字符串
        :param extractor_class UI提取器类对象
        :param keyword 用户excel表内写的UI关键字 字符串
        :param var: 用户自定义变量栈 字典
        :return: R_var 更新后的字典 字典
        """
        # logger.info(f'正在运行函数：{sys._getframe().f_code.co_name}')
        # 检查关键字是否正确
        extractor_fun = getattr(extractor_class, keyword)
        if keyword == 'get_page_source':
            try:
                args = eval(args)
            except:
                logger.exception(f'{args} is wrong!!')
            # 正则提取器
            resp = extractor_fun()
            # 将本次用例的页面源码通过正则表达提取结果添加到自定义变量栈中
            var.update(Utils.get_re_Vars(resp, args))
            return var
        elif keyword == 'get_page_title':
            # args = '@{title}'
            # 获取首页title
            try:
                resp = extractor_fun()
            except:
                resp = None
            # 建立需要更新的字典
            resp_dict = {}
            resp_dict[args] = resp
            # 将本次用例的页面标题添加到自定义变量栈中
            var.update(resp_dict)
            return var
        elif keyword == 'get_element_text':
            # args = '[[\'@{order}\',\'xpath\',\'//span[@class="order-id"\',\'.*?(\\d+).*?\']，[\'@{order}\',\'xpath\',\'//span[@class="order-id"\',\'.*?(\\d+).*?\']]'
            try:
                args = eval(
                    args)  # [[\'@{order}\',\'xpath\',\'//span[@class="order-id"\',\'.*?(\\d+).*?\'],[\'@{order_1}\',\'xpath\',\'//span[@class="order"\',\'.*?(\\d+).*?\']]
            except:
                logger.exception(f'{args} is wrong!!')
            # 建立列表
            R_var = {}  # {"@{order}":"613215","@{order_1}":None}
            for args_list in args:
                # args_list = [\'@{order}\',\'xpath\',\'//span[@class="order-id"\',\'.*?(\\d+).*?\']
                # 已找到的页面text
                try:
                    text = extractor_fun(args_list[1], args_list[2])
                except:
                    logger.exception('Please check the positioning method and the specific value')
                R_text = re.findall(args_list[-1], text)
                if R_text != [] and R_text != ['']:
                    resp = R_text[random.randint(0, len(R_text) - 1)]
                    R_var[args_list[0]] = resp
                else:
                    R_var[args_list[0]] = False
            var.update(R_var)
            return var

    @classmethod
    def get_session_list(cls,session_str):
        """
        将excel表中的session字段内的内容转化列表
        :param session_str: session字符串 ：/b2c/validcode.do##GET##vtype=memberreg\n/b2c/api/shop/sms/sms-safe.do##GET##_=1612860762883\n/b2c/api/shop/sms/send-sms-code.do##POST##mobile=18328070206&key=register
        :return:R_session_list 列表: [{'uri':'/b2c/validcode.do','method':'GET','data':{'vtype':'memberreg'}},{},{}]
        """
        if session_str:
            R_session_list = []
            session_list = session_str.strip().split('\n')   #['/b2c/validcode.do##GET##vtype=memberreg',...]

            for session_value in session_list: #session_value = '/b2c/validcode.do##GET##vtype=memberreg'
                R_dict = {}
                dict_value_list = session_value.strip().split('##')  #dict_value_list= ['/b2c/validcode.do','GET','vtype=memberreg']

                R_dict['uri'] = dict_value_list[0]
                R_dict['method'] = dict_value_list[1]
                R_dict['data'] = Utils.chageTodict(dict_value_list[2])
                R_session_list.append(R_dict)
            return R_session_list
        else:
            return None
# if __name__ == '__main__':
#     r = Utils.chageTodict('mobile=18328070206&key=register')
#     print(r)
#     r = Utils.get_session_list('/b2c/validcode.do##GET##vtype=memberreg\n/b2c/api/shop/sms/sms-safe.do##GET##_=1612860762883\n/b2c/api/shop/sms/send-sms-code.do##POST##mobile=18328070206&key=register')
#     print(r)
#     #测试postfile参数函数
#     # data = {'id': '4', 'file1': 'pic0,01.png,C:/Users/Administrator/Desktop/woniuticket/CaseFile/006.png,image/png', 'file2': 'pic1,01.png,C:/Users/Administrator/Desktop/woniuticket/CaseFile/007.png,image/png'}
#     # p,f = Utils.get_post_parma(data)
#     # print('p>>',p)
#     # print('f>>',f)
#     print(Utils.get_time())
# 测试获取变量
# args_list= ['id','login-username','@{message}']
# resp = {'@{code}': '123', '@{message}': 'False'}
# print(Utils.put_re_Vars(args_list,resp))
# import os
# r = Utils.get_Caselist_backup(os.path.dirname(os.path.dirname(__file__)) + r'/CaseFile/casefile.xlsx','api_backstage',tag0='login')
# print(r)
# print(len(Utils.get_Caselist(os.path.dirname(os.path.dirname(__file__)) + r'/CaseFile/woniuticket.xlsx','api_backstage',tag0='uploadpics',tag1='login',tag2='selectOrderWeek',col1=4,col2=7,col3=8,col4=9,col5=10,col6=12)))
# print(Utils.chageTodict('content-type&application/json; charset=UTF-8'))
# a = Utils.spilt_sheet('api_backstage,api_feng,UI_backstage','ui_')
# print(a)
# resp = {'code':'success',
#         'list':{
#             'zhangdan':{'code':'success1','asd':'2'},
#             'lisi':{'code':'success2', 'asd':'4'},
#                 }
#             }
# JP = '$.code'
# a = Utils.getJsonPathValue(resp,JP)
# print(a)
# a = "get_element_text(['@{order}','xpath','//span[@class=\"order-id\"','.*?(\d+).*?'],['@{order_1}','xpath','//span[@class=\"order-id\"','.*?(\d+).*?'])"
# b = Utils.chageTodict(a)
# print(b)