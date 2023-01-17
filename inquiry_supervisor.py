import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore
import numpy as np
import pyqtgraph as pg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


form_class = uic.loadUiType("store.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # ui 시작 인덱스 0으로 고정
        self.stackedWidget.setCurrentIndex(4)
        self.inquiry_supervisor()
        self.inquiry_tableWidget.setColumnWidth(1, 320)
        self.inquiry_tableWidget.setColumnWidth(2, 250)
        self.inquiry_tableWidget.cellClicked.connect(self.inquiry_table_clicked)
        self.inquiry_tableWidget.cellDoubleClicked.connect(self.inquiry_table_clicked)

        self.answer_btn.clicked.connect(self.replied)
        # self.btn_search.clicked.connect(self.search)

########그래프


        #
        # self.table.setColumnWidth(3, 357)
    def inquiry_supervisor(self):
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='restaurant',
                               charset='utf8')  # password 변경 해주세요
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()
        ## SQL문 실행
        # sql = f"select * from jejudoweather where jijum_name = '{self.combo_selected}'"
        sql = f"SELECT * FROM inquiries"
        cur.execute(sql)
        requiry = cur.fetchall()
        print(requiry)
        self.inquiry_tableWidget.setRowCount(len(requiry))  # 테이블의 행 갯수를 rows의 길이로 정함
        self.inquiry_tableWidget.setColumnCount(len(requiry[0]))
        for i in range(len(requiry)):
            for j in range(len(requiry[i])):
                self.inquiry_tableWidget.setItem(i, j, QTableWidgetItem(str(requiry[i][j])))

    def inquiry_table_clicked(self, row, col):
        data = self.inquiry_tableWidget.item(row, col)
        print("셀 클릭 셀 값 : ", data.text())
        self.clicked_inquiry = data.text()



    def replied(self):
        reply1 = self.answer_lineEdit.text()

        conn = pymysql.connect(host='localhost', user='root', password='0000', db='restaurant',
                               charset='utf8')  # password 변경 해주세요
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()
        print(reply1, 'ok')
        sql1 = f"update restaurant.inquiries set reply = '{reply1}' where customer_id = '{self.clicked_inquiry}' or inquiry = '{self.clicked_inquiry}'"
        sql = f"select * from inquiries"
        cur.execute(sql1)

        cur.execute(sql)
        requiry = cur.fetchall()
        print(requiry)
        conn.commit()

        for i in range(len(requiry)):
            for j in range(len(requiry[i])):
                self.inquiry_tableWidget.setItem(i, j, QTableWidgetItem(str(requiry[i][j])))

#감사합니다. 고객님. 앞으로도 열심히 노력하는 은희네해장국이 되겠습니다.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
