from orm_db.orm_contromysql import MySql

"""
@author RansySun
@create 2019-10-04-10:38
"""


class Filed:
    """
    生成表中对应的字段约束
    """

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        # print(default)
        self.default = default


class IntegetFiled(Filed):
    """
    与表中对应的整型类型字段
    """

    def __init__(self, name, column_type='int', primary_key=False, default=0):
        super().__init__(name, column_type, primary_key, default)


class StringFiled(Filed):
    """
    与表中对应的字符串类型字段
    """

    def __init__(self, name, column_type='varchar(250)', primary_key=False, default=None):
        super().__init__(name, column_type, primary_key, default)


class OrmMetaClass(type):
    def __new__(cls, class_name, class_base, class_dic):
        """
        控制数据库中表的约束和字段的封装
        :param class_name:
        :param class_base:
        :param class_dic:
        :return:
        """
        if class_name == 'Models':
            return type.__new__(cls, class_name, class_base, class_dic)
        # print(class_dic)

        # 数据库中的表名
        table_name = class_dic.get('table_name', class_name)

        # 数据库中主键字段的名称
        primary_key_name_id = None

        # 数据库中的所有字段
        mappings = {}

        # 与数据库中对应的字段封装起来，
        for field_name, filed_obj in class_dic.items():
            if isinstance(filed_obj, Filed):
                mappings[field_name] = filed_obj

                # 判断是否只有一个主键
                if filed_obj.primary_key:

                    # 判断只有一个主键
                    if primary_key_name_id:
                        raise TypeError("只能有一个主键")

                    primary_key_name_id = filed_obj.name

        # 判断必须有一个主键
        if not primary_key_name_id:
            raise TypeError('必须有一个主键')

        # 过滤重复的字段名
        for field_name in mappings.keys():
            class_dic.pop(field_name)

        # 将字段添加到名称空间中
        class_dic['table_name'] = table_name
        class_dic['primary_key_name_id'] = primary_key_name_id
        class_dic['mappings'] = mappings
        # print(class_dic)
        return type.__new__(cls, class_name, class_base, class_dic)


class Models(dict, metaclass=OrmMetaClass):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def __setattr__(self, key, value):
        """
        重写，让字段的字段 = 赋值
        :param key:
        :param value:
        """
        self[key] = value

    def __getattr__(self, item):
        """
        通过.可以获取值
        :param item:
        :return:
        """
        return self.get(item)

    @classmethod
    def sql_select(cls, **kwargs):
        """
        sql查询语句，有条件和没有条件查询
        :param kwargs: 条件，支持一个条件
        :return:  返回结果对象
        """
        mysql_obj = MySql()

        # 判断查询是否有条件
        if not kwargs:
            # select * from 表名
            sql = 'select * from %s' % cls.table_name
            sql_data = mysql_obj.select(sql)

        else:

            # select * from 表名 where 字段名 = 值（添加） kwargs.keys()[0]==>不能直接取值，因为他是key对象

            filed_name = list(kwargs.keys())[0]
            filed_value = kwargs.get(filed_name)

            sql = 'select * from %s where %s= ?' % (cls.table_name, filed_name)
            sql = sql.replace('?', '%s')

            # 获取数据---->dict
            sql_data = mysql_obj.select(sql, filed_value)

        # 关闭连接
        mysql_obj.close()
        return [cls(**s) for s in sql_data]

    def sql_save(self):
        """
        数据库插入保存数据
        """
        mysql_obj = MySql()

        # 字段名
        filed_name_list = []

        # 字段值
        filed_value_list = []

        # ?占位符，防止sql注入
        replace_list = []

        # 获取字段名，字段值
        for filed_name, filed_obj in self.mappings.items():
            filed_name_list.append(filed_name)

            filed_value_list.append(
                # filed_obj.name：如果不存在他触发的是__getattr__，获取一个返回值None
                getattr(self, filed_obj.name, filed_obj.default)  # 通过反射获取字段名
            )

            replace_list.append('?')

        # 拼接sql insert into 表名(字段值) values(值)
        sql = 'insert into %s(%s) values (%s)' % (self.table_name, ','.join(filed_name_list), ','.join(replace_list))
        sql = sql.replace('?', '%s')

        # print(filed_name_list)
        # print(filed_value_list)
        # print(sql)

        mysql_obj.execute(sql, filed_value_list)
        mysql_obj.close()

    def sql_update(self):
        """
        修改内容
        """
        mysql_obj = MySql()

        # 字段名
        filed_name_list = []

        # 字段值
        filed_value_list = []

        # 获取条件名key的值
        primary_key_value = None

        # 获取字段名，字段值，条件
        for filed_name, filed_obj in self.mappings.items():
            filed_name_list.append(f'{filed_name}=?')
            filed_value_list.append(
                getattr(self, filed_obj.name, filed_obj.default)
            )

            # 获取主键值
            if filed_obj.primary_key:
                primary_key_value = getattr(self, filed_obj.name, filed_obj.default)

        # print(filed_name_list)
        # print(filed_value_list)
        # print(primary_key_value)

        # 拼接sql语句 update 表名 set 字段名=值 where id = 值
        # UserInfo set user_id=%s,user_name=%s,user_pwd=%s where user_id=None

        sql = 'update %s set %s where %s=%s' % (
            self.table_name,
            ','.join(filed_name_list),
            self.primary_key_name_id,
            primary_key_value
        )

        sql = sql.replace('?', '%s')
        # print(sql)

        # 修改数据
        mysql_obj.execute(sql, filed_value_list)


class UserInfo(Models):
    table_name = 'UserInfo'
    user_id = IntegetFiled(name='user_id', primary_key=True)
    user_name = StringFiled('user_name')
    user_pwd = StringFiled('user_pwd')


if __name__ == '__main__':
    user = UserInfo()
    user.sql_save()
    pass
# user = UserInfo.sql_select(user_name='randy')
# print(user)
# print(user[0].user_name)
#
#     user_insert = UserInfo(
#         user_name='test1',
#         user_pwd='123'
#     )
#     user_insert.sql_save()
#
#     # user_update = UserInfo()
#     # user_update.sql_update()
#
#     # user_update = UserInfo.sql_select(user_id=4)[0]
#     # user_update.user_name = '升级版randy'
#     # user_update.user_pwd = '123'
#     # user_update.sql_update()
#     # print(user.user_name)
#     # print(id(user.user_name))
#     # user['user_name'] = 'randysun'
#     # print(user.user_name)
#     # print(id(user.user_name))
#
#     # model = Models(user_name='randy')
#     #
#     # print(id(model.get('user_name')))
#     # print(model.user_name)
#     # model.user_name = 'randysun'
#     # print(id(model.get('user_name')))
#     # print(model.user_name)
