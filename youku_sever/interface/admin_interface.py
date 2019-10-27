from lib import common
from db import Models
import datetime
import os
from threading import Lock
from db import user_data
from interface import common_interface
from conf import settings

"""
@author RansySun
@create 2019-10-04-10:36
"""
lock = Lock()

lock.acquire()

user_data.mutex = lock

lock.release()


def register_interface(back_dic, conn):
    """
    用户注册接口
    :param bacd_dic:
    :param conn:
    """
    username = back_dic.get('username')
    user_pwd = back_dic.get('pwd')
    user_type = back_dic.get('user_type')
    user_obj = Models.UserInfo.sql_select(user_name=username)
    user_pwd = common.get_md5(user_pwd)
    # 判断用户是否存在
    if not user_obj:
        user_reg = Models.UserInfo(

            user_name=username,
            user_pwd=user_pwd,
            is_vip=0,
            is_locked=0,
            user_type=user_type,
            register_time=datetime.datetime.now()

        )
        user_reg.sql_save()
        send_dic = {
            'flag': True,
            'msg': '注册成功！'
        }
    else:
        send_dic = {
            'flag': False,
            'msg': '用户已经存在！'
        }

    common.send_msg(send_dic, conn)


def login_interface(back_dic, conn):
    """
    用户登录接口
    :param back_dic:
    :param conn:
    """
    username = back_dic.get('username')
    pwd = back_dic.get('pwd')

    user_pwd = common.get_md5(pwd)

    user_obj = Models.UserInfo.sql_select(user_name=username)

    # 在服务器中保存session信息
    addr = back_dic.get('addr')

    if user_obj:
        user_obj = user_obj[0]
        # 判断密码是否相同
        if user_obj.user_pwd == user_pwd:
            send_dic = {
                'flag': True,
                'msg': '登录成功',
                'is_vip': user_obj.is_vip,
                'new_notice': None
            }

            session = common.get_session(username)

            send_dic['session'] = session

            # 将登录信息保存到online_info中
            lock.acquire()

            user_data.online_info[addr] = [session, user_obj.user_id]  # 保存，session 和用户id用户登录验证

            lock.release()

            # 获取最新公告
            new_notice = common_interface.get_new_notice_interface()
            send_dic['new_notice'] = new_notice

        else:
            send_dic = {
                'flag': False,
                'msg': '用户名或密码错误'
            }
    else:
        send_dic = {
            'flag': False,
            'msg': '用户不存在，还不去注册去'
        }
    # {"('127.0.0.1', 63696)": ['104207c87d76dba69375219c4909eb85', 1]}
    # print(user_data.online_info)

    # print(user_data.mutex)

    common.send_msg(send_dic, conn)


@common.login_auth
def upload_movies_interface(back_dic, conn):
    # print(back_dic)
    # 电影信息
    movies_name = back_dic.get('movies_name')
    movies_size = back_dic.get('movies_size')
    is_free = back_dic.get('is_free')
    movies_md5 = back_dic.get('movies_md5')
    user_id = back_dic.get('user_id')

    movies_path = os.path.join(
        settings.DOWNLOAD_MOVIES_PATH,
        movies_name
    )

    recv_data = 0
    with open(movies_path, 'wb') as fw:
        while recv_data < movies_size:
            data = conn.recv(1024)
            fw.write(data)
            recv_data += len(data)

        fw.flush()

    movies_obj = Models.Movie(

        movie_name=movies_name,
        is_free=is_free,
        is_delete=0,
        file_md5=movies_md5,
        path=movies_path,
        movie_size=movies_size,
        upload_time=datetime.datetime.now(),
        user_id=user_id

    )

    # 保存电影信息
    movies_obj.sql_save()

    send_dic = {
        'flag': True,
        'msg': '电影上传成功！'
    }

    common.send_msg(send_dic, conn)


@common.login_auth
def delete_movies_interface(back_dic, conn):
    """
    根据电影id删除电影
    :param back_dic:
    :param conn:
    """
    movie_id = back_dic.get('movie_id')
    movie_obj_list = Models.Movie.sql_select(movie_id=movie_id)
    if movie_obj_list:

        # 删除电影记录
        movie_obj = movie_obj_list[0]
        movie_obj.is_delete = 1
        movie_obj.sql_update()

        send_dic = {
            'flag': True,
            'msg': '电影删除成功！'
        }


    else:
        send_dic = {
            'flag': False,
            'msg': '删除的电影不存在'
        }

    common.send_msg(send_dic, conn)


@common.login_auth
def send_notice_interface(back_dic, conn):
    """
    管理员发布公告
    :param back_dic:
    :param conn:
    """
    # 获取公告标题和内容
    title = back_dic.get("title")
    content = back_dic.get('content')

    notice_obj = Models.Notice(
        title=title,
        content=content,
        create_time=datetime.datetime.now(),
        user_id=back_dic.get('user_id')

    )

    # 保存发布的公告
    notice_obj.sql_save()

    send_dic = {
        'flag': True,
        'msg': '公告发布成功!',
    }

    common.send_msg(send_dic, conn)
