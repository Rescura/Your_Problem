import sys
import requests
import pytz
from datetime import datetime
from PyQt5 import QtWidgets

import requests
from pathlib import Path
from pprint import pprint



# 필요한 클래스 임포트
# MainGui.py를 직접 실행하면 ui_main 모듈안에 있는 클래스를 임포트 시켜야 함
# main.py를 실행하면 QtApplicationPart 패키지로 접근해 ui_main 모듈안에 있는 클래스를 임포트 시켜야 함 
if __name__ == '__main__':  from ui_main import Ui_MainWindow
else : from QtApplicationPart.ui_main import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow) :
    def __init__(self) :
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("너의 이름은")
        self.userName = 'No Username'

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.nextButton1.clicked.connect(self.onNextButton1Click)
        self.ui.nextButton2.clicked.connect(self.onNextButton2Click)
        self.ui.backButton.clicked.connect(self.onBackButtonClick)
        self.ui.sendButton.clicked.connect(self.onSendButtonClick)

    def onNextButton1Click(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        print("[nextButton1 Clicked] : 두번째 페이지로 이동합니다.")

    def onNextButton2Click(self):
        self.userName = self.ui.nameLineEdit.text()
        if self.userName == '': 
            # self.ui.nameLabel.setStyleSheet('')
            self.ui.nameLabel.setText('불리고 싶은 이름을 입력해주세요!')
        else :
            self.ui.stackedWidget.setCurrentIndex(2)
        print("[nextButton2 Clicked] : 세번째 페이지로 이동합니다.")

    def onBackButtonClick(self):
        print("[backButton Clicked] : 두번째 페이지로 이동합니다.")
        self.ui.stackedWidget.setCurrentIndex(1)


    def onSendButtonClick(self):
        print("[sendButton Clicked] : 고민 내용을 모아서 서버에 업로드를 시도합니다.")
        _problemTitle = self.ui.titleTextEdit.toPlainText()
        _problemTime = datetime.now(pytz.timezone('Asia/Seoul')).strftime(r'%Y-%m-%d %H:%M:%S')
        _problemContent = self.ui.problemTextEdit.toPlainText()
        
        res = requests.post('http://127.0.0.1:5000/problems/',
            data={
                "problemTitle" : _problemTitle,
                "problemAuthor" : self.userName,
                "problemTime" : _problemTime,
                "problemContent" : _problemContent
                })

        res_json = res.json()
        if res_json["Message"] != 'Post Successful':
            self.ui.consoleLabel.setText('고민을 서버에 업로드하는데 실패했습니다!')
        else :
            self.ui.consoleLabel.setText('고민을 서버에 성공적으로 업로드했습니다!')
            self.ui.stackedWidget.setCurrentIndex(3)

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MainWindow() 
    myWindow.show()
    app.exec_()