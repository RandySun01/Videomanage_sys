from lib import common
from conf import settings
import os

"""
@author RansySun
@create 2019-10-04-10:40
"""
user_info = {
    'cookies': None
}


def register(client):
    """
    管理员注册功能
    :param client:
    """
    username = input('请输入用户名：')
    pwd = input("请输入密码：")
    re_pwd = input("请输入确认密码")

    if pwd == re_pwd:
        send_dic = {
            'func_type': 'register',
            'username': username,
            'pwd': pwd,
            'user_type': 'admin'

        }
        back_dic = common.send_msg(send_dic, client)

        if back_dic.get('flag'):
            print(back_dic.get('msg'))
        else:
            print(back_dic.get('msg'))
    else:
        print("两次密码输入不一样！")


def login(client):
    """
    管理员登录功能
    :param client:
    """
    username = input('请输入用户名：')
    pwd = input("请输入密码：")

    send_dic = {
        'func_type': 'login',
        'username': username,
        'pwd': pwd,
        'user_type': 'admin'

    }
    back_dic = common.send_msg(send_dic, client)

    # {'flag': True, 'msg': '登录成功', 'is_vip': 0, 'new_notice': {'title': 'via提', 'content': '怎么搞得我是最帅的'}, 'session': '104207c87d76dba69375219c4909eb85'}
    # print(back_dic)
    if back_dic.get('flag'):

        # 登录装饰器判断
        user_info['cookies'] = back_dic.get('session')

        print(user_info)
        print(back_dic.get('msg'))
    else:
        print(back_dic.get('msg'))


def upload_movies(client):
    """
    电影上传
    :param client:
    """
    while True:
        # 1.获取当前文件夹中的视频列表
        upload_movies_list = common.get_movies_list()

        if upload_movies_list:
            # 选择电影名称
            for index, movies_name in enumerate(upload_movies_list):
                print(index, movies_name)

            choice = input("请选择电影编号：")
            if choice == 'q':
                break

            if not choice.isdigit():
                print('输入必须是数字')
                continue

            choice = int(choice)

            if choice not in range(len(upload_movies_list)):
                print('电影不存在！')
                continue

            movies_name = upload_movies_list[choice]
            # 2 拼接电影路径
            movies_path = os.path.join(
                settings.UPLOAD_MOVIES_PAHT,
                movies_name
            )

            movies_size = os.path.getsize(movies_path)
            # 3 获取电影md5值判断电影是否存在
            movies_md5 = common.get_movies_md5(movies_path, movies_size)

            send_dic = {
                'func_type': 'check_movie',
                'session': user_info.get('cookies'),
                'movies_md5': movies_md5
            }

            back_dic = common.send_msg(send_dic, client)

            if back_dic.get('flag'):
                print(back_dic.get('msg'))

                # 判断电影是否免费
                free_choice = input("电影是否免费（Y/N）：").strip().lower()
                if free_choice == 'y':
                    is_free = 1
                else:
                    is_free = 0
                print("正在上传")
                send_dic = {
                    'func_type': 'upload_movies',
                    'session': user_info.get('cookies'),
                    'movies_name': movies_name,
                    'is_free': is_free,
                    'movies_md5': movies_md5,
                    'movies_size': movies_size
                }

                back_dic = common.send_msg(send_dic, client, movies_path)
                if back_dic.get('flag'):
                    print(back_dic.get('msg'))
                    break
                else:
                    print(back_dic.get('msg'))
                    break
            else:
                print(back_dic.get('msg'))
                break

        else:
            print("上传电影类表为空！")


def delete_movies(client):
    """
    删除电影
    :param client:
    """
    while True:
        # 1.获取删除的电影列表
        send_dic = {
            'func_type': 'check_all_movies',
            'session': user_info.get('cookies'),
            'movies_type': 'all'

        }

        back_dic = common.send_msg(send_dic, client)
        if back_dic.get('flag'):

            # 获取电影名称
            movies_list = back_dic.get('back_movies_list')
            for index, movie in enumerate(movies_list):
                print(index, movie)

            choice = input("请选择电影编号：")
            if choice == 'q':
                break

            if not choice.isdigit():
                print('输入必须是数字')
                continue

            choice = int(choice)

            if choice not in range(len(movies_list)):
                print('电影不存在！')
                continue

            # 获取要删除的电影名称
            movie_id, movie_name, movie_type = movies_list[choice]
            print("电影正在删除")
            send_dic = {
                'func_type': 'delete_movies',
                'session': user_info.get("cookies"),
                'movie_id': movie_id
            }
            # 发送要删除的电影
            back_dic = common.send_msg(send_dic, client)
            if back_dic.get('flag'):
                print(back_dic.get('msg'))
            else:
                print(back_dic.get('msg'))

        else:
            print(back_dic.get('msg'))
            break


def send_notice(client):
    title = input("请输入标题：")
    content = input("请输入内容：")

    sned_dic = {
        'func_type': 'send_notice',
        'session': user_info.get('cookies'),
        'title': title,
        'content': content
    }
    back_dic = common.send_msg(sned_dic, client)

    if back_dic.get('flag'):
        print(back_dic.get('msg'))

    else:
        print(back_dic.get('msg'))


func_dic = {

    '1': register,
    '2': login,
    '3': upload_movies,
    '4': delete_movies,
    '5': send_notice,

}


def admin_view(client):
    """
    管理员入口
    :param client:
    """
    while True:
        print(
            '''
                1 注册
                2 登录
                3 上传视频
                4 删除视频
                5 发布公告
                q 退出
                '''
        )

        choice = input("请选择功能")

        if choice == 'q':
            break

        if not choice.isdigit():
            print("输入必须是数字")
            continue

        if choice not in func_dic:
            print("输入错误")
            continue

        # 选择功能
        func_dic.get(choice)(client)
