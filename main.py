# 2019-9-17

import re
import sys
import requests
import json
import time
import threading
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from login_py import login

from posting_del import del_pos
from comment_del import del_com

LOGIN_FLAG = False

class MainWindow(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        #========================== 로그인 영역 시작 ==========================
        group_login = QGroupBox("로그인", self)
        group_login.move(10, 10)
        group_login.resize(275, 97)
        group_login.setFont(QFont("Yoon 윤고딕 550_TT",12))


        self.usid = QLineEdit(self)
        self.usid.move(25, 35)
        self.usid.resize(150,25)
        self.usid.setPlaceholderText("아이디") 
        self.usid.setFont(QFont("-윤고딕330"))

        self.uspw = QLineEdit(self)
        self.uspw.move(25, 65)
        self.uspw.resize(150,25)
        self.uspw.setEchoMode(QLineEdit.Password)
        self.uspw.setPlaceholderText("비밀번호") 
        self.uspw.setFont(QFont("-윤고딕330"))

        self.l_btn = QPushButton("LOGIN", self)
        self.l_btn.move(185, 35)
        self.l_btn.resize(85,55)
        self.l_btn.setStyleSheet("border:1px solid #ccc; background-color : #37474f; color : white;")
        self.l_btn.setFont(QFont("Yoon 윤고딕 550_TT"))
        self.l_btn.clicked.connect(self.execute_login)
        #========================== 로그인 영역 끝 ==========================


        #========================== 삭제 영역 시작 ==========================
        group_del = QGroupBox("삭제", self)
        group_del.move(10, 125)
        group_del.resize(275, 97)
        group_del.setFont(QFont("Yoon 윤고딕 550_TT",12))
        
        self.p_d_btn = QPushButton("글삭제", self)
        self.p_d_btn.move(23, 155)
        self.p_d_btn.resize(115,50)
        self.p_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #37474f; color : white;")
        self.p_d_btn.setFont(QFont("Yoon 윤고딕 550_TT"))
        self.p_d_btn.clicked.connect(self.execute_main_p)

        self.r_d_btn = QPushButton("리플삭제", self)
        self.r_d_btn.move(155, 155)
        self.r_d_btn.resize(115,50)
        self.r_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #37474f; color : white;")
        self.r_d_btn.setFont(QFont("Yoon 윤고딕 550_TT"))
        self.r_d_btn.clicked.connect(self.execute_main_c)

        #========================== 삭제 영역 끝 ==========================

        
        #========================== 부가 영역 시작 ==========================
        self.progress = QLabel("    로그인 전",self)
        self.progress.move(0,240)
        self.progress.resize(300,30)
        self.progress.setStyleSheet("background-color : #403e41; color : white;")
        self.progress.setFont(QFont("Yoon 윤고딕 550_TT"))

        self.setWindowTitle("Cleaner")
        self.setFixedSize(300,270)
        self.setWindowIcon(QIcon("asset\icon.jpg"))
        self.setStyleSheet("background-color: #FFFFFF;")
        self.show()
        #========================== 부가 영역 끝 ==========================


    def execute_login(self):

        usid = self.usid.text()
        uspw = self.uspw.text()

        login_session = login(usid,uspw)

        global SESS
        SESS = login_session

        try:

            if 'gn_cookie' in SESS.cookies:

                self.progress.setText("    로그인 성공")
                self.usid.setEnabled(False)
                self.uspw.setEnabled(False)
                self.l_btn.setEnabled(False)
                global LOGIN_FLAG
                LOGIN_FLAG = True

        except Exception as ex:

            print (ex)
            self.progress.setText("    로그인 실패")
            pass
    

    def execute_main_p(self):
        
        def process():

            if LOGIN_FLAG == True:  
                
                global DEL_FLAG
                DEL_FLAG = []

                usid = self.usid.text()
                self.progress.setText("    POST-DEL...")
                self.p_d_btn.setEnabled(False)
                self.r_d_btn.setEnabled(False)
                self.p_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")
                self.r_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")

                thr = (threading.Thread(target=del_pos,args=(SESS,DEL_FLAG,usid)))
                thr.start()

            else:

                self.progress.setText("    로그인 해줘요!")

        process()   
        
        def check():

            while True:
                
                if 'True' in DEL_FLAG:

                    self.progress.setText("    DEL-END-!")
                    self.p_d_btn.setEnabled(True)
                    self.r_d_btn.setEnabled(True)
                    self.p_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #37474f; color : white;")
                    self.r_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #37474f; color : white;")
                    break
                
                else:
                    pass

        chk = (threading.Thread(target=check))
        chk.start()           

    def execute_main_c(self):
        
        def process():

            if LOGIN_FLAG == True:
                
                global DEL_FLAG
                DEL_FLAG = []

                usid = self.usid.text()
                self.progress.setText("    CMT-DEL...")
                self.p_d_btn.setEnabled(False)
                self.r_d_btn.setEnabled(False)
                self.p_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")
                self.r_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")

                thr = (threading.Thread(target=del_com,args=(SESS,DEL_FLAG,usid)))
                thr.start()

            else:

                self.progress.setText("    로그인 해줘요!")
        
        process()

        def check():

            while True:
                
                if 'True' in DEL_FLAG:

                    self.progress.setText("    DEL-END-!")
                    self.p_d_btn.setEnabled(True)
                    self.r_d_btn.setEnabled(True)
                    self.p_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #37474f; color : white;")
                    self.r_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #37474f; color : white;")

                    break
                
                else:
                    pass

        chk = (threading.Thread(target=check))
        chk.start()


if __name__ == "__main__": 


    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_())

