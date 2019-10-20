# 2019-9-20

import re
import sys
import requests
import json
import time
import threading
import js2py
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

decode_service_code='''
    function get_service_code(service_code, r_value){

    var a,e,n,t,f,d,h,i = "yL/M=zNa0bcPQdReSfTgUhViWjXkYIZmnpo+qArOBs1Ct2D3uE4Fv5G6wHl78xJ9K",
    o = "",
    c = 0;
    for (r_value = r_value.replace(/[^A-Za-z0-9+/=]/g,""); c < r_value.length;) {
        t = i.indexOf(r_value.charAt(c++));
        f = i.indexOf(r_value.charAt(c++));
        d = i.indexOf(r_value.charAt(c++));
        h = i.indexOf(r_value.charAt(c++));
        a = t << 2 | f >> 4;
        e = (15 & f) << 4 | d >> 2;
        n = (3 & d) << 6 | h;
        o += String.fromCharCode(a);
        64 != d && (o += String.fromCharCode(e));
        64 != h && (o += String.fromCharCode(n));
        }
        var tvl = o;
        var fi = parseInt(tvl.substr(0,1));
        fi = fi > 5 ? fi - 5 : fi + 4;
        var _r = tvl.replace(/^./, fi);
        var _rs = _r.split(",");
        var replace = "";
        for (e = 0; e < _rs.length; e++) replace += String.fromCharCode(2 * (_rs[e] - e - 1) / (13 - e - 1));
        return service_code.replace(/(.{10})$/, replace)
    }
    '''
decode_service_code = js2py.eval_js(decode_service_code)

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

        user_id = self.usid.text()
        # convert to service_code_origin - decode_service_code
        req = SESS.get('https://gallog.dcinside.com/%s/posting'%user_id)
        soup = BeautifulSoup(req.text,'lxml')

        service_code_origin = soup.find('input', {'name' : 'service_code'})['value']

        data  = soup.select("script")[29]

        cut_1 = "var _r = _d"
        cut_2 = '<script type="text/javascript">'
        cut_3 = "</script>"

        cut_data = str(data).replace(cut_1,"")
        cut_data = str(cut_data).replace(cut_2,"")
        cut_data = str(cut_data).replace(cut_3,"")
        _r = re.sub("\n","",str(cut_data))
        r_value = re.sub("['();]","",str(_r))
        r_value = str(r_value)
        # 정규식

        service_code = decode_service_code(service_code_origin, r_value)

        if LOGIN_FLAG == True:  

                
            global DEL_FLAG
            DEL_FLAG = []
            self.progress.setText("    POST-DEL...")
            time.sleep(0.2)
            thr = (threading.Thread(target=del_pos,args=(SESS,DEL_FLAG,user_id,service_code)))
            thr.start()
            self.p_d_btn.setEnabled(False)
            self.r_d_btn.setEnabled(False)
            self.p_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")
            self.r_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")

        else:

            self.progress.setText("    로그인 해줘요!")
        
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

        user_id = self.usid.text()
        # convert to service_code_origin - decode_service_code
        req = SESS.get('https://gallog.dcinside.com/%s/posting'%user_id)
        soup = BeautifulSoup(req.text,'lxml')

        service_code_origin = soup.find('input', {'name' : 'service_code'})['value']

        data  = soup.select("script")[29]

        cut_1 = "var _r = _d"
        cut_2 = '<script type="text/javascript">'
        cut_3 = "</script>"

        cut_data = str(data).replace(cut_1,"")
        cut_data = str(cut_data).replace(cut_2,"")
        cut_data = str(cut_data).replace(cut_3,"")
        _r = re.sub("\n","",str(cut_data))
        r_value = re.sub("['();]","",str(_r))
        r_value = str(r_value)
        # 정규식

        service_code = decode_service_code(service_code_origin, r_value)

        if LOGIN_FLAG == True:  

                
            global DEL_FLAG
            DEL_FLAG = []
            self.progress.setText("    CMT-DEL...")
            time.sleep(0.2)
            thr = (threading.Thread(target=del_com,args=(SESS,DEL_FLAG,user_id,service_code)))
            thr.start()
            self.p_d_btn.setEnabled(False)
            self.r_d_btn.setEnabled(False)
            self.p_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")
            self.r_d_btn.setStyleSheet("border:1px solid #ccc; background-color : #5f7b89; color : white;")

        else:

            self.progress.setText("    로그인 해줘요!")

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

