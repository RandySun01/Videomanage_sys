import socket
import json
import struct
from lib import common
from interface import admin_interface, common_interface, user_interface
from concurrent.futures import ThreadPoolExecutor
from db import user_data

"""
@author RansySun
@create 2019-10-04-10:39
"""
pool = ThreadPoolExecutor(100)

func_dic = {
    # 注册
    'register': admin_interface.register_interface,

    # 登录
    'login': admin_interface.login_interface,

    # 查看上传电影是否存在
    'check_movie': common_interface.check_movie_interface,

    # 添加电影
    'upload_movies': admin_interface.upload_movies_interface,

    # 管理员查看没有被删除电影
    'check_all_movies': common_interface.check_all_movies_interface,

    # 管理员删除电影
    'delete_movies': admin_interface.delete_movies_interface,

    # 管理员发布公告
    'send_notice': admin_interface.send_notice_interface,

    # 普通用户
    'buy_vip': user_interface.buy_vip_interface,
    # 普通用户下载免费电影
    'download_movie': user_interface.download_movie_interface,
    'check_recore': user_interface.check_recore_interface,
    'check_notice': user_interface.check_notice_interface

}


def run():
    """
    服务端启动入口
    """
    server = socket.socket()
    server.bind(('127.0.0.1', 8888))
    server.listen(5)

    while True:
        conn, addr = server.accept()

        # 启动一个线程工作
        pool.submit(working, conn, addr)


def dispatcher(back_dic, conn):
    """
    转发任务
    :param back_dic:
    :param conn:
    :param addr:
    """
    func_type = back_dic.get('func_type')

    # 判断功能接口是否存在
    if func_type not in func_dic:
        send_dic = {
            'flag': False,
            'msg': '请求错误！'
        }

        common.send_msg(send_dic, conn)

    func_dic.get(func_type)(back_dic, conn)


def working(conn, addr):
    """
    接收请求数据
    :param conn:
    :param addr:
    """
    while True:
        try:
            # 接收客户端数据
            header = conn.recv(4)
            data_len = struct.unpack('i', header)[0]
            json_data = conn.recv(data_len)
            back_dic = json.loads(json_data)

            # 将地址添加到字典中作为身份验证
            back_dic['addr'] = str(addr)  # addr===>是元组
            print(back_dic)
            dispatcher(back_dic, conn)
        except Exception as e:
            user_data.mutex.acquice()
            user_data.online_info.pop(addr)
            user_data.mutex.release()
            print(f'\033[34m e: {e}\033[0m')
