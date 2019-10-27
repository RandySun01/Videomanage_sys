import os

"""
@author RansySun
@create 2019-10-04-10:35
"""

############################
#
#
# 上传电影路径和下载路径
############################

BASE_PATH = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DOWNLOAD_MOVIES_PATH = os.path.join(
    BASE_PATH,
    'db',
    'download_movies'
)
