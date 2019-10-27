from db import Models
from lib import common
import datetime

"""
@author RansySun
@create 2019-10-04-10:37
"""


@common.login_auth
def buy_vip_interface(back_dic, conn):
    user_id = back_dic.get('user_id')
    is_vip = back_dic.get('is_vip')
    # 获取当前用户信息
    user_obj = Models.UserInfo.sql_select(user_id=user_id)[0]

    # 修改vip
    user_obj.is_vip = is_vip
    user_obj.sql_update()
    send_dic = {
        'flag': True,
        'msg': '恭喜你成为我们的会员，你可以享受服务了啊！'
    }
    common.send_msg(send_dic, conn)


@common.login_auth
def download_movie_interface(back_dic, conn):
    """
    下载收费和免费电影
    :param back_dic:
    :param conn:
    """
    # 查询要下载电影
    movie_id = back_dic.get('movie_id')
    movie_obj_list = Models.Movie.sql_select(movie_id=movie_id)
    if movie_obj_list:
        movie_obj = movie_obj_list[0]
        movie_path = movie_obj.path
        movie_size = int(movie_obj.movie_size)
        user_id = back_dic.get('user_id')
        user_obj = Models.UserInfo.sql_select(user_id=user_id)[0]
        wait_time = 0
        if not user_obj.is_vip:
            wait_time = 15
        send_dic = {
            'flag': True,
            'msg': '正在下载！',
            'movie_size': movie_size,
            'wait_time': wait_time
        }
        common.send_msg(send_dic, conn, movie_path)

        download_record_obj = Models.DownloadRecord(
            user_id=user_id,
            movie_id=movie_id,
            download_time=datetime.datetime.now()

        )
        download_record_obj.sql_save()

    else:
        send_dic = {
            'flag': False,
            'msg': '下载的电影不存在！'
        }

        common.send_msg(send_dic, conn)


@common.login_auth
def check_recore_interface(back_dic, conn):
    user_id = back_dic.get('user_id')
    down_record = Models.DownloadRecord.sql_select()
    movie_record_list = []

    if down_record:
        for record in down_record:

            # 判断下载用户id是否与当前用户id相同
            if record.user_id == user_id:
                # 获取当前记录下载的电影id,获取电影名称
                movie_obj = Models.Movie.sql_select(movie_id=record.movie_id)[0]
                movie_record_list.append(
                    movie_obj.movie_name
                )

        if movie_record_list:

            send_dic = {
                'flag': True,
                'record_list': movie_record_list

            }
        else:
            send_dic = {
                'flag': False,
                'msg': '当前用户没有下载记录'
            }
    else:
        send_dic = {
            'flag': False,
            'msg': '没有下载记录！'
        }

    common.send_msg(send_dic, conn)


@common.login_auth
def check_notice_interface(back_dic, conn):
    notice_obj_list = Models.Notice.sql_select()

    notice_list = []

    if notice_obj_list:
        for notice_obj in notice_obj_list:
            notice_list.append(
                {
                    'title': notice_obj.title,
                    'content:': notice_obj.content,
                }
            )
        send_dic = {
            'flag': True,
            'notice_list': notice_list
        }
    else:
        send_dic = {
            'flag': False,
            'msg': "没有公告！"
        }

    common.send_msg(send_dic, conn)
