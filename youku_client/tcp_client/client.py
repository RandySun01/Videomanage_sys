import socket

"""
@author RansySun
@create 2019-10-04-10:41
"""


def get_client():
    client = socket.socket()
    client.connect(('127.0.0.1', 8888))

    return client
