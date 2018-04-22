# -*- coding: utf-8 -*-
import sqlite3 as sqlite
import sys

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.1
@date    : 2018.04.22
'''

def main():
    print("*********************** Welcome to TBTracker System **************************")
    print("*                                                                            *")
    print("******************************************************************************")
    
    conn = sqlite.connect('TBTracker_DB/TBTracker.db')
    c = conn.cursor()
    try:
        c.execute('create table product (\
            ProductName text      not null, \
            URL         text      not null, \
            Title       text      not null, \
            ShopName    text      not null, \
            Price       text      not null, \
            TaoBaoPrice text      not null, \
            CreateTime  timestamp not null)')
    except sqlite.OperationalError as e:
        print(e)
    finally:
        c.close()

    conn = sqlite.connect('TBTracker_DB/TBTrackerTag.db')
    c = conn.cursor()
    try:
        c.execute('create table tag (\
            TagName    text      not null, \
            CreateTime timestamp not null)')
    except sqlite.OperationalError as e:
        print(e)
    finally:
        c.close()

    conn = sqlite.connect('TBTracker_DB/TBTrackerRoutineSpider.db')
    c = conn.cursor()
    try:
        c.execute('create table commodity (\
            Description text      not null, \
            Price       text      not null,\
            CreateTime  timestamp not null)')
    except sqlite.OperationalError as e:
        print(e)
    finally:
        c.close()

    print("******************************************************************************")
    print("*                                                                            *")
    print("********************* TBTracker_DB_Init is Successful! ***********************")

if __name__ == '__main__':
    main()
    