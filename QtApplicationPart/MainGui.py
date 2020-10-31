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
from colorama import init, Fore, Back, Style


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

        # 내 고민에 답장이 왔는지 확인하는 함수를 주기적으로 실행할 타이머객체
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.requestNewReply)

        # 0번(메인화면) 페이지 함수들
        self.ui.goToPage1Btn.clicked.connect(self.goToPage1)

        # 1번(내 이름 입력) 페이지 함수들
        self.ui.goToPage2Btn.clicked.connect(self.goToPage2)
        
        # 2번(내 고민 입력) 페이지 함수들
        self.ui.backToPage1Btn.clicked.connect(self.backToPage1)
        self.ui.postProblemBtn.clicked.connect(self.onPostProblemBtnClicked)
        self.ui.postProblemBtn.clicked.connect(self.postProblem) # 나의 고민을 포스트함
        self.ui.postProblemBtn.clicked.connect(self.requestProblems) # 다른 사람의 고민들을 요청해서 받아옴
        self.ui.postProblemBtn.clicked.connect(lambda : self.ui.stackedWidget.setCurrentIndex(4)) # 4번 페이지로 이동

        # 3번(타인 고민 선택) 페이지 함수들
        # self.ui.goToPage4Btn.clicked.connect()
        
        # 4번(타인고민에답장보내기) 페이지 함수들
        self.ui.backToPage3Btn.clicked.connect(self.backToPage3)
        self.ui.postReplyBtn.clicked.connect(self.postReply)
        self.ui.postReplyBtn.clicked.connect(self.goToPage6)

        # 5번(대기화면) 페이지 함수들
  

    #### 0번 페이지 (메인 화면) UI 함수들 ####
    def goToPage1(self):
        ''' 0번 페이지 (메인 화면) -> 1번 페이지 (이름 입력)'''
        print(f"{Fore.BLACK}{Back.WHITE}[goToPage1() - 실행됨] : Page0 -> Page1으로 이동합니다.")
        self.ui.stackedWidget.setCurrentIndex(1)

    
    #### 1번 페이지 (이름 입력) UI 함수들 ####
    def goToPage2(self):
        ''' 1번 페이지 (이름 입력) -> 2번 페이지 (내 고민 입력) '''

        self.userName = self.ui.nameLineEdit.text()
        if self.userName == '': 
            print(f"{Fore.YELLOW}[goToPage2() - 경고] : 이름이 입력되지 않았습니다!")
            self.ui.nameLabel.setText('불리고 싶은 이름을 입력해주세요!')
        else:
            print(f"{Fore.BLACK}{Back.WHITE}[goToPage2() - 실행됨] : Page1 -> Page2으로 이동합니다.")
            self.ui.stackedWidget.setCurrentIndex(2)
            self.ui.fifthLabel2.setText(f'{self.userName}님의 답장도 곧 돌아올거에요... 편안히 기다려주세요')

            
            # TODO : 로컬에서 전구 불빛 조정하기
            # requests.get('http://127.0.0.1:5000/lights/setLevel/100')
    
    #### 2번 페이지 (내 고민 입력) UI 함수들 ####
    def backToPage1(self) -> None:
        ''' 2번 페이지 (내 고민 입력) -> 1번 페이지 (이름 입력)'''
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage1() - 실행됨] : Page2 -> Page1으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(1)
        return

    def postProblem(self) -> None:
        ''' 내가 적은 나의 고민을 서버에 올린다.
            postProblemBtn.clicked -> postProblem()'''
        
        print(f"{Fore.BLACK}{Back.WHITE}[postProblem() - 실행됨]")

        self.myProblemTitle =  self.ui.problemTitleTextEdit.toPlainText()
        self.myProblemTime = datetime.now(pytz.timezone('Asia/Seoul')).strftime(r'%Y-%m-%d %H:%M:%S')
        self.myProblemContent = self.ui.problemContentTextEdit.toPlainText()
        print(f'{Fore.WHITE}{Back.BLUE}[postProblem() - GUI에서 받아온 전달인자들 확인] :')
        print(f'    {type(self.myProblemTitle)} | {self.myProblemTitle}')
        print(f'    {type(self.myProblemTime)} | {self.myProblemTime}')
        print(f'    {type(self.myProblemContent)} | {self.myProblemContent}')
        
        print(f"{Fore.WHITE}{Back.MAGENTA}[postProblem() - 서버에 고민 업로드] : 고민 내용을 모아서 서버에 업로드를 시도합니다.")
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
            print(f'{Fore.GREEN}{Back.MAGENTA}{Style.BRIGHT}[postProblem() - 서버 응답]')
            print(f'    StatusCode : {res_statusCode}')
            print(f'    Message : {res_message}')
            print(f'{Fore.WHITE}{Back.BLUE}[postProblem() - 내 고민 ID 확인] : \n    {self.myProblemId}')
            self.ui.consoleLabel.setText('고민을 서버에 성공적으로 업로드했습니다!')
        
        else:
            print(f'{Fore.RED}{Back.MAGENTA}{Style.BRIGHT}[postProblem() - 서버 응답]')
            print(f'    StatusCode : {res_statusCode}')
            print(f'    Message : {res_message}')
            self.ui.consoleLabel.setText('고민을 서버에 업로드하는데 실패했습니다!')

        print(f"{Fore.BLACK}{Back.WHITE}[postProblem() - 종료됨]")
        return
        
    def requestProblems(self):
        ''' 서버에 존재하는 다른 사람의 고민들을 요청해 그중 하나의 ID를 저장한다.
            postProblemBtn.clicked -> requestProblems() '''

        print(f'{Fore.BLACK}{Back.WHITE}[requestProblems() - 실행됨]')
        print(f"{Fore.WHITE}{Back.MAGENTA}[requestProblems() - 서버에 타인 고민 여러개 요청] : 타인의 고민 여러개를 서버에 요청합니다.")
        res = requests.get('http://127.0.0.1:5000/problems/')
        res_json = res.json()
        
        if res_json['Counts'] == 0:
            # 받아온 타인 고민이 없다면 그냥 리턴함
            print(f"{Fore.RED}{Back.MAGENTA}{Style.BRIGHT}[requestProblems() - 응답 가공] : 서버에 고민이 없습니다!")
            return
        else :
            # 받아온 타인의 고민 ID중 랜덤으로 하나를 self.otherProblemId에 저장함
            problems_list = res_json["Problems"]
            other_problem_ids = []
            for problem in problems_list:
                other_problem_ids.append(problem['problemId'])
            
            self.otherProblemId = other_problem_ids[random.randint(0, len(other_problem_ids)-1)]
        
        print(f'{Fore.WHITE}{Back.BLUE}[requestProblems() - 타인의 고민 ID 확인]:')
        print(f'    self.otherProblemId : {self.otherProblemId}')

        # 받은 타인의 고민ID로 상세정보를 받아와 GUI를 업데이트시킴
        self.requestOneProblem()
        print(f'{Fore.BLACK}{Back.WHITE}[requestProblems() - 종료됨]')
        return

    def requestOneProblem(self):
        ''' 저장된 다른 사람의 고민 id에 따라 그 고민의 상세정보를 불러와 GUI를 업데이트 시킨다.
            requestProblems() -> requestOneProblem()'''
        
        print(f'{Fore.BLACK}{Back.WHITE}[requestOneProblem() - 실행됨]')
        
        print(f"{Fore.WHITE}{Back.MAGENTA}[requestOneProblem() - 타인의 고민 상세정보 요청] : problemId = {self.otherProblemId}인 고민의 상세정보를 서버에 요청합니다.")
        res = requests.get(f'http://127.0.0.1:5000/problems/{self.otherProblemId}/problem')
        res_json = res.json()
        res_statusCode = res_json['StatusCode']
        res_message = res_json['Message']
        res_problemData = res_json['ProblemData']
        
        if res_statusCode != 400: 
            print(f"{Fore.RED}{Back.MAGENTA}[requestOneProblem() - 타인의 고민 상세정보 요청] : 실패")
            print(f"{Fore.RED}{Back.MAGENTA}    res_StatusCode : {res_statusCode}")
            print(f"{Fore.RED}{Back.MAGENTA}    res_Message :{res_message}")
            return

        elif res_statusCode == 400: 
            print(f"{Fore.RED}{Back.MAGENTA}[requestOneProblem() - 타인의 고민 상세정보 요청] : 실패")
            print(f"{Fore.RED}{Back.MAGENTA}    res_StatusCode : {res_statusCode}")
            print(f"{Fore.RED}{Back.MAGENTA}    res_Message :{res_message}")

        _otherProblemTitle = res_problemData["problemTitle"]
        _otherProblemAuthor = res_problemData["problemAuthor"]
        _otherProblemTime = res_problemData["problemTime"]
        _otherProblemContent = res_problemData["problemContent"]

        print(f'{Fore.WHITE}{Back.BLUE}[requestProblems() - 타인의 고민 정보 확인]:')
        print(f'    self.otherProblemId : {self.otherProblemId}')
        print(f'    _otherProblemTitle : {_otherProblemAuthor}')
        print(f'    _otherProblemAuthor : {_otherProblemAuthor}')
        print(f'    _otherProblemTime : {_otherProblemTime}')
        print(f'    _otherProblemContent : {_otherProblemContent}')

        print(f'{Fore.BLACK}{Back.WHITE}[requestOneProblem() - UI 업데이트]')
        resultOtherProblemText = (
            f"제목 : {_otherProblemTitle}"
            f"by {_otherProblemAuthor}, {_otherProblemTime}"
            "\n"
            f"{_otherProblemContent}"
        )
        self.ui.otherProblemTextBrower.setPlainText(resultOtherProblemText)
        print(f'{Fore.BLACK}{Back.WHITE}[requestOneProblem() - 종료됨]')

    #### 3번 페이지 (타인 고민 선택) UI 함수들 ####
    def goToPage4(self):
        ''' 3번 페이지 (타인 고민 선택) -> 4번 페이지 (타인 고민 답장)'''
        print(f'{Fore.BLACK}{Back.WHITE}[goToPage4() - 실행됨] : Page3 (타인 고민 선택) -> Page4 (타인 고민 답장) 으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(4)

    #### 4번 페이지 (타인 고민 답장)  UI 함수들 ####
    def backToPage3(self):
        ''' 4번 페이지 (타인 고민 답장) -> 3번 페이지 (타인 고민 선택)'''
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage3() - 실행됨] : Page4 (타인 고민 답장) -> Page3 (타인 고민 선택) 으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(3)
        
    def goToPage5(self):
        ''' 4번 페이지 (타인 고민 답장) -> 5번 페이지 (대기화면)'''
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage3() - 실행됨] : Page4 (타인 고민 답장) -> Page5 (대기화면) 으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(5)

        
    def requestNewReply(self, f_problemId):
        ''' 내가 보낸 고민에 답장이 달렸는지를 웹사이트에 요청해서 체크해주는 함수. '''
        
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