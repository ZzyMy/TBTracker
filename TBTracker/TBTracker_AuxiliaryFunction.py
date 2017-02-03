# -*- coding: utf-8 -*-
# ********************系统自带相关模块导入********************
import datetime
import platform
import time

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2017.01.24
'''

# 检查当前操作系统版本信息并依此设置主路径
def check_os():
    if platform.system() == "Windows":
        return "D:/"
    elif platform.system() == "Linux":
        import getpass
        user = getpass.getuser()
        return "/home/" + user + "/"

# 返回当前操作系统版本信息
def return_os():
    if platform.system() == "Windows":
        return "Windows"
    elif platform.system() == "Linux":
        return "Linux"

# 获取当前屏幕尺寸
def get_current_screen_size():
    width = int(1366 * 0.9)
    height = int(768 * 0.9)
    return (width, height)

# 获取当前系统时间
def get_current_system_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

# 获取当前系统日期
def get_current_system_date():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))

# 生成指定范围内的日期序列
def generate_date_list(start, end):
    start_date = datetime.date(*start)
    end_date = datetime.date(*end)

    date_list = []
    current_date = start_date
    while current_date != end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(1)
    date_list.append(current_date)
    return date_list

if __name__ == '__main__':
    print(generate_date_list((2014, 7, 28), (2014, 8, 3)))
    