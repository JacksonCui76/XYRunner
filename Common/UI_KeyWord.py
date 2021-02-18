# -*- coding: utf-8 -*-
# @Time : 2021\1\18 0018 15:24
# @Author : JacksonCui
# @File : UI_KeyWord.py
# @Software: PyCharm
import time
from selenium import webdriver
from Project.Common.Utils import Utils
from Project.Common.FilePath import img_path
from Project.Common.DoDatabase import DoDatabase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from Project.Common.Dologs import Logger

# 日志
logger = Logger()
'''
    ID = "id"
    XPATH = "xpath"
    LINK_TEXT = "link text"
    PARTIAL_LINK_TEXT = "partial link text"
    NAME = "name"
    TAG_NAME = "tag name"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"
'''


class WebUIExtractor:
    # driver = webdriver.Chrome()
    driver = None
    now_handle = None
    DB = DoDatabase()

    def __init__(self):
        pass

    @classmethod
    def get_page_source(cls):
        return cls.driver.page_source

    @classmethod
    def get_page_title(cls):
        return cls.driver.title

    @classmethod
    def get_element_text(cls, by, value):
        ele = cls.driver.find_element(by, value)
        return ele.text


class WebUIOperation(WebUIExtractor):

    @classmethod
    def get_url(cls, url):
        cls.driver.maximize_window()
        cls.driver.get(url)
        cls.driver.implicitly_wait(10)
        cls.now_handle = cls.driver.current_window_handle

    @classmethod
    def open_browser(cls, url, browser_name):
        if browser_name.lower() == 'ff' or browser_name.lower() == 'firefox':
            WebUIExtractor.driver = webdriver.Firefox()
            cls.driver = WebUIExtractor.driver
            cls.get_url(url)
        if browser_name.lower() == 'gc' or browser_name.lower() == 'chrome':
            WebUIExtractor.driver = webdriver.Chrome()
            cls.driver = WebUIExtractor.driver
            cls.get_url(url)

    @classmethod
    def findelement(cls, by, value, timeout=5, poll_frequenc=0.5):
        element = WebDriverWait(cls.driver, timeout, poll_frequenc).until(lambda driver: driver.find_element(by, value))
        return element

    @classmethod
    def findelements(cls, BY, value, index, timeout=15, POLL_FREQUENCY=0.5):
        """获取多个元素，指定其中一个元素"""
        element = WebDriverWait(cls.driver, timeout, POLL_FREQUENCY).until(
            lambda driver: driver.find_elements(BY, value))
        ele = element[int(index) - 1]
        return ele

    @classmethod
    def clicks(cls, BY, value, index):
        """筛选多元素再单点击"""
        cls.findelements(BY, value, index).click()

    @classmethod
    def input_text(cls, by, value, content):
        ele = cls.findelement(by, value)
        ele.clear()
        ele.send_keys(content)

    @classmethod
    def click(cls, by, value):
        ele = cls.findelement(by, value)
        ele.click()

    @classmethod
    def select_by_comment(cls, by, value, comment):
        ele = cls.findelement(by, value)
        Select(ele).select_by_value(comment)

    @classmethod
    def select_by_index(cls, by, value, index):
        ele = cls.findelement(by, value)
        Select(ele).select_by_index(index)

    @classmethod
    def img_screenshots(cls):
        cls.driver.save_screenshot(img_path + f'/{Utils.get_time()}')

    @classmethod
    def quit(cls):
        cls.driver.quit()

    @classmethod
    def wait(cls, t):
        try:
            t = int(t)
            time.sleep(t)
        except:

            logger.exception('Please enter the type of int in seconds')

    # js代码运行
    @classmethod
    def commit_js(cls, attrib, value, comment):
        """提交js业务"""
        js = None
        if attrib == 'id':
            js = f'document.getElementById("{value}").value="{comment}";'
        elif attrib == 'name':
            js = f'document.getElementByName("{value}").value="{comment}";'
        elif attrib == 'class name':
            js = f'document.getElementByClassName("{value}").value="{comment}";'
        elif attrib == 'tag name':
            js = f'document.getElementByTagName("{value}").value="{comment}";'
        cls.driver.execute_script(js)

    # 键鼠控制
    @classmethod
    def mouse_click(cls, by, value):
        ele = cls.findelement(by, value)
        webdriver.ActionChains(cls.driver).click(ele).perform()

    @classmethod
    def mouse_hold(cls, by, value):
        ele = cls.findelement(by, value)
        webdriver.ActionChains(cls.driver).move_to_element(ele).perform()

    # frame和窗口和警告框的切换
    @classmethod
    def switch_to_frame(cls, by, value):
        f = cls.findelement(by, value)
        cls.driver.switch_to.frame(f)

    @classmethod
    def switch_to_window(cls):
        handles = cls.driver.window_handles
        for i in handles:
            if i != cls.now_handle:
                cls.driver.switch_to.window(i)
                break

    # 点击警告弹窗的确定
    @classmethod
    def alert_accept(cls):
        cls.driver.switch_to.alert.accept()

    # confirm 有取消和确定按钮
    @classmethod
    def alert_dismiss(cls):
        cls.driver.switch_to.alert.dismiss()

    # prompt 在警告框内输入内容后点击确定
    @classmethod
    def alert_send_keys(cls, value):
        cls.driver.switch_to.alert.send_keys(value)
        cls.driver.switch_to.alert.accept()

    # 断言
    @classmethod
    def elementTextShouldBeContain(cls, by, value, ex_text):

        ele = cls.findelement(by, value)
        assert ex_text in ele.text

    @classmethod
    def pageSourseShouldBeContain(cls, ex_text):
        pagesource = cls.get_page_source()
        assert ex_text in pagesource

    @classmethod
    def elementShouldBeContain(cls, by, value):
        try:
            cls.findelement(by, value)
        except:
            logger.exception(f'Element with {by} as {value} was not found')

    # 数据库断言
    @classmethod
    def assertDB(cls, sql, length):
        """

        :param sql: sql查询语句
        :param length: 本次查询结果条数断言
        :return: fail or pass
        """
        try:
            length = int(length)
        except:
            logger.exception('Please enter 0 or a positive integer for the length parameter')
        rlt_len = cls.DB.excute_sql(sql)
        assert rlt_len == length

    # 数据库操作
    @classmethod
    def update(cls, sql):
        try:
            cls.DB.DML(sql)
        except:
            logger.exception(f'please check the sql:{sql}')