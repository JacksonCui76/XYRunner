import pymysql
from Project.Common.DoConfig import DoConf
from pymysql.cursors import SSDictCursor
from Project.Common.Dologs import Logger

# 日志
logger = Logger()



class DoDatabase():

    def __init__(self,charset='utf8', cursorType=None):
        self.conf = DoConf()
        DBconfig = self.conf.get_db_config()
        host, username, pwd, database, port = DBconfig
        try:
            self.conn = pymysql.connect(host=host, port=port, user=username, password=pwd, database=database,
                                    charset=charset)
        except:
            logger.exception('Database parameter error!!')
        # 指定游标的类型
        cursor = None
        if cursorType == None:
            cursor = None
        elif cursorType == 'dict':
            cursor = SSDictCursor

        # 创建游标
        self.cur = self.conn.cursor(cursor)

    # 增 删 改
    def change_db(self, sql):
        # 建立连接

        # 执行sql语句
        rest = self.cur.execute(sql)

        # 提交事务
        self.conn.commit()
        # self.cur.close()
        # self.conn.close()
        return rest

    # 查询语句
    def select_db(self, sql, method='all'):
        self.cur.execute(sql)

        # 获取数据
        rest = None
        if method == 'all':
            rest = self.cur.fetchall()
        elif method == 'one':
            rest = self.cur.fetchone()
        # self.cur.close()
        # self.conn.close()
        return rest

    def excute_sql(self,sql):
        num = self.cur.execute(sql)
        return num

    def DML(self,sql):
        self.cur.execute(sql)
        self.conn.commit()


    def __del__(self):
        # 关闭连接对象
        try:
            self.cur.close()
            self.conn.close()
        except:
            logger.exception('Please check the database parameters!!')
# if __name__ == '__main__':
#     DB = DoDatabase()
