import sys
from PyQt5.uic import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import MySQLdb
class PoertyDialogui(QMainWindow):        
    def __init__(self,context):
        super(PoertyDialogui, self).__init__() #初始化
        self.ui = loadUi(r'poetryDialog.ui', self)#加载ui
        self.setFixedSize(self.width(), self.height()); 
        self.setWindowIcon(QIcon("title.jpg"))
        self.ui.textEdit.setText(context)


