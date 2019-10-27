from db import Models
from lib import common

"""
@author RansySun
@create 2019-10-04-10:37
"""


@common.login_auth
def check_movie_interface(back_dic, conn):
    """
    查看电影是否已经存在
    :param back_dic:
    :param conn:
    """
    movies_md5 = back_dic.get('movies_md5')
    models_obj = Models.Movie.sql_select(file_md5=movies_md5)
    if models_obj:
        send_dic = {
            'flag': False,
            'msg': '电影已存在！'
        }
    else:
        send_dic = {
            'flag': True,
            'msg': '可以上传电影啦'
        }

    common.send_msg(send_dic, conn)


@common.login_auth
def check_all_movies_interface(back_dic, conn):
    """
    按照查看电影类别返回电影列表
    :param back_dic:
    :param conn:
    """
    movies_obj = Models.Movie.sql_select()
    movie_type = back_dic.get('movies_type')
    back_movies_list = []
    check_movies_list = []

    # 获取没有删除电影列表
    for movie in movies_obj:
        if not movie.is_delete:
            check_movies_list.append(movie)

    # 获取，收费免费，收费，免费的电影
    if check_movies_list:
        for movie in check_movies_list:
            if movie_type == 'all':

                back_movies_list.append(
                    [
                        movie.movie_id,
                        movie.movie_name,
                        '免费' if movie.is_free else '收费'
                    ]  # 电影id,电影名称， 是否免费
                )

            elif movie_type == 'free':
                if movie.is_free:
                    back_movies_list.append(
                        [
                            movie.movie_id,
                            movie.movie_name,
                            '免费'
                        ]
                    )

            elif movie_type == 'pay':
                if not movie.is_free:
                    back_movies_list.append(
                        [
                            movie.movie_id,
                            movie.movie_name,
                            '收费'
                        ]
                    )
        send_dic = {
            'flag': True,
            'back_movies_list': back_movies_list
        }

    else:
        send_dic = {
            'flag': False,
            'msg': '可以删除的电影列表为空'
        }

    common.send_msg(send_dic, conn)


def get_new_notice_interface():
    """
    获取最新公告给用户
    :return: 公告
    """
    notice_obj_list = Models.Notice.sql_select()

    notice_desc = sorted(
        notice_obj_list, key=lambda notice_obj: notice_obj.n_id, reverse=True
    )
    notice_dic = {
        'title': notice_desc[0].title,
        'content': notice_desc[0].content
    }
    return notice_dic
