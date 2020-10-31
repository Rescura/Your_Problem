import sys
import random
import requests
import pytz
import pymysql
from pathlib import Path
from pprint import pprint
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from colorama import init, Fore, Back


init(autoreset=True)

# 필요한 클래스 임포트
# MainGui.py를 직접 실행하면 ui_main 모듈안에 있는 클래스를 임포트 시켜야 함
# main.py를 실행하면 QtApplicationPart 패키지로 접근해 ui_main 모듈안에 있는 클래스를 임포트 시켜야 함 
if __name__ == '__main__':  from ui_main import Ui_MainWindow
else : from QtApplicationPart.ui_main import Ui_MainWindow

def logPrint(f_string: str, mode: str='norm'):
    ''' 일반적 프린트: norm
        GUI 변경: gui
        함수 첫 실행: init
        값 체크: check
        오류: fatal'''

    res_string = f_string
    if mode == 'init':
        res_string = f'{Fore.BLACK}{Back.WHITE}' + f_string

    elif mode == 'gui':
        res_string = f'{Fore.CYAN}' + f_string

class MainWindow(QtWidgets.QMainWindow) :
    def __init__(self) :
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("너의 이름은")
        self.userName = 'No Username'
        self.myProblemId = 0 
        self.otherProblemId = 0
        self.ui.stackedWidget.setCurrentIndex(0)

        # 0번(첫화면) 페이지 함수들
        self.ui.goToPage1Btn.clicked.connect(self.goToPage1)

        # 1번(이름입력) 페이지 함수들
        self.ui.goToPage2Btn.clicked.connect(self.goToPage2)
        
        # 2번(자신고민입력) 페이지 함수들
        self.ui.backToPage1Btn.clicked.connect(self.backToPage1)
        self.ui.postProblemBtn.clicked.connect(self.postProblem) # 나의 고민을 포스트함
        self.ui.postProblemBtn.clicked.connect(self.requestProblems) # 다른 사람의 고민들을 요청해서 받아옴
        self.ui.postProblemBtn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(4)) # 4번 페이지로 이동
        # self.ui.postProblemBtn.clicked.connect(self.requestOneProblem)
        
        # 3번(다른고민선택) 페이지 함수들
        self.ui.goToPage4Btn.clicked.connect(self.goToPage5)
        
        # 4번(답장보내기) 페이지 함수들
        self.ui.backToPage3Btn.clicked.connect(self.backToPage3)
        self.ui.postReplyBtn.clicked.connect(self.postReply)
        self.ui.postReplyBtn.clicked.connect(self.goToPage6)

        # 5번(대기화면) 페이지 함수들

    def goToPage1(self):
        print(f"{Fore.BLACK}{Back.WHITE}[goToPage1() - 실행됨] : Page0 -> Page1으로 이동합니다.")
        self.ui.stackedWidget.setCurrentIndex(1)

    def goToPage2(self):
        self.userName = self.ui.nameLineEdit.text()

        if self.userName == '': 
            print(f"{Fore.YELLOW}[goToPage2() - 경고] : 이름이 입력되지 않았습니다!")
            self.ui.nameLabel.setText('불리고 싶은 이름을 입력해주세요!')
        else:
            print(f"{Fore.BLACK}{Back.WHITE}[goToPage2() - 실행됨] : Page1 -> Page2으로 이동합니다.")
            self.ui.stackedWidget.setCurrentIndex(2)
            
            # TODO : 로컬에서 전구 불빛 조정하기
            # requests.get('http://127.0.0.1:5000/lights/setLevel/100')

    def postProblem(self):
        print(f"{Fore.WHITE}{Back.MAGENTA}[postProblem() - 실행됨] : 고민 내용을 모아서 서버에 업로드를 시도합니다.")
        self.myProblemTitle =  self.ui.problemTitleTextEdit.toPlainText()
        self.myProblemTime = datetime.now(pytz.timezone('Asia/Seoul')).strftime(r'%Y-%m-%d %H:%M:%S')
        self.myProblemContent = self.ui.problemContentTextEdit.toPlainText()
        
        print(f'{Fore.WHITE}{Back.BLUE}[postProblem() - GUI에서 받아온 전달인자들 확인] :\n    {type(self.myProblemTitle)} | {self.myProblemTitle}\n    {type(self.myProblemTime)} | {self.myProblemTime}\n    {type(self.myProblemContent)} | {self.myProblemContent}')
        res = requests.post('http://127.0.0.1:5000/problems/',
            data={
                "problemTitle" : self.myProblemTitle,
                "problemAuthor" : self.userName,
                "problemTime" : self.myProblemTime,
                "problemContent" : self.myProblemContent
                })

        res_json = res.json()
        res_statusCode = int(res_json['StatusCode'])
        res_message = res_json['Message']
        self.myProblemId = res_json['ResultId']
        
        if res_statusCode == 400 :
            print(f'{Fore.GREEN}[postProblem() - 결과] : {res_message}')
            self.ui.consoleLabel.setText('고민을 서버에 성공적으로 업로드했습니다!')
        
        else:
            print(f'{Fore.RED}[postProblem() - 결과] : {res_message}')
            self.ui.consoleLabel.setText('고민을 서버에 업로드하는데 실패했습니다!')

                
    def backToPage1(self):
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage1() - 실행됨] : Page2 -> Page1으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(1)
    
    def requestProblems(self):
        """ 다른사람의 고민 목록을 10개 받아온다. """

        print(f'{Fore.BLACK}{Back.WHITE}[requestsProblems() - 실행됨]')
        res = requests.get('http://127.0.0.1:5000/problems/')
        res_json = res.json()
        
        if res_json['Counts'] == 1:
            random_id = 1
        
        elif res_json['Counts'] == 0:
            print(f"{Fore.RED}[requestProblems() - 응답 가공] : 서버에 고민이 없습니다!")
        
        else :
            random_id = random.randint(0, res_json["Counts"])

        problems_list = res_json["Problems"]
        
        print(f"{Fore.WHITE}{Back.BLUE}[requestsProblems() - 응답 데이터] : res_json")
        pprint(res_json)
        
        print(f"{Fore.WHITE}{Back.BLUE}[requestsProblems() - 응답 데이터] : problems_list")
        pprint(problems_list)

        self.otherProblemId = problems_list[random_id-1]["problemId"]
        print(f'[requestsProblems() - ID 확인]:\n    내 고민의 ID : {self.myProblemId}\n    ')
        self.requestOneProblem()
        
    def requestOneProblem(self):
        print(f'{Fore.BLACK}{Back.WHITE}[requestOneProblem() - 실행됨]')
        res = requests.get(f'http://127.0.0.1:5000/problems/{self.otherProblemId}/problem')
        res_json = res.json()
        pprint(res_json)
        
        _otherProblemTitle = res_json["problemTitle"]
        _otherProblemAuthor = res_json["problemAuthor"]
        _otherProblemTime = res_json["problemTime"]
        _otherProblemContent = res_json["problemContent"]

        self.ui.otherProblemTextBrower.setPlainText(f'제목 : {_otherProblemTitle}\nby {_otherProblemAuthor}, {_otherProblemTime}\n\n{_otherProblemContent}')
        
    
    def goToPage4(self):
        # 고민 리스트에서 고민 선택해서 다음으로 가기
        self.ui.stackedWidget.setCurrentIndex(4)

    def backToPage3(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def postReply(self):
        '''다른 사람의 고민에 대한 나의 답장을 서버에 업로드한다.'''
        
        print("[postReply()] : 답장 내용을 모아서 서버에 업로드를 시도합니다.")
        _replyTitle = self.ui.replyTitleTextEdit.toPlainText()
        _replyTime = datetime.now(pytz.timezone('Asia/Seoul')).strftime(r'%Y-%m-%d %H:%M:%S')
        _replyContent = self.ui.replyContentTextEdit.toPlainText()
        
        print(f'''[postReply() : GUI 입력화면에 적힌 내용들] :
            {type(_replyTitle)} | {_replyTitle}
            {type(_replyTime)} | {_replyTime}
            {type(_replyContent)} | {_replyContent}''')

        res = requests.post(f'http://127.0.0.1:5000/problems/{self.otherProblemId}/reply',
            data={
                "replyTitle" : _replyTitle,
                "replyAuthor" : self.userName,
                "replyTime" : _replyTime,
                "replyContent" : _replyContent
                })

        pprint(res.text)
        res_json = res.json()
        res_statusCode = int(res_json['StatusCode'])
        res_message = res_json['Message']
        print(f'[postReply()] : Post 요청에 대한 응답 - {res_statusCode}, {res_message}')
        
        if res_statusCode == 400 :
            self.ui.consoleLabel.setText('답장을 서버에 성공적으로 업로드했습니다!')
        
        else:
            print(f'{Fore.RED}[postProblem() ERROR MESSAGE] : {res_message}')
            self.ui.consoleLabel.setText('답장을 서버에 업로드하는데 실패했습니다!')

    
    def goToPage5(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.ui.sixthLabel2.setText(f'{self.userName}님의 답장도 곧 돌아올거에요... 편안히 기다려주세요')

        # 내 고민에 답장이 달렸는지 주기적으로 요청을 보내서 확인함.
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.requestNewReply)
        
    def requestNewReply(self, f_problemId):
        '''
        내가 보낸 고민에 답장이 달렸는지를 웹사이트에 요청해서 체크해주는 함수.
        '''
        
        res = requests.get(f'http://127.0.0.1:5000/problems/{self.myProblemId}/replys')
        res_json = res.json()
        reply_list = res_json['Replys']

        self.replyId = reply_list[0]['replyId']
        self.replyTitle = reply_list[0]['replyTItle']
        self.replyAuthor = reply_list[0]['replyAuthor']
        self.replyTime = reply_list[0]['replyTime']
        self.replyContent = reply_list[0]['replyContent']


        if res_json['Counts'] == 1:
            print(f'[requestNewReply()] : 새로운 답장이 달렸습니다!')
            self.timer.stop()
            pprint(reply_list[0])
        self.goToPage6()

    def goToPage6(self):
        self.ui.myProblemTextBrowser.setPlainText(f'제목 : {self.myProblemTitle}\nby {self.userName}, {self.myProblemTime}\n\n{self.myProblemContent}')
        self.ui.otherReplyTextBrowser.setPlainText(f'제목 : {self.replyId}\nby {self.replyAuthor}, {self.replyTime}\n\n{self.replyContent}')

        self.ui.stackedWidget.setCurrentIndex(6)
        

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MainWindow() 
    myWindow.show()
    app.exec_()