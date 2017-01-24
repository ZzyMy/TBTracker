# -*- coding: utf-8 -*-
# ********************第三方相关模块导入********************
import logging

Logger = logging.getLogger("TBTracker")
Logger.setLevel(logging.DEBUG)
InfoHandler = logging.FileHandler("TBTracker_Log/info.log")
InfoHandler.setLevel(logging.INFO)
INFOFORMATTER = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]: %(message)s')
InfoHandler.setFormatter(INFOFORMATTER)
Logger.addHandler(InfoHandler)
ErrHandler = logging.FileHandler("TBTracker_Log/error.log")
ErrHandler.setLevel(logging.ERROR)
ERRORFORMATTER = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] File "%(filename)s", line %(lineno)d: %(message)s')
ErrHandler.setFormatter(ERRORFORMATTER)
Logger.addHandler(ErrHandler)

import math
import matplotlib.pyplot as plt
import os
import random
import requests
import sqlite3 as sqlite
import sys
import xlwt

from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wordcloud import WordCloud
# ********************PyQt5相关模块导入********************
from PyQt5.QtCore import QEvent
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
# ********************用户自定义相关模块导入********************
from TBTracker_AuxiliaryFunction import check_os, get_current_screen_size, get_current_system_time
from TBTracker_Gui.TBTracker_Gui_Button import *
from TBTracker_Gui.TBTracker_Gui_Dialog import *

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2017.01.20
'''

class TBTrackerMainWindow(QWidget):
    def __init__(self):
        super(TBTrackerMainWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("淘宝商品数据跟踪系统")
        self.setWindowIcon(QIcon('TBTracker_Ui/python.png'))
        self.width, self.height = get_current_screen_size()
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.set_widgets()
        self.setLayout(self.layout)

        self.show_database()
        self.plot_word_cloud()
        self.plot_product_tree()

    def set_widgets(self):
        q_1_Font = QFont()
        q_1_Font.setPointSize(16)

        labelFont = QFont()
        labelFont.setPointSize(12)

        q_2_Font = QFont()
        q_2_Font.setPointSize(12)

        self.table_1_Font = QFont()
        self.table_1_Font.setPointSize(10)
        self.table_1_Font.setStyleName("Bold") 
        self.table_2_Font = QFont()
        self.table_2_Font.setPointSize(12)
        self.table_2_Font.setStyleName("Bold")

        self.headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}

        # ****************************************
        firstWidget = QWidget()

        taobaoLabel = QLabel()
        logImage = QImage("TBTracker_Ui/tb_log.webp").scaled(int(148 * 0.8), int(66 * 0.8))
        taobaoLabel.setPixmap(QPixmap.fromImage(logImage))
        self.searchLineEdit = QLineEdit()
        self.searchLineEdit.setFont(q_1_Font)
        searchButton = SearchButton()
        searchButton.setFont(q_1_Font)
        searchButton.clicked.connect(self.call_spider)

        searchRegionLayout = QHBoxLayout()
        searchRegionLayout.setContentsMargins(240, 0, 240, 0)
        searchRegionLayout.setSpacing(20)
        searchRegionLayout.addWidget(taobaoLabel)
        searchRegionLayout.addWidget(self.searchLineEdit)
        searchRegionLayout.addWidget(searchButton)
        
        self.taobaoDataTable = QTableWidget(0, 4)
        self.taobaoDataTable.horizontalHeader().hide()
        self.taobaoDataTable.verticalHeader().hide()
        self.taobaoDataTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.taobaoDataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.progressBar = QProgressBar()
        
        self.productIDLineEdit = QLineEdit()
        self.productIDLineEdit.setFont(q_2_Font)
        productIDSaveButton = SaveButton()
        productIDSaveButton.setFont(q_2_Font)
        productIDSaveButton.clicked.connect(self.save_product_id)
        updateDataButton = UpdateButton()
        updateDataButton.setFont(q_2_Font)
        updateDataButton.clicked.connect(self.update_data)

        dataOperateLayout = QHBoxLayout()
        dataOperateLayout.setContentsMargins(500, 0, 0, 0)
        dataOperateLayout.addStretch()
        dataOperateLayout.setSpacing(20)
        dataOperateLayout.addWidget(self.productIDLineEdit)
        dataOperateLayout.addWidget(productIDSaveButton)
        dataOperateLayout.addWidget(updateDataButton)

        firstWidgetLayout = QVBoxLayout()
        firstWidgetLayout.setSpacing(10)
        firstWidgetLayout.addLayout(searchRegionLayout)
        firstWidgetLayout.addWidget(self.taobaoDataTable)
        firstWidgetLayout.addWidget(self.progressBar)
        firstWidgetLayout.addLayout(dataOperateLayout)

        firstWidget.setLayout(firstWidgetLayout)
        # ****************************************

        # ****************************************
        secondWidget = QWidget()
        self.DBTable = QTableWidget(0, 6)
        self.DBTable.setHorizontalHeaderLabels(["商品标识", "标题", "店铺名", "价格", "淘宝价", "是否删除数据？"])
        self.DBTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.DBTable.verticalHeader().setVisible(False)
        self.DBTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.addButton = AddButton()
        self.addButton.clicked.connect(self.add_data)
        deleteButton = DeleteButton()
        deleteButton.clicked.connect(self.delete_data)

        DBOperateLayout = QHBoxLayout()
        DBOperateLayout.addStretch()
        DBOperateLayout.setSpacing(20)
        DBOperateLayout.addWidget(self.addButton)
        DBOperateLayout.addWidget(deleteButton)

        secondWidgetLayout = QVBoxLayout()
        secondWidgetLayout.setSpacing(10)
        secondWidgetLayout.addWidget(self.DBTable)
        secondWidgetLayout.addLayout(DBOperateLayout)

        secondWidget.setLayout(secondWidgetLayout)
        # ****************************************

        # ****************************************
        thirdWidget = QWidget()
        
        self.wordCloudLabel = QLabel()
        self.wordCloudLabel.setAlignment(Qt.AlignCenter)
        self.wordCloudLabel.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.wordCloudLabel.setLineWidth(4)
        self.wordCloudLabel.setPixmap(QPixmap.fromImage(QImage("TBTracker_Ui/WordCloud.png")))

        self.productTree = QTreeWidget()
        self.productTree.setColumnCount(2)
        self.productTree.setHeaderLabels(['商品标识','商品数量'])
        self.productTree.header().setSectionResizeMode(QHeaderView.Stretch)
        productTreeLayout = QHBoxLayout()
        productTreeLayout.addWidget(self.productTree)

        exportButton = ExportButton()
        exportButton.clicked.connect(self.export_data)
        dataExportLayout = QHBoxLayout()
        dataExportLayout.addStretch()
        dataExportLayout.addWidget(exportButton)

        exportLayout = QVBoxLayout()
        exportLayout.setSpacing(20)
        exportLayout.addLayout(productTreeLayout)
        exportLayout.addLayout(dataExportLayout)

        thirdWidgetLayout = QHBoxLayout()
        thirdWidgetLayout.setSpacing(50)
        thirdWidgetLayout.setContentsMargins(50, 20, 50, 20)
        thirdWidgetLayout.addWidget(self.wordCloudLabel)
        thirdWidgetLayout.addLayout(exportLayout)
        
        thirdWidget.setLayout(thirdWidgetLayout)
        # ****************************************

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(firstWidget, "数据爬虫")
        self.tabWidget.addTab(secondWidget, "数据后台")
        self.tabWidget.addTab(thirdWidget, "数据导出")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 20, 50, 20)
        self.layout.addWidget(self.tabWidget)

    # 类方法重载 -- 关闭窗口事件
    def closeEvent(self, event):
        messageDialog = MessageDialog()
        reply = messageDialog.question(self, "消息提示对话框", "您要退出系统吗?", messageDialog.Yes | messageDialog.No, messageDialog.No)
        if reply == messageDialog.Yes:
            event.accept()
        else:
            event.ignore()
    
    @staticmethod
    def remove_pics():
        root_dir = 'TBTracker_Temp'
        for root, dirs, files in os.walk(root_dir):
            Logger.info('正在删除图片...')
            for filename in files:
                os.remove(root+'/'+filename)
            Logger.info('图片删除完毕!')

    def find_out_real_price(self, i, shop_url, match_price):
        title, price, taobao_price = "", "", ""
        try:
            html = requests.get(shop_url, timeout=10, headers=self.headers)
            Logger.info("第{0}家店铺的商品页面读取成功...".format(i))
            soup = BeautifulSoup(html.text, 'lxml')
            try:
                title = soup.find(name='h3', attrs={'class': 'tb-main-title'})['data-title'].strip()
            except TypeError as e:
                title = soup.find(name='div', attrs={'class': 'tb-detail-hd'}).find(name='h1').get_text().strip()
            try:
                price = soup.find(name='li', attrs={'id': 'J_StrPriceModBox'}). \
                    find(name='em', attrs={'class': 'tb-rmb-num'}).get_text().strip()
                if match_price != price:
                    taobao_price = match_price
            except Exception as e:
                try:
                    driver = webdriver.PhantomJS()
                    driver.set_window_size(800, 400)
                    driver.get(shop_url)
                    tm_price_panel = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'tm-price-panel')))
                    price = WebDriverWait(tm_price_panel, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'tm-price'))).text
                    driver.close()
                    if match_price != price:
                        taobao_price = match_price
                except Exception as e:
                    Logger.error(e)
        except Exception as e:
            Logger.error(e)
            Logger.warn('第{0}家店铺的商品页面读取失败...'.format(i))
        finally:
            if taobao_price == "":
                taobao_price = "无"
            return title, price, taobao_price

    def call_spider(self):
        searchWord = self.searchLineEdit.text()
        if searchWord != "":
            self.remove_pics()
            try:
                webDriver = webdriver.PhantomJS()
                webDriver.set_window_size(800, 400)
                try:
                    Logger.info("模拟登录淘宝网")
                    webDriver.get("https://www.taobao.com/")
                    try:
                        search_combobox = WebDriverWait(webDriver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'search-combobox-input-wrap')))
                        search_input = WebDriverWait(search_combobox, 10).until(
                            EC.presence_of_element_located((By.ID, 'q')))
                        # 发送搜索词
                        search_input.send_keys(searchWord.strip())

                        search_button_wrap = WebDriverWait(webDriver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'search-button')))
                        search_button = WebDriverWait(search_button_wrap, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'btn-search')))
                        search_button.click()
                        try:
                            Logger.info('搜索成功，正在返回搜索结果...')
                            main_srp_item_list = WebDriverWait(webDriver, 10).until(
                                EC.presence_of_element_located((By.ID, 'mainsrp-itemlist')))
                            m_item_list = WebDriverWait(main_srp_item_list, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'm-itemlist')))
                            items = WebDriverWait(m_item_list, 10).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, 'items')))[0]
                            allItems = WebDriverWait(items, 10).until(
                                EC.presence_of_all_elements_located((By.CLASS_NAME, 'item'))
                            )
                            self.returnCNT = len(allItems)
                            Logger.info('总共返回{0}个搜索结果'.format(self.returnCNT))

                            self.taobaoDataTable.setRowCount(self.returnCNT * 6)
                            imageLabel = [QLabel() for _ in range(self.returnCNT)]
                            titleItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            shopItem = [QTableWidgetItem("店铺：") for _ in range(self.returnCNT)]
                            shopValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            sourceItem = [QTableWidgetItem("来源地：") for _ in range(self.returnCNT)]
                            sourceValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            priceItem = [QTableWidgetItem("价格：") for _ in range(self.returnCNT)]
                            priceValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            tbPriceItem = [QTableWidgetItem("淘宝价：") for _ in range(self.returnCNT)]
                            tbPriceValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            dealItem = [QTableWidgetItem("付款人数：") for _ in range(self.returnCNT)]
                            dealValueItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            isJoinedItem = [QTableWidgetItem("是否加入价格跟踪队列？") for _ in range(self.returnCNT)]
                            checkItem = [QTableWidgetItem() for _ in range(self.returnCNT)]
                            self.URLList = []

                            # 抓取商品图
                            for (j, item) in enumerate(allItems):
                                try:
                                    Logger.info('正在爬取第{0}家店铺的数据...'.format(j + 1))
                                    itemPic = WebDriverWait(item, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'J_ItemPic')))
                                    itemPic_id = itemPic.get_attribute('id')
                                    itemPic_data_src = itemPic.get_attribute('data-src')
                                    if not itemPic_data_src.startswith("https:"):
                                        itemPic_data_src = "https:" + itemPic_data_src
                                    itemPic_alt = itemPic.get_attribute('alt').strip()
                                    if itemPic_id == "":
                                        random_serial = ""
                                        for _ in range(12):
                                            random_serial += str(random.randint(0, 10))
                                        itemPic_id = "J_Itemlist_Pic_" + random_serial

                                    Logger.info("正在爬取第{0}家店铺的商品图片...".format(j + 1))
                                    try:
                                        stream = requests.get(itemPic_data_src, timeout=10, headers=self.headers)
                                    except requests.RequestException as e:
                                        Logger.error(e)
                                    finally:
                                        Logger.info("第{0}家店铺的商品图片爬取完毕...".format(j + 1))
                                        try:
                                            im = Image.open(BytesIO(stream.content))
                                            if im.mode != 'RGB':
                                                im = im.convert('RGB')
                                            im.save("TBTracker_Temp/{0}.jpeg".format(itemPic_id))
                                            Logger.info("第{0}家店铺的商品图片保存完毕...".format(j + 1))
                                            self.taobaoDataTable.setSpan(j * 6, 0, 6, 1)
                                            imageLabel[j].setPixmap(QPixmap.fromImage(QImage("TBTracker_Temp/{0}.jpeg".format(itemPic_id)).scaled(int(230 * 0.7), int(230 * 0.7))))
                                            imageLabel[j].setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                            self.taobaoDataTable.setCellWidget(j * 6, 0, imageLabel[j])
                                        except Exception as e:
                                            Logger.error(e)
                                    
                                    item_price_and_link = WebDriverWait(item, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'J_ClickStat'))
                                    )

                                    item_match_price = item_price_and_link.get_attribute('trace-price')
                                    item_link = item_price_and_link.get_attribute('href')
                                    if not item_link.startswith("https:"):
                                        item_link = "https:" + item_link
                                    self.URLList.append(item_link)

                                    status_code = requests.get(item_link).status_code
                                    Logger.info(status_code)
                                    if status_code == 200:
                                        item_title, item_price, item_taobao_price = self.find_out_real_price(j+1, item_link, item_match_price)
                                        Logger.info('第{0}家店铺的商品价格和链接爬取完毕...'.format(j + 1))
                                        self.taobaoDataTable.setSpan(j * 6, 1, 1, 2)
                                        titleItem[j].setData(Qt.DisplayRole, QVariant(item_title))
                                        titleItem[j].setFont(self.table_1_Font)
                                        titleItem[j].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                        self.taobaoDataTable.setItem(j * 6, 1, titleItem[j])

                                        priceItem[j].setFont(self.table_2_Font)
                                        priceItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                        self.taobaoDataTable.setItem(j * 6 + 3, 1, priceItem[j])
                                        priceValueItem[j].setData(Qt.DisplayRole, QVariant(item_price))
                                        self.taobaoDataTable.setItem(j * 6 + 3, 2, priceValueItem[j])

                                        tbPriceItem[j].setFont(self.table_2_Font)
                                        tbPriceItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                        self.taobaoDataTable.setItem(j * 6 + 4, 1, tbPriceItem[j])
                                        tbPriceValueItem[j].setData(Qt.DisplayRole, QVariant(item_taobao_price))
                                        self.taobaoDataTable.setItem(j * 6 + 4, 2, tbPriceValueItem[j])
                                    else:
                                        Logger.warn('第{0}家店铺的商品价格和链接爬取失败...'.format(j + 1))

                                    item_deal = WebDriverWait(item, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'deal-cnt'))).text.strip()
                                    Logger.info('第{0}家店铺的商品交易量爬取完毕...'.format(j + 1))
                                    dealItem[j].setFont(self.table_2_Font)
                                    dealItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6 + 5, 1, dealItem[j])
                                    dealValueItem[j].setData(Qt.DisplayRole, QVariant(item_deal))
                                    self.taobaoDataTable.setItem(j * 6 + 5, 2, dealValueItem[j])

                                    row_3 = WebDriverWait(item, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'row-3')))
                                    item_shop_name = WebDriverWait(row_3, 10).until(
                                        EC.presence_of_all_elements_located((By.TAG_NAME, 'span')))[4].text.strip()
                                    Logger.info('第{0}家店铺的商铺名爬取完毕...'.format(j + 1))
                                    shopItem[j].setFont(self.table_2_Font)
                                    shopItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6 + 1, 1, shopItem[j])
                                    shopValueItem[j].setData(Qt.DisplayRole, QVariant(item_shop_name))
                                    self.taobaoDataTable.setItem(j * 6 + 1, 2, shopValueItem[j])

                                    item_location = WebDriverWait(row_3, 10).until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'location'))).text.strip()
                                    Logger.info('第{0}家店铺的货源地爬取完毕...'.format(j + 1))
                                    if item_location == "":
                                        item_location = "抓取为空"
                                    sourceItem[j].setFont(self.table_2_Font)
                                    sourceItem[j].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6 + 2, 1, sourceItem[j])
                                    sourceValueItem[j].setData(Qt.DisplayRole, QVariant(item_location))
                                    self.taobaoDataTable.setItem(j * 6 + 2, 2, sourceValueItem[j])

                                    isJoinedItem[j].setFont(self.table_1_Font)
                                    isJoinedItem[j].setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                    self.taobaoDataTable.setItem(j * 6, 3, isJoinedItem[j])
                                    self.taobaoDataTable.setSpan(j * 6 + 1, 3, 5, 1)
                                    checkItem[j].setCheckState(False)
                                    self.taobaoDataTable.setItem(j * 6 + 1, 3, checkItem[j])

                                    self.progressBar.setValue(math.ceil(((j + 1)/self.returnCNT) * 100))                              
                                except Exception as e:
                                    Logger.error(e)
                            messageDialog = MessageDialog()
                            messageDialog.information(self, "消息提示对话框", "数据爬取完毕!")
                            Logger.info("数据爬取完毕")
                            webDriver.close()
                        except NoSuchElementException as e:
                            webDriver.close()
                            Logger.error(e)
                    except NoSuchElementException as e:
                        webDriver.close()
                        Logger.error(e)
                except TimeoutException as e:
                    webDriver.close()
                    Logger.error(e)
            except WebDriverException as e:
                Logger.error(e)
        else:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示对话框", "请先输入搜索词!")
        
    def save_product_id(self):
        productID = self.productIDLineEdit.text()
        if productID != "":
            conn = sqlite.connect('TBTracker_DB/TBTrackerTag.db')
            c = conn.cursor()
            c.execute('select count(*) from tag where TagName="{}"'.format(productID))
            count = c.fetchone()[0]
            if count == 0:
                c.execute('insert into tag values ("{}", "{}")'.format(productID, get_current_system_time()))
                conn.commit()
                c.close()
                messageDialog = MessageDialog()
                messageDialog.information(self, "消息提示对话框", "标识成功入库!")
            else:
                messageDialog = MessageDialog()
                messageDialog.information(self, "消息提示对话框", "标识已经存在!")
        else:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示对话框", "请先填写商品标识!")

    def update_data(self):
        for j in range(self.returnCNT):
            flag = self.taobaoDataTable.item(j * 6 + 1, 3).checkState()
            if flag == 2:
                conn = sqlite.connect('TBTracker_DB/TBTracker.db')
                c = conn.cursor()
                c.execute('insert into product values ("{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(
                    self.productIDLineEdit.text(),
                    self.URLList[j],
                    self.taobaoDataTable.item(j * 6, 1).text(),
                    self.taobaoDataTable.item(j * 6 + 1, 2).text(),
                    self.taobaoDataTable.item(j * 6 + 3, 2).text(),
                    self.taobaoDataTable.item(j * 6 + 4, 2).text(), 
                    get_current_system_time()))
                conn.commit()
                c.close()
        messageDialog = MessageDialog()
        messageDialog.information(self, "消息提示对话框", "数据成功入库!") 

        self.show_database()
        self.plot_word_cloud()
        self.plot_product_tree()
    
    def export_data(self):
        pass

    def show_database(self):
        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()
        c.execute('select * from product order by CreateTime desc')
        queries = c.fetchall()
        self.DBCNT = len(queries)
        c.close()
        self.DBTable.setRowCount(self.DBCNT)
        for j in range(self.DBCNT):
            self.DBTable.setItem(j, 0, QTableWidgetItem(queries[j][0]))
            self.DBTable.setItem(j, 1, QTableWidgetItem(queries[j][2]))
            self.DBTable.setItem(j, 2, QTableWidgetItem(queries[j][3]))
            self.DBTable.setItem(j, 3, QTableWidgetItem(queries[j][4]))
            self.DBTable.setItem(j, 4, QTableWidgetItem(queries[j][5]))
            flag = QTableWidgetItem()
            flag.setCheckState(False)
            self.DBTable.setItem(j, 5, flag)

    def add_data(self):
        pass

    def delete_data(self):
        notDeleteCNT = 0
        for j in range(self.DBCNT):
            flag = self.DBTable.item(j, 5).checkState()
            if flag == 2:
                conn = sqlite.connect('TBTracker_DB/TBTracker.db')
                c = conn.cursor()
                c.execute('delete from product where ProductName="{}" and Title="{}" and ShopName="{}" and Price="{}"'.format(
                    self.DBTable.item(j, 0).text(), 
                    self.DBTable.item(j, 1).text(), 
                    self.DBTable.item(j, 2).text(), 
                    self.DBTable.item(j, 3).text()))
                conn.commit()
                c.close()
            else:
                notDeleteCNT += 1
        if notDeleteCNT == self.DBCNT:
            messageDialog = MessageDialog()
            messageDialog.warning(self, "消息提示对话框", "无效操作!")
        else:
            self.show_database()

    def plot_word_cloud(self):
        conn = sqlite.connect('TBTracker_DB/TBTrackerTag.db')
        c = conn.cursor()
        c.execute('select * from tag')
        tagQueries = c.fetchall()
        c.close()

        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()
        wordFreq = []
        for tagQuery in tagQueries:
            c.execute('select count(*) from product where ProductName="{}"'.format(tagQuery[0]))
            wordFreq.append((tagQuery[0], c.fetchone()[0]))
        c.close()

        wc = WordCloud(
            font_path="TBTracker_Font/wqy-microhei.ttc",
            width=420, 
            height=280,
            margin=10,
            max_words=500,
            background_color='white',
            max_font_size=50
        ).fit_words(wordFreq)
        wc.to_file("TBTracker_Ui/WordCloud.png")

        self.wordCloudLabel.setPixmap(QPixmap.fromImage(QImage("TBTracker_Ui/WordCloud.png")))

    def plot_product_tree(self):
        conn = sqlite.connect('TBTracker_DB/TBTrackerTag.db')
        c = conn.cursor()
        c.execute('select * from tag')
        tagQueries = c.fetchall()
        c.close()

        conn = sqlite.connect('TBTracker_DB/TBTracker.db')
        c = conn.cursor()
        roots = [QTreeWidgetItem(self.productTree) for _ in range(len(tagQueries))]
        for i, tagQuery in enumerate(tagQueries):
            roots[i].setText(0, tagQuery[0])
            roots[i].setFont(0, self.table_2_Font)
            roots[i].setCheckState(0, False)

            c.execute('select ShopName from product where ProductName="{}"'.format(tagQuery[0]))
            shopNames = [query[0] for query in c.fetchall()]
            childs = [QTreeWidgetItem(roots[i]) for _ in range(len(shopNames))]
            for j, child in enumerate(childs):
                child.setText(0, shopNames[j])
                child.setFont(0, self.table_1_Font)
                child.setCheckState(0, False)
                c.execute('select count(*) from product where ProductName="{}" and ShopName="{}"'.format(tagQuery[0], shopNames[j]))
                child.setText(1, str(c.fetchone()[0]))
            
            self.productTree.addTopLevelItem(roots[i])

        c.close()

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            pass
            # if 75 <= event.pos().x() <= 135 and 5 <= event.pos().y() <= 25:
            # if 145 <= event.pos().x() <= 215 and 5 <= event.pos().y() <= 25:
        return QWidget.eventFilter(self, source, event)
        

class TBTrackerAddDataWindow(QWidget):
    def __init__(self):
        super(TBTrackerAddDataWindow, self).__init__()
        self.create_main_window()

    def create_main_window(self):
        self.setWindowTitle("添加数据")
        self.setWindowIcon(QIcon('TBTracker_Ui/python.png'))
        self.setMinimumSize(500, 350)
        self.setMaximumSize(500, 350)
        self.set_widgets()
        self.setLayout(self.layout)

    def set_widgets(self):
        self.productIDLineEdit = QLineEdit()
        self.URLLineEdit = QLineEdit()
        self.titleLineEdit = QLineEdit()
        self.shopNameLineEdit = QLineEdit()
        self.priceLineEdit = QLineEdit()
        self.taobaoPriceLineEdit = QLineEdit()
        self.createTimeLineEdit = QLineEdit()

        inputLayout = QGridLayout()
        inputLayout.addWidget(QLabel("商品标识"), 0, 0, 1, 1)
        inputLayout.addWidget(self.productIDLineEdit, 0, 1, 1, 3)
        inputLayout.addWidget(QLabel("URL"), 1, 0, 1, 1)
        inputLayout.addWidget(self.URLLineEdit, 1, 1, 1, 3)
        inputLayout.addWidget(QLabel("标题"), 2, 0, 1, 1)
        inputLayout.addWidget(self.titleLineEdit, 2, 1, 1, 3)
        inputLayout.addWidget(QLabel("店铺名"), 3, 0, 1, 1)
        inputLayout.addWidget(self.shopNameLineEdit, 3, 1, 1, 3)
        inputLayout.addWidget(QLabel("价格"), 4, 0, 1, 1)
        inputLayout.addWidget(self.priceLineEdit, 4, 1, 1, 3)
        inputLayout.addWidget(QLabel("淘宝价"), 5, 0, 1, 1)
        inputLayout.addWidget(self.taobaoPriceLineEdit, 5, 1, 1, 3)

        self.confirmButton = ConfirmButton()
        self.confirmButton.clicked.connect(self.confirm)
        cancelButton = CancelButton()
        cancelButton.clicked.connect(self.cancel)

        operateLayout = QHBoxLayout()
        operateLayout.addStretch()
        operateLayout.setSpacing(20)
        operateLayout.addWidget(self.confirmButton)
        operateLayout.addWidget(cancelButton)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(50, 20, 50, 20)
        self.layout.setSpacing(10)
        self.layout.addLayout(inputLayout)
        self.layout.addLayout(operateLayout)

    def confirm(self):
        pass

    def cancel(self):
        self.close()
    