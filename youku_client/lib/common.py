import json
import struct
import os
import hashlib
from conf import settings

"""
@author RansySun
@create 2019-10-04-10:41
"""


def send_msg(send_dic, client, file=None):
    """
    向服务端发送消息和接收消息
    :param send_dic:
    :param client:
    :param file:
    :return:
    """
    # 向服务端发送数据
    json_data = json.dumps(send_dic).encode('utf8')
    headers = struct.pack('i', len(json_data))
    client.send(headers)
    client.send(json_data)

    if file:
        # 上传电影
        with open(file, 'rb') as fr:
            for line in fr:
                client.send(line)

    # 接收服务端发来的数据
    header = client.recv(4)
    length = struct.unpack('i', header)[0]
    json_data = client.recv(length)

    back_dic = json.loads(json_data)
    return back_dic


def get_movies_list():
    """
    获取上传电影列表
    :return:
    """
    movies_path = settings.UPLOAD_MOVIES_PAHT
    if os.path.exists(movies_path):
        return os.listdir(movies_path)


def get_movies_md5(movies_path, movies_size):
    """
    获取电影md5值
    :param movies_path:
    """

    movies_list = [0, movies_size // 3, movies_size // 3 * 2, movies_size - 10]
    m = hashlib.md5()

    # 读取十个字节划分
    with open(movies_path, 'rb') as fr:
        for line in movies_list:
            fr.seek(line)
            data = fr.read(10)
            m.update(data)

    return m.hexdigest()
