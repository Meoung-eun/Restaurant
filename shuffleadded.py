import pymysql
import sys
import random
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
        self.stackedWidget.setCurrentIndex(0)
        #메뉴 - 로그아웃, 관리 버튼
        self.logout_btn.clicked.connect(self.to_logout)
        self.product_btn.clicked.connect(self.to_product)
        self.order_btn.clicked.connect(self.to_order)
        self.question_btn.clicked.connect(self.to_question)
        self.inventory_btn.clicked.connect(self.to_inventory)

        ##로그인 창: [회원가입] 버튼
        self.join_btn.clicked.connect(self.to_stackJoin)
        ##로그인 창 : [로그인] 버튼
        self.login_btn.clicked.connect(self.login)
        self.login_done = False

        ##회원가입 창:  [가입하기] 버튼
        self.join_btn_2.clicked.connect(self.to_join)
        # 회원가입 창 : 유효성 검사
        self.join_id.textChanged.connect(self.joincheck)
        self.join_pw.textChanged.connect(self.joincheck)
        self.join_pw_chk.textChanged.connect(self.joincheck)
        # 회원가입 창: [로그인창으로 이동] 버튼
        self.toLogin_btn.clicked.connect(self.to_loginpage)

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
        requiry_list = []
        for i in requiry:
            requiry_list.append(i)
        print(requiry_list)
        print('yahoo', requiry_list)
        conn.commit()

        for i in range(len(requiry_list)):
            for j in range(len(requiry_list[i])):
                self.inquiry_tableWidget.setItem(i, j, QTableWidgetItem(str(requiry_list[i][j])))



#감사합니다. 고객님. 앞으로도 열심히 노력하는 은희네해장국이 되겠습니다.
    def to_logout(self): #로그아웃버튼누를시
        if self.login_done:
            self.login_done = False
            self.stackedWidget.setCurrentIndex(0)
            self.login_id.clear()
            self.login_pw.clear()
        else:QtWidgets.QMessageBox.information(self, "알림", "로그아웃 상태입니다.")
    def to_product(self): # 상품관리 메뉴 버튼누를시
        if self.login_done:self.stackedWidget.setCurrentIndex(2)
        else:QtWidgets.QMessageBox.information(self, "알림", "로그인 후에 이용 가능합니다.")
    def to_order(self): # 주문관리 메뉴 버튼누를시
        if self.login_done:self.stackedWidget.setCurrentIndex(3)
        else:QtWidgets.QMessageBox.information(self, "알림", "로그인 후에 이용 가능합니다.")
    def to_question(self): # 문의관리 메뉴 버튼누를시
        if self.login_done:self.stackedWidget.setCurrentIndex(4)
        else:QtWidgets.QMessageBox.information(self, "알림", "로그인 후에 이용 가능합니다.")
        conn = pymysql.connect(host='localhost', user='root', password='0000', db='restaurant',
                               charset='utf8')  # password 변경 해주세요
        ## conn로부터  결과를 얻어올 때 사용할 Cursor 생성
        cur = conn.cursor()
        sql = f"select * from inquiries"
        cur.execute(sql)
        requiry = cur.fetchall()
        print(requiry)
        requiry_list = []
        for i in requiry:
            requiry_list.append(i)
        print(requiry_list)
        print('yahoo', requiry_list)
        conn.commit()

        for i in range(len(requiry_list)):
            for j in range(len(requiry_list[i])):
                self.inquiry_tableWidget.setItem(i, j, QTableWidgetItem(str(requiry_list[i][j])))


    def to_inventory(self):  # 재고관리 메뉴 버튼누를시
        if self.login_done:self.stackedWidget.setCurrentIndex(5)
        else:QtWidgets.QMessageBox.information(self, "알림", "로그인 후에 이용 가능합니다.")

    ##로그인 창: [회원가입] 버튼
    def to_stackJoin(self):
        self.stackedWidget.setCurrentIndex(1)

    # 회원가입 창: [로그인창으로 이동] 버튼
    def to_loginpage(self):
        self.stackedWidget.setCurrentIndex(0)

    ##로그인 창 : [로그인] 버튼
    def login(self):
        print('login')
        con = pymysql.connect(host='localhost', user='root', password='0000',
                              db='restaurant', charset='utf8')  # 한글처리 (charset = 'utf8')
        cur = con.cursor()
        sql = f"SELECT * FROM restaurant.user"
        cur.execute(sql)
        userRows = cur.fetchall()
        print(userRows)
        for i in range(len(userRows)):
            for j in range(len(userRows[i])):
                if userRows[i][0] == self.login_id.text() and userRows[i][1] == self.login_pw.text():
                    self.login_done = True
                elif userRows[i][0] != self.login_id.text() or userRows[i][1] != self.login_pw.text():
                    print('회원정보가없습니다')

        if self.login_done == False :
            QtWidgets.QMessageBox.information(self, "로그인", "회원 정보가 없습니다.")
        elif self.login_done:
            self.stackedWidget.setCurrentIndex(2)

    # 회원가입 창 : 유효성 검사
    def joincheck(self):
        if self.join_id.text() != '' and self.join_pw.text() != '' and self.join_pw_chk.text() != '' and self.join_pw.text() == self.join_pw_chk.text():
            self.join_btn_2.setEnabled(True) # 라인에디트 모두 입력해야 하고 비번과 비번확인란이 같아야함
        else:
            self.join_btn_2.setEnabled(False)

        if self.join_pw.text() != self.join_pw_chk.text():
            self.label_pwck.setText('비밀번호가 일치하지 않습니다.')
        else:
            self.label_pwck.setText('비밀번호 일치')

        if self.join_pw.text() == '' and self.join_pw_chk.text() == '':
            self.label_pwck.setText('')

    ##회원가입 창:  [가입하기] 버튼
    def to_join(self):
        print('가입됨')
        con = pymysql.connect(host='localhost', user='root', password='0000',
                              db='restaurant', charset='utf8')  # 한글처리 (charset = 'utf8')
        cur = con.cursor()
        sql = f"INSERT INTO restaurant.user (ID,PW) VALUES ('{self.join_id.text()}', '{self.join_pw_chk.text()}')"
        cur.execute(sql)
        con.commit()
        QtWidgets.QMessageBox.information(self, "회원가입", "회원가입이 완료되었습니다.")
        self.join_id.clear()
        self.join_pw.clear()
        self.join_pw_chk.clear()
        self.stackedWidget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
