from orm_db.orm_db_mysql import Models, IntegetFiled, StringFiled

"""
@author RansySun
@create 2019-10-04-10:36
"""


# 1创建用具表
class UserInfo(Models):
    # 自定义表名
    table_name = 'UserInfo'

    # 定义字段
    user_id = IntegetFiled(name='user_id', primary_key=True)
    user_name = StringFiled(name='user_name')
    user_pwd = StringFiled(name="user_pwd")
    is_vip = IntegetFiled(name='is_vip')
    is_locked = IntegetFiled(name='is_locked')
    user_type = StringFiled(name='user_type')
    register_time = StringFiled(name='register_time')


# 创建电影表
class Movie(Models):
    table_name = 'Movie'

    movie_id = IntegetFiled('movie_id', primary_key=True)
    movie_name = StringFiled(name='movie_name')
    is_free = IntegetFiled(name='is_free')
    is_delete = IntegetFiled(name='is_delete')
    file_md5 = StringFiled(name='file_md5')
    path = StringFiled(name='path')
    movie_size = StringFiled(name='movie_size')
    upload_time = StringFiled(name='upload_time')
    user_id = IntegetFiled(name='user_id')


# 公告表
class Notice(Models):
    table_name = 'Notice'

    n_id = IntegetFiled(name='n_id', primary_key=True)
    title = StringFiled(name='title')
    content = StringFiled(name='content')
    create_time = StringFiled(name='create_time')
    user_id = IntegetFiled(name='user_id')


# 下载记录表
class DownloadRecord(Models):
    table_name = 'DownloadRecord'

    download_id = IntegetFiled(name='download_id', primary_key=True)
    user_id = IntegetFiled(name='user_id')
    movie_id = IntegetFiled(name='movie_id')
    download_time = StringFiled(name='download_time')

