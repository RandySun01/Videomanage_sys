import json
import struct
import hmac
import uuid
from functools import wraps
from db import user_data

"""
@author RansySun
@create 2019-10-04-10:37
"""


def send_msg(send_dic, conn, file=None):
    """
    向客户端发送消息
    :param send_dic:
    :param conn:
    :param file:
    """
    json_data = json.dumps(send_dic).encode('utf8')
    headers = struct.pack('i', len(json_data))
    conn.send(headers)
    conn.send(json_data)

    if file:
        # 发送文件(movies)
        with open(file, 'rb') as fr:
            for line in fr:
                conn.send(line)


def get_md5(pwd):
    """
    获取md5加密
    :param pwd:
    """
    m = hmac.new('randy'.encode('utf8'))
    m.update(pwd.encode('utf8'))
    return m.hexdigest()


def get_session(name):
    """
    获取当前用户session
    :param name:
    :return:
    """
    m = hmac.new('randy'.encode('utf8'))
    m.update(name.encode('utf8'))
    uuid_obj = uuid.uuid4()

    m.update(str(uuid_obj).encode('utf8'))
    return m.hexdigest()


def login_auth(func):
    """
    登录装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def innter(*args, **kwargs):
        # args ===> back_dic, coon
        # 判断用户是否登录

        # 1.获取客户端session
        back_dic = args[0]
        conn = args[1]

        client_session = back_dic.get('session')

        addr = back_dic.get('addr')

        # 获取服务器中session
        user_data.mutex.acquire()
        # server_list = user_data.online_info[addr]  # [session, user_id]

        # 尽量使用get取值
        server_list = user_data.online_info.get(addr)  # [session, user_id]

        user_data.mutex.release()

        if server_list:

            # 判断服务端和客户端session是否相等
            if server_list[0] == client_session:

                # 添加用户id
                back_dic['user_id'] = server_list[1]
                res = func(*args, **kwargs)
                return res
            else:

                send_dic = {
                    'flag':False,
                    'msg': '没有登录，请去登录！'
                }

        else:
            send_dic = {
                'flag': False,
                'msg': '没有登录，，请去登录！'
            }

        send_msg(send_dic, conn)

    return innter
