import os
import sys
from tcp_server import server

"""
@author RansySun
@create 2019-10-04-10:35
"""

sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)

if __name__ == '__main__':
    print("服务端正在启动....")
    server.run()
