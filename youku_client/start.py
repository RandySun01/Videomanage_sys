import sys
import os
from core import src
import cv2 as cv

"""
@author RansySun
@create 2019-10-04-10:41
"""
sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)


def play_video():
    # 读取视频
    cap = cv.VideoCapture(r'G:\方优酷\fangyouiku02\youku_client\db\upload_movies\1服务端注册功能封装.mp4')
    while cap.isOpened():
        ret, frame = cap.read()
        print(cap.read())
        if not ret:
            print("无法接收帧，流结束，正在退出")
            break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        cv.imshow('frame', gray)
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


play_video()

if __name__ == '__main__':
    # 客户端启动入口
    src.run()
