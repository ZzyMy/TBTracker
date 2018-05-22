# -*- coding: utf-8 -*-
import schedule
import time

from TBTracker_RoutineSpider import run

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.1
@date    : 2018.04.22
'''

def job():
    print('Work Hard!!!')
    run()

if __name__ == '__main__':
    schedule.every().day.at('19:47').do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
    