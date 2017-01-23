# -*- coding: utf-8 -*-
import sqlite3 as sqlite

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication

from TBTracker_AuxiliaryFunction import get_current_system_time
from TBTracker_Gui.TBTracker_Gui_Dialog import MessageDialog
from TBTracker_MainWindow import TBTrackerMainWindow, TBTrackerAddDataWindow

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2017.01.20
'''

class OverLoadClassMethod(object):
    def __init__(self):
        super(OverLoadClassMethod, self).__init__()
    
    def tb_tracker_main_window_add_data(self):
        myTBTrackerAddDataWindow.show()

    def tb_tracker_add_data_window_confirm(self):
        productID = myTBTrackerAddDataWindow.productIDLineEdit.text()
        myTBTrackerAddDataWindow.productIDLineEdit.setText("")
        URL = myTBTrackerAddDataWindow.URLLineEdit.text()
        myTBTrackerAddDataWindow.URLLineEdit.setText("")
        title = myTBTrackerAddDataWindow.titleLineEdit.text()
        myTBTrackerAddDataWindow.titleLineEdit.setText("")
        shopName = myTBTrackerAddDataWindow.shopNameLineEdit.text()
        myTBTrackerAddDataWindow.shopNameLineEdit.setText("")
        price = myTBTrackerAddDataWindow.priceLineEdit.text()
        myTBTrackerAddDataWindow.priceLineEdit.setText("")
        taobaoPrice = myTBTrackerAddDataWindow.taobaoPriceLineEdit.text()
        myTBTrackerAddDataWindow.taobaoPriceLineEdit.setText("")

        if (productID != "" and URL != "" and
            title != "" and shopName !="" and
            price != "" and taobaoPrice != ""):
            conn = sqlite.connect('TBTracker_DB/TBTracker.db')
            c = conn.cursor()
            c.execute('insert into product values ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                productID, URL, title, shopName, price, taobaoPrice, get_current_system_time()))
            conn.commit()
            c.close()
            myTBTrackerAddDataWindow.close()
            myTBTrackerMainWindow.show_database()
        else:
            messageDialog = MessageDialog()
            messageDialog.warning(myTBTrackerAddDataWindow, "消息提示对话框", "存在未填项!")

    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    # 读取样式表
    file = open("TBTracker_Gui/TBTracker_Gui_Style.qss", 'r')
    styleSheet = file.read()
    file.close()
    # 设置全局样式
    qApp.setStyleSheet(styleSheet)

    # 汉化处理
    tran = QTranslator()
    tran.load("qt_zh_CN.qm", "TBTracker_Font/")
    qApp.installTranslator(tran)

    myTBTrackerMainWindow = TBTrackerMainWindow()
    myTBTrackerAddDataWindow = TBTrackerAddDataWindow()

    overLoad = OverLoadClassMethod()

    myTBTrackerMainWindow.add_data = overLoad.tb_tracker_main_window_add_data
    myTBTrackerMainWindow.addButton.clicked.connect(myTBTrackerMainWindow.add_data)
    myTBTrackerAddDataWindow.confirm = overLoad.tb_tracker_add_data_window_confirm
    myTBTrackerAddDataWindow.confirmButton.clicked.connect(myTBTrackerAddDataWindow.confirm)

    myTBTrackerMainWindow.show()

    qApp.installEventFilter(myTBTrackerMainWindow)
    sys.exit(app.exec_())
