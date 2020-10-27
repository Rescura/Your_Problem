import sys
import requests
import pytz
from datetime import datetime
from PyQt5 import QtWidgets
from colorama import init, Fore

import requests
from pathlib import Path
from pprint import pprint

init(autoreset=True)

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

        # 1번 페이지
        self.ui.goToPage2Btn.clicked.connect(self.goToPage2)
        # 2번 페이지
        self.ui.goToPage3Btn.clicked.connect(self.goToPage3)
        # 3번 페이지
        self.ui.postProblemBtn.clicked.connect(self.postProblem)
        self.ui.backToPage2Btn.clicked.connect(self.backToPage2)
        # 4번 페이지
        self.ui.goToPage5Btn.clicked.connect(self.goToPage5)
        # 5번 페이지
        self.ui.backToPage4Btn.clicked.connect(self.backToPage4)
        self.ui.postReplyBtn.clicked.connect(self.postReply)

    def goToPage2(self):
        print("[goToPage2Btn Clicked] : 두번째 페이지로 이동합니다.")
        self.ui.stackedWidget.setCurrentIndex(1)

    def goToPage3(self):
        self.userName = self.ui.nameLineEdit.text()
        if self.userName == '': 
            # self.ui.nameLabel.setStyleSheet('')
            print(f"{Fore.RED}[goToPage3Btn Clicked] : 이름이 입력되지 않았습니다!")
            self.ui.nameLabel.setText('불리고 싶은 이름을 입력해주세요!')
        else:
            print("[goToPage3Btn Clicked] : 세번째 페이지로 이동합니다.")
            self.ui.stackedWidget.setCurrentIndex(2)

    def PostProblem(self):
        print("[postProblemClick Clicked] : 고민 내용을 모아서 서버에 업로드를 시도합니다.")
        _problemTitle = self.ui.problemTitleTextEdit.toPlainText()
        _problemTime = datetime.now(pytz.timezone('Asia/Seoul')).strftime(r'%Y-%m-%d %H:%M:%S')
        _problemContent = self.ui.problemContentTextEdit.toPlainText()
        
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
    
    def backToPage2(self):
        pass
    
    def goToPage5(self):
        pass

    def backToPage4(self):
        pass

    def postReply(self):
        pass

    

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MainWindow() 
    myWindow.show()
    app.exec_()