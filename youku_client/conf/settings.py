import os

"""
@author RansySun
@create 2019-10-04-10:39
"""

############################
#
# 获取视频上传/下载路径
############################
BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

UPLOAD_MOVIES_PAHT = os.path.join(
    BASE_PATH,
    'db',
    'upload_movies'
)

DOWN_MOVIES_PATH = os.path.join(
    BASE_PATH,
    'db',
    'down_movies'
)
if __name__ == '__main__':
    print(BASE_PATH)
