from core import admin, user
from tcp_client import client

"""
@author RansySun
@create 2019-10-04-10:40
"""
func_dic = {
    '1': admin.admin_view,
    '2': user.user_view
}


def run():
    """
    选择角色
    """
    clients = client.get_client()
    while True:
        print(
            """
                请选择角色编号: 
                      1 管理员
                      2 普通用户
                      q 退出
            """
        )

        choice = input("请选择角色")

        if choice == 'q':
            break

        if not choice.isdigit():
            print("输入必须是数字")
            continue

        if choice not in func_dic:
            print("输入错误")
            continue

        # 选择功能
        func_dic.get(choice)(clients)
