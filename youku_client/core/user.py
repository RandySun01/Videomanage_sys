from conf import settings
import os
import time
from lib import common

"""
@author RansySun
@create 2019-10-04-10:40
"""
user_info = {
    'cookies': None,
    'is_vip': None
}


def register(client):
    """
    用户注册功能
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
            'user_type': 'user'

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
    用户登录功能
    :param client:
    """
    username = input('请输入用户名：')
    pwd = input("请输入密码：")

    send_dic = {
        'func_type': 'login',
        'username': username,
        'pwd': pwd,
        'user_type': 'user'

    }
    back_dic = common.send_msg(send_dic, client)

    # {'flag': True, 'msg': '登录成功', 'is_vip': 0, 'new_notice': {'title': 'via提', 'content': '怎么搞得我是最帅的'}, 'session': '104207c87d76dba69375219c4909eb85'}
    # print(back_dic)
    if back_dic.get('flag'):
        # 登录装饰器判断
        user_info['cookies'] = back_dic.get('session')
        user_info['is_vip'] = back_dic.get('is_vip')
        # print(back_dic)

        if back_dic.get('new_notice'):
            new_notice = back_dic.get('new_notice')
            # print(new_notice)
            print(f'\033[31m title: {new_notice.get("title")}\033[0m')
            print(f'\033[34m content: {new_notice.get("content")}\033[0m')

        print(user_info)
        print(back_dic.get('msg'))
    else:
        print(back_dic.get('msg'))


def buy_vip(client):
    """
    普通用户充值会员
    :param client:
    :return:
    """
    # 判断用户是否vip
    if user_info.get("is_vip"):
        print("你已经是我们的会员啦，可以享受额外的服务")
        return

    if not user_info.get('is_vip'):
        buy_choice = input("是否充值会员（Y/N）？").strip().lower()

        # 是否充值
        if buy_choice == 'y':
            is_vip = 1
            print(f'\033[31m 正在充值！ \033[0m')

            send_dic = {
                'func_type': 'buy_vip',
                'session': user_info.get('cookies'),
                'is_vip': is_vip
            }
            back_dic = common.send_msg(send_dic, client)

            # 判断是否充值成功
            if back_dic.get('flag'):
                user_info['is_vip'] = 1
                print(back_dic.get('msg'))
            else:
                print(back_dic.get('msg'))

        else:
            print("充值失败，你享受不到我们的服务啦")


def check_all_movie(client):
    send_dic = {
        'func_type': 'check_all_movies',
        'session': user_info.get('cookies'),
        'movies_type': 'all'
    }

    back_dic = common.send_msg(send_dic, client)

    if back_dic.get('flag'):
        print("电影列表：")
        movie_list = back_dic.get('back_movies_list')
        for index, movie in enumerate(movie_list):
            print(index, movie)

    else:
        print(back_dic.get('msg'))


def download_free_movie(client):
    """
    下载免费电影
    :param client:
    """
    send_dic = {
        'func_type': 'check_all_movies',
        'session': user_info.get('cookies'),
        'movies_type': 'free'
    }

    back_dic = common.send_msg(send_dic, client)

    if back_dic.get('flag'):
        print("免费电影列表：")
        movie_list = back_dic.get('back_movies_list')

        # 选择要下载的电影
        for index, movie in enumerate(movie_list):
            print(index, movie)
            choice = input("请选择电影编号：")
            if choice == 'q':
                break

            if not choice.isdigit():
                print('输入必须是数字')
                continue

            choice = int(choice)

            if choice not in range(len(movie_list)):
                print('电影不存在！')
                continue

            # 获取要下载电影的信息
            movie_id, movie_name, movie_type = movie_list[choice]

            # 拼接电影路径
            movie_path = os.path.join(
                settings.DOWN_MOVIES_PATH, movie_name
            )

            # 请求发送电影信息
            send_dic = {
                'func_type': 'download_movie',
                'session': user_info.get('cookies'),
                'movie_id': movie_id,
            }

            back_dic = common.send_msg(send_dic, client)

            # 接收电影
            if back_dic.get('flag'):
                movie_size = back_dic.get('movie_size')
                wait_time = back_dic.get('wait_time')
                if wait_time:
                    print("老王的duchagn上线了， 老王一直发牌")
                    time.sleep(wait_time)
                recv_data = 0
                print("正在下载电影")
                with open(movie_path, 'wb') as fw:
                    while recv_data < movie_size:
                        data = client.recv(1024)
                        fw.write(data)
                        recv_data += len(data)
                    fw.flush()

                print(f"{movie_name}--下载成功！")
            else:
                print(back_dic.get('msg'))
    else:
        print(back_dic.get('msg'))


def download_pay_movie(client):
    """
    下载收费电影
    :param client:
    """
    send_dic = {
        'func_type': 'check_all_movies',
        'session': user_info.get('cookies'),
        'movies_type': 'pay'
    }
    if user_info.get('is_vip'):
        pay_choice = input("会员购买打五折，花费5￥（Y/N）").strip().lower()
    else:
        pay_choice = input('你不是会员（会员打五折），共花费50￥（Y/N）').strip().lower()

    if pay_choice == 'y':

        back_dic = common.send_msg(send_dic, client)
    else:
        print("购买失败")

    if back_dic.get('flag'):
        print("收费电影列表：")
        movie_list = back_dic.get('back_movies_list')

        # 选择要下载的电影
        for index, movie in enumerate(movie_list):
            print(index, movie)
            choice = input("请选择电影编号：")
            if choice == 'q':
                break

            if not choice.isdigit():
                print('输入必须是数字')
                continue

            choice = int(choice)

            if choice not in range(len(movie_list)):
                print('电影不存在！')
                continue

            # 获取要下载电影的信息
            movie_id, movie_name, movie_type = movie_list[choice]

            # 拼接电影路径
            movie_path = os.path.join(
                settings.DOWN_MOVIES_PATH, movie_name
            )

            # 请求发送电影信息
            send_dic = {
                'func_type': 'download_movie',
                'session': user_info.get('cookies'),
                'movie_id': movie_id,
            }

            back_dic = common.send_msg(send_dic, client)

            # 接收电影
            if back_dic.get('flag'):
                movie_size = back_dic.get('movie_size')
                wait_time = back_dic.get('wait_time')
                if wait_time:
                    print("老王的duchagn上线了， 老王一直发牌")
                    time.sleep(wait_time)
                recv_data = 0
                print("正在下载电影")
                with open(movie_path, 'wb') as fw:
                    while recv_data < movie_size:
                        data = client.recv(1024)
                        fw.write(data)
                        recv_data += len(data)
                    fw.flush()

                print(f"{movie_name}--下载成功！")
            else:
                print(back_dic.get('msg'))
    else:
        print(back_dic.get('msg'))


def check_download_record(client):
    """
    查看当前用户现在记录
    :param client:
    """
    send_dic = {
        'func_type': 'check_recore',
        'session': user_info.get('cookies')

    }
    back_dic = common.send_msg(send_dic, client)
    if back_dic.get("flag"):
        print("当前用户下载记录：")
        record_list = back_dic.get('record_list')
        for index, movie in enumerate(record_list):
            print(index, movie)
    else:
        print(back_dic.get('msg'))


def check_all_notice(client):
    """
    查看所有发布的公告
    :param client:
    """
    send_dic = {
        'func_type': 'check_notice',
        'session': user_info.get('cookies'),

    }

    back_dic = common.send_msg(send_dic, client)

    if back_dic.get('flag'):
        notice_list = back_dic.get('notice_list')
        print("公告列表：")
        for notice_dic in notice_list:
            print(notice_dic)
    else:
        print(back_dic.get('msg'))


fun_dic = {

    '1': register,
    '2': login,
    '3': buy_vip,
    '4': check_all_movie,
    '5': download_free_movie,
    '6': download_pay_movie,
    '7': check_download_record,
    '8': check_all_notice,

}


def user_view(client):
    while True:
        print('''
               1 注册
               2 登录
               3 冲会员
               4 查看视频
               5 下载免费视频
               6 下载收费视频
               7 查看观影记录
               8 查看公告
               ''')

        choice = input("请选择功能")

        if choice == 'q':
            break

        if not choice.isdigit():
            print("输入必须是数字")
            continue

        if choice not in fun_dic:
            print("功能不不能再")
            continue

        fun_dic.get(choice)(client)
