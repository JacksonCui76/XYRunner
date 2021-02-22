# -*- coding: utf-8 -*-
# @Time : 2021\1\15 0015 14:32
# @Author : JacksonCui
# @File : DoRequests.py
# @Software: PyCharm
import requests
from Project.Common.Utils import Utils
from Project.Common.Dologs import Logger

# 日志
logger = Logger()

class DoRequests:
    def __init__(self, server, session_list):
        self.server = server
        self.session_list = session_list #[{'uri':'/b2c/validcode.do','method':'GET','data':{'vtype':'memberreg'},{..},{..}] or None
        self.session = None
        self.isSession()
        # print('session_list>>',session_list)
    def isSession(self):
        if self.session_list is None:
            self.session = requests
        else:
            self.session = requests.session()

        for session in self.session_list: # session = {'uri':'/b2c/validcode.do','method':'GET','data':{'vtype':'memberreg'}
            if session['method'] in ('GET', 'get', 'Get'):
                r = self.session.get(url=self.server+session['uri'], params=session['data'])
            elif session['method'] in ('POST', 'post', 'Post'):
                r = self.session.post(url=self.server+session['uri'], data=session['data'])
    def Requests_json(self, url, params, Request_Method, headers=None):
        """

        :param Request_Method:请求方法 str
        :param headers:请求头 字典
        :param url: url,地址 str
        :param params: 请求参数 字典
        :return: json响应字典
        """

        sess = self.session

        if Request_Method.lower() in ('get', 'g'):
            resp = sess.get(url=url, params=params, headers=headers)
        elif Request_Method.lower() in ('post', 'po'):
            resp = sess.post(url=url, data=params, headers=headers)
        elif Request_Method.lower() in ('put', 'pu'):
            resp = sess.put(url=url, data=params, headers=headers)
        elif Request_Method.lower() in ('delete', 'del'):
            resp = sess.delete(url=url, params=params, headers=headers)

        else:
            logger.exception('Your request method is wrong')
        try:
            return resp.json()
        except:
            logger.exception('Your request did not return a JSON string')

    def Post_File(self, url, params, Request_Method, headers=None):
        """
        :param url: Request_Method:请求方法 str
        :param params: params: excel表处理过后的请求参数 字典
        :param files:文件参数，字典
        :param Request_Method:请求方法
        :param headers:
        :return:
        """
        if headers is None:
            headers = {'Content-Type': 'multipart/form-data'}

        # 处理参数
        paramsData, files = Utils.get_post_parma(params)
        # 发送请求
        sess = self.session
        if Request_Method.lower() in ('postfile', 'pt', 'post_file'):
            resp = sess.post(url=url, files=files, params=paramsData, headers=headers)

        else:
            logger.exception('Your request method is wrong')
        return resp.json()

    def do_Request(self, url, TestData, Method, headers):
        if headers:
            if Method.lower() not in ('postfile', 'pf', 'post_file'):
                resp = self.Requests_json(url, TestData, Method, headers=headers)
            else:

                resp = self.Post_File(url, TestData, Method, headers=headers)
        else:
            if Method.lower() not in ('postfile', 'pf', 'post_file'):
                resp = self.Requests_json(url, TestData, Method)
                print(resp)
            else:
                resp = self.Post_File(url, TestData, Method)
        try:
            return resp
        except:

            logger.exception('Your request did not return a JSON string')


# if __name__ == '__main__':
#     data = [{'CaseID': '0001', 'Version': 'V1.0', 'Method': 'GET', 'uri': '/cinema-stage/admin/login',
#              'headers': {'content-type&application/json; charset': 'UTF-8'}, 'Tag': 'login', 'Description': '正确的数据登录',
#              'TestData': {'username': 'Wanda', 'password': '123456'}, 'session': {'Get': '/cinema-stage/admin/login'},
#              'SessionData': {'username': 'Wanda', 'password': '123456'}, 'Expect': {'code': 'success'},
#              'AssertType': 'response', 'variable': {'@{code}': '$.code'}},
#             {'CaseID': '0002', 'Version': 'V1.0', 'Method': 'GET', 'uri': '/cinema-stage/admin/login', 'headers': None,
#              'Tag': 'login', 'Description': '错误的用户名登录', 'TestData': {'username': '@{code}', 'password': '123457'},
#              'session': {'Get': '/cinema-stage/admin/login'},
#              'SessionData': {'username': 'Wanda', 'password': '123456'}, 'Expect': {'object': 'None'},
#              'AssertType': 'None', 'variable': None},
#             {'CaseID': '0003', 'Version': 'V1.0', 'Method': 'GET', 'uri': '/orders/profile/orders/selectOrderWeek',
#              'headers': None, 'Tag': 'selectOrderWeek', 'Description': '正常访问营业额统计', 'TestData': None,
#              'session': {'Get': '/cinema-stage/admin/login'},
#              'SessionData': {'username': 'Wanda', 'password': '123457'}, 'Expect': {'finish': '1'},
#              'AssertType': 'length', 'variable': None},
#             {'CaseID': '0004', 'Version': 'V1.0', 'Method': 'postfile', 'uri': '/cinema-stage/admin/uploadpics',
#              'headers': {'Content-Type': 'multipart/form-data'}, 'Tag': 'uploadpics', 'Description': '正常上传影院图片',
#              'TestData': {'id': '1',
#                           'file1': 'pic0,007.png,C:/Users/Administrator/Desktop/woniuticket/CaseFile/007.png,image/png',
#                           'file2': 'pic1,008.png,C:/Users/Administrator/Desktop/woniuticket/CaseFile/008.png,image/png'},
#              'session': {'Get': '/cinema-stage/admin/login'},
#              'SessionData': {'username': 'Wanda', 'password': '123458'}, 'Expect': {'code': 'success'},
#              'AssertType': 'response', 'variable': None}
#             ]
#     sessionUrl = 'http://192.168.16.179:14200' + data[0]['uri']
#     sessionMethod = Utils.get_dict_key(data[0]['session'])
#     SessionData = data[0]['SessionData']
#     isSession = Utils.get_dict_value(data[0]['session'])
#     # 根据excel表决定是否带session
#     DR = DoRequests(sessionUrl, sessionMethod, SessionData, isSession)
#
#     url = 'http://192.168.255.64:14200' + data[3]['uri']
#     resp = DR.do_Request(url, data[3]['TestData'], data[3]['Method'],
#                          {'Content-Type': 'image/png'})

"""
使用多个参数上传多个文件的时候，参数的组装形式

file = {
"pic": ("kejian.ppt", open(r"C:\课件\课件模板.ppt", "rb"), "text/txt"),

"pic2": ("lmb.png", open("lmb.png", "rb"), "text/txt")

}

同一个参数上传多个文件的时候，参数的组装形式

files = [

("pic", ("kejian.ppt", open(r"C:\课件\课件模板.ppt", "rb"), "text/txt")),

("pic", ("lmb.png", open("lmb.png", "rb"), "text/txt")),

]
"""
