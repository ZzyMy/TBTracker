# -*- coding: utf-8 -*-
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

'''
@author  : Zhou Jian
@email   : zhoujian@hust.edu.cn
@version : V1.0
@date    : 2017.01.24
'''

class BaseButton(QPushButton):
    '''
    基类按钮
    '''
    def __init__(self, name=""):
        super(BaseButton, self).__init__(name)


class SearchButton(BaseButton):
    '''
    搜素按钮，继承自基类按钮
    '''
    def __init__(self):
        super(SearchButton, self).__init__(name="搜索")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class SaveButton(BaseButton):
    '''
    保存按钮，继承自基类按钮
    '''
    def __init__(self):
        super(SaveButton, self).__init__(name="标识入库")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class UpdateButton(BaseButton):
    '''
    更新按钮，继承自基类按钮
    '''
    def __init__(self):
        super(UpdateButton, self).__init__(name="导入数据")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class ExportButton(BaseButton):
    '''
    导出按钮，继承自基类按钮
    '''
    def __init__(self):
        super(ExportButton, self).__init__(name="导出数据")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class AddButton(BaseButton):
    '''
    增加数据按钮，继承自基类按钮
    '''
    def __init__(self):
        super(AddButton, self).__init__(name="增加数据")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class DeleteButton(BaseButton):
    '''
    删除数据按钮，继承自基类按钮
    '''
    def __init__(self):
        super(DeleteButton, self).__init__(name="删除数据")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class ConfirmButton(BaseButton):
    '''
    确定按钮，继承自基类按钮
    '''
    def __init__(self):
        super(ConfirmButton, self).__init__(name="确定")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class CancelButton(BaseButton):
    '''
    取消按钮，继承自基类按钮
    '''
    def __init__(self):
        super(CancelButton, self).__init__(name="取消")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass

class AllSelectButton(BaseButton):
    '''
    全选按钮，继承自基类按钮
    '''
    def __init__(self):
        super(AllSelectButton, self).__init__(name="全部选择")
        self.function_init()
    
    # 功能绑定 - 
    def function_init(self):
        pass
    