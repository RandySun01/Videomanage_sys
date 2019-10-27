import pymysql

"""
@author RansySun
@create 2019-10-04-10:38
"""


class MySql:
    """
    对数据库、增删改查封装
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        :param args:
        :param kwargs:
        :return:
        """
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self):
        """
        创建数据连接
        """
        self.mysql = pymysql.connect(
            user='root',
            passwd='root',
            charset='utf8',
            db='db_orm',
            autocommit=True
        )

        self.cursor = self.mysql.cursor(pymysql.cursors.DictCursor)

    def select(self, sql, args=None):
        """
        查询
        :param sql: 查询语句
        :param args: 条件
        :return: 返回查询结果集--->字典
        """
        print(f'\033[31m sql: {sql}\033[0m')
        print(f'\033[34m sql-args: {args}\033[0m')

        self.cursor.execute(sql, args)  # 提交sql语句
        res_data = self.cursor.fetchall()  # 查询结果
        return res_data

    def execute(self, sql, args=None):
        """
        增、删、改
        :param sql: 增、删、改sql
        :param args: 参数，防止sql注入
        """
        try:
            print(f'\033[31m sql: {sql}\033[0m')
            print(f'\033[34m sql-args: {args}\033[0m')
            # [None, 'test1', '123'],为什么会有None,因为有一个id字段，所以为None


            # insert into 表名(字段名) values(值)
            self.cursor.execute(sql, args)  # 提交sql语句

        except Exception as e:
            print(f'\033[31m sql错误: {e}\033[0m')

    def close(self):
        """
        关闭数据的连接
        """
        self.cursor.close()
        self.mysql.close()
