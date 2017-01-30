# -*- coding: utf-8 -*-
import sqlite3 as sqlite

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication

from TBTracker_AuxiliaryFunction import get_current_system_time
from TBTracker_Gui.TBTracker_Gui_Dialog import MessageDialog
from TBTracker_MainWindow import (TBTrackerMainWindow, 
                                  TBTrackerAddDataWindow, 
                                  TBTrackerSelectCommodityWindow,
                                  TBTrackerSelectMonthWindow,
                                  TBTrackerSelectYearWindow)

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2017.01.24
'''

MonthMap = {"一月份数据": "01", "二月份数据": "02", "三月份数据": "03", "四月份数据": "04",
            "五月份数据": "05", "六月份数据": "06", "七月份数据": "07", "八月份数据": "08",
            "九月份数据": "09", "十月份数据": "10", "十一月份数据": "11", "十二月份数据": "12"}

class OverLoadClassMethod(object):
    def __init__(self):
        super(OverLoadClassMethod, self).__init__()
    
    def tb_tracker_add_data_window(self):
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

    def tb_tracker_select_commodity_window(self):
        myTBTrackerSelectCommodityWindow.show()

    def tb_tracker_select_commodity_window_confirm(self):
        commodityCNT = myTBTrackerSelectCommodityWindow.commodityTable.rowCount()
        selectedFlag = False
        for i in range(commodityCNT):
            radio = myTBTrackerSelectCommodityWindow.commodityTable.cellWidget(i, 0)
            checkedFlag = radio.isChecked()
            if checkedFlag:
                print(myTBTrackerSelectCommodityWindow.commodityTable.item(i, 1).text().strip())
                selectedFlag = True
                break
        if selectedFlag:
            myTBTrackerSelectCommodityWindow.close()
        else:
            messageDialog = MessageDialog()
            messageDialog.warning(myTBTrackerAddDataWindow, "消息提示对话框", "未选择任何商品!")

    def tb_tracker_select_month_window(self):
        myTBTrackerSelectMonthWindow.show()

    def tb_tracker_select_month_window_confirm(self):
        selectedMonth = myTBTrackerSelectMonthWindow.monthComboBox.itemText(myTBTrackerSelectMonthWindow.monthComboBox.currentIndex())
        print(MonthMap[selectedMonth])
        myTBTrackerSelectMonthWindow.close()

    def tb_tracker_select_year_window(self):
        myTBTrackerSelectYearWindow.show()

    def tb_tracker_select_year_window_confirm(self):
        selectedYear = myTBTrackerSelectYearWindow.yearComboBox.itemText(myTBTrackerSelectYearWindow.yearComboBox.currentIndex())
        print(selectedYear)
        myTBTrackerSelectYearWindow.close()

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
    myTBTrackerSelectCommodityWindow = TBTrackerSelectCommodityWindow()
    myTBTrackerSelectMonthWindow = TBTrackerSelectMonthWindow()
    myTBTrackerSelectYearWindow = TBTrackerSelectYearWindow()

    overLoad = OverLoadClassMethod()

    myTBTrackerMainWindow.add_data = overLoad.tb_tracker_add_data_window
    myTBTrackerMainWindow.addButton.clicked.connect(myTBTrackerMainWindow.add_data)
    myTBTrackerAddDataWindow.confirm = overLoad.tb_tracker_add_data_window_confirm
    myTBTrackerAddDataWindow.confirmButton.clicked.connect(myTBTrackerAddDataWindow.confirm)
    myTBTrackerMainWindow.select_commodity = overLoad.tb_tracker_select_commodity_window
    myTBTrackerMainWindow.selectCommodityButton.clicked.connect(myTBTrackerMainWindow.select_commodity)
    myTBTrackerSelectCommodityWindow.confirm = overLoad.tb_tracker_select_commodity_window_confirm
    myTBTrackerSelectCommodityWindow.confirmButton.clicked.connect(myTBTrackerSelectCommodityWindow.confirm)
    myTBTrackerMainWindow.select_month = overLoad.tb_tracker_select_month_window
    myTBTrackerMainWindow.monthlyDataButton.clicked.connect(myTBTrackerMainWindow.select_month)
    myTBTrackerMainWindow.select_year = overLoad.tb_tracker_select_year_window
    myTBTrackerMainWindow.yearlyDataButton.clicked.connect(myTBTrackerMainWindow.select_year)
    myTBTrackerSelectMonthWindow.confirm = overLoad.tb_tracker_select_month_window_confirm
    myTBTrackerSelectMonthWindow.confirmButton.clicked.connect(myTBTrackerSelectMonthWindow.confirm)
    myTBTrackerSelectYearWindow.confirm = overLoad.tb_tracker_select_year_window_confirm
    myTBTrackerSelectYearWindow.confirmButton.clicked.connect(myTBTrackerSelectYearWindow.confirm)

    myTBTrackerMainWindow.show()

    sys.exit(app.exec_())
