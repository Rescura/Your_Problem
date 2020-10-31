import sys
import os

# GUI에 필요한 모듈과 라이브러리 임포트
from PyQt5 import QtWidgets
from QtApplicationPart.MainGui import MainWindow
from PyQt5 import QtGui
if __name__ == "__main__" :

    # MainGui.py의 MainWindow 인스턴스를 만들어 화면에 띄움
    app = QtWidgets.QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont("\\QtApplicationPart\\Resources\\Tmoney RoundWind.ttf")
    QtGui.QFontDatabase.addApplicationFont("\\QtApplicationPart\\Resources\\SpoqaHanSans-Regular.ttf")
    myWindow = MainWindow() 
    myWindow.show()
    app.exec_()