import sys
import requests
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

        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.nextButton1.clicked.connect(self.onNextButton1Click)
        self.ui.nextButton2.clicked.connect(self.onNextButton2Click)
        self.ui.backButton.clicked.connect(self.onBackButtonClick)
        self.ui.sendButton.clicked.connect(self.onSendButtonClick)

    def onNextButton1Click(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        print("[nextButton1 Clicked] : 두번째 페이지로 이동합니다.")

    def onNextButton2Click(self):
        userName = self.ui.nameLineEdit.text()
        if userName == '': 
            # self.ui.nameLabel.setStyleSheet('')
            self.ui.nameLabel.setText('불리고 싶은 이름을 입력해주세요!')
        self.ui.stackedWidget.setCurrentIndex(2)
        print("[nextButton2 Clicked] : 세번째 페이지로 이동합니다.")

    def onBackButtonClick(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        print("[backButton Clicked] : 두번째 페이지로 이동합니다.")


    def onSendButtonClick(self):
        problemHtmlText = self.ui.problemTextEdit.toHtml()
        print(problemHtmlText)
        
        # 고민을 textEdit HTML 형식으로 저장시킴
        with open('problem.html', 'w', encoding='utf8') as f:
            f.write(problemHtmlText)

        
        #TODO : 서버에 전송하기


if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MainWindow() 
    myWindow.show()
    app.exec_()