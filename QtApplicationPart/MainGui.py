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
import RPi.GPIO as GPIO

# 필요한 클래스 임포트
# MainGui.py를 직접 실행하면 ui_main 모듈안에 있는 클래스를 임포트 시켜야 함
# main.py를 실행하면 QtApplicationPart 패키지로 접근해 ui_main 모듈안에 있는 클래스를 임포트 시켜야 함 
if __name__ == '__main__':  from ui_main import Ui_MainWindow
else : from QtApplicationPart.ui_main import Ui_MainWindow

if __name__ == '__main__':  import requestFunc
else : from QtApplicationPart import requestFunc

init(autoreset=True)

# GPIO 제어를 위한 설정
LED = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

class MainWindow(QtWidgets.QMainWindow) :
    def __init__(self) :
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("너의 이름은")

        # 내가 쓴 고민 정보
        self.problemDictAboutMe = {}
        # 내가 쓴 고민에 대한 답장 정보 (타인이 씀)
        self.replyDictAboutMe = {}
        # 타인이 쓴 고민 정보
        self.problemDictAboutOther = {}
        # 타인이 쓴 고민에 대한 답장 정보 (내가 씀)
        self.replyDictAboutOther = {}

        self.ui.stackedWidget.setCurrentIndex(0)

        # 내 고민에 답장이 왔는지 확인하는 함수를 주기적으로 실행할 타이머객체
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(8000)
        self.timer.timeout.connect(lambda : self.checkNewReply(self.problemDictAboutMe['problemId']))

        # 0번(메인화면) 페이지 함수들
        self.ui.goToPage1Btn.clicked.connect(self.goToPage1)

        # 1번(내 이름 입력) 페이지 함수들
        self.ui.goToPage2Btn.clicked.connect(self.goToPage2)
        
        # 2번(내 고민 입력) 페이지 함수들
        self.ui.backToPage1Btn.clicked.connect(self.backToPage1)
        self.ui.postProblemBtn.clicked.connect(self.onPostProblemBtnClicked)

        # 3번(타인 고민 선택) 페이지 함수들
        # self.ui.goToPage4Btn.clicked.connect()
        
        # 4번(타인고민에답장보내기) 페이지 함수들
        self.ui.backToPage3Btn.clicked.connect(self.backToPage3)
        self.ui.postReplyBtn.clicked.connect(self.onPostReplyBtnClicked)

        # 5번(대기화면) 페이지 함수들
  

    #### 0번 페이지 (메인 화면) UI 함수들 ####
    def goToPage1(self):
        ''' 0번 페이지 (메인 화면) -> 1번 페이지 (이름 입력)'''
        print(f"{Fore.BLACK}{Back.WHITE}[goToPage1() - 실행됨] : Page0 -> Page1으로 이동합니다.")
        self.ui.stackedWidget.setCurrentIndex(1)

    
    #### 1번 페이지 (이름 입력) UI 함수들 ####
    def goToPage2(self):
        ''' 1번 페이지 (이름 입력) -> 2번 페이지 (내 고민 입력) '''

        _userName = self.ui.nameLineEdit.text()
        if _userName == '': 
            print(f"{Fore.YELLOW}[goToPage2() - 경고] : 이름이 입력되지 않았습니다!")
            self.ui.nameLabel.setText('불리고 싶은 이름을 입력해주세요!')
        else:
            print(f"{Fore.BLACK}{Back.WHITE}[goToPage2() - 실행됨] : Page1 -> Page2으로 이동합니다.")
            self.ui.stackedWidget.setCurrentIndex(2)
            self.problemDictAboutMe['problemAuthor'] = _userName
            self.replyDictAboutOther['replyAuthor'] = _userName
            # 입력받은 이름으로 5번 페이지에 fifthLabel2 텍스트를 세팅함
            self.ui.fifthLabel2.setText(f'{_userName}님의 답장도 곧 돌아올거에요... 편안히 기다려주세요')
            
            print(f'{Fore.BLACK}{Back.CYAN}[goToPage2()] : LED를 켭니다.')
            GPIO.output(LED, GPIO.HIGH)
            
    
    #### 2번 페이지 (내 고민 입력) UI 함수들 ####
    def backToPage1(self) -> None:
        ''' 2번 페이지 (내 고민 입력) -> 1번 페이지 (이름 입력)'''
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage1() - 실행됨] : Page2 -> Page1으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(1)
        
        print(f'{Fore.BLACK}{Back.CYAN}[goToPage2()] : Turn Off LED')
        GPIO.output(LED, GPIO.LOW)
        return

    def onPostProblemBtnClicked(self) -> None:
        # 입력된 고민 정보를 저장함
        self.problemDictAboutMe['problemTitle'] = self.ui.problemTitleTextEdit.toPlainText()
        self.problemDictAboutMe['problemTime'] = datetime.now(pytz.timezone('Asia/Seoul')).strftime(r'%Y-%m-%d %H:%M:%S')
        self.problemDictAboutMe['problemContent'] = self.ui.problemContentTextEdit.toPlainText()
        print(f'{Fore.WHITE}{Back.BLUE}[서버로 고민 올리기 - GUI에서 받아온 전달인자들 확인] :')
        print(f'    {type(self.problemDictAboutMe["problemTitle"])} | {self.problemDictAboutMe["problemTitle"]}')
        print(f'    {type(self.problemDictAboutMe["problemAuthor"])} | {self.problemDictAboutMe["problemAuthor"]}')
        print(f'    {type(self.problemDictAboutMe["problemTime"])} | {self.problemDictAboutMe["problemTime"]}')
        print(f'    {type(self.problemDictAboutMe["problemContent"] )} | {self.problemDictAboutMe["problemContent"] }')
        
        # 고민 정보를 서버에 올려 응답객체를 받아옴
        resDict_postProblem = requestFunc.postProblem(
            self.problemDictAboutMe['problemTitle'],
            self.problemDictAboutMe['problemAuthor'],
            self.problemDictAboutMe['problemTime'],
            self.problemDictAboutMe['problemContent'])
        
        # 받아온 응답객체에 담긴 나의 고민 ID를 저장하고 결과를 표시함.
        if int(resDict_postProblem['StatusCode']) == 400 :
            self.ui.consoleLabel.setText('고민을 서버에 성공적으로 업로드했습니다!')
            self.problemDictAboutMe['problemId'] = resDict_postProblem['ResultId']
            print(f"{Fore.WHITE}{Back.BLUE}[서버로 고민 올리기 - 나의 고민ID 확인] :\n")
            print(f"    self.problemDictAboutMe['problemId'] | {self.problemDictAboutMe['problemId']}")
            
        else :
            self.ui.consoleLabel.setText('고민을 서버에 업로드하는데 실패했습니다!')
            self.problemDictAboutMe['problemId'] = -1
            return
        
        # 타인의 고민이 여러개 담긴 응답 객체를 받아옴
        resDict_requestProblems = requestFunc.requestProblems()

        # 받아온 타인의 고민이 없으면 리턴함
        if resDict_requestProblems['Counts'] == 0:
            print(f"{Fore.RED}{Style.BRIGHT}[타인의 고민 여러개 받기] : 서버에 고민이 없습니다!")
            return
        
        #  타인의 고민중 랜덤으로 하나의 ID를 선택함
        problems_list = resDict_requestProblems["Problems"]
        other_problem_ids = []
        for problem in problems_list:
            other_problem_ids.append(problem['problemId'])
        self.problemDictAboutOther['problemId'] = other_problem_ids[random.randint(0, len(other_problem_ids)-1)]
        print(f'{Fore.WHITE}{Back.BLUE}[타인의 고민 여러개 받기 - 타인의 고민 ID 확인]:')
        print(f"    {Fore.WHITE}{Back.BLUE}self.otherProblemId['problemId'] | {self.problemDictAboutOther['problemId']}")
        
        # 고른 타인의 고민 ID로 고민 상세정보를 요청해 응답객체를 받음
        resDict_requestOneProblem = requestFunc.requestOneProblem(self.problemDictAboutOther['problemId'])
        # 응답 객체 속 타인의 고민 상세정보를 저장함
        self.problemDictAboutOther = resDict_requestOneProblem['ProblemData']

        # updatePage5 : 4번 페이지 (타인 고민 답장) 타인 고민을 표시함
        resultOtherProblemText = (
            f"제목 : {self.problemDictAboutOther['problemTitle']}\n"
            f"by {self.problemDictAboutOther['problemAuthor']}, {self.problemDictAboutOther['problemTime']}\n"
            "\n"
            f"{self.problemDictAboutOther['problemContent']}"
        )
        self.ui.otherProblemTextBrower.setPlainText(resultOtherProblemText)

        # 페이지 전환
        self.ui.stackedWidget.setCurrentIndex(4)

    #### 3번 페이지 (타인 고민 선택) UI 함수들 ####
    # [리스트뷰 마지막에 도달했을 때] 
        # TODO fetchMore(): 화면 내리면 데이터 더 요청해 모델에 fetch 시키기
    
    # [4번 페이지 (타인 고민 답장) 페이지로 넘어갈 때]
        # TODO requestOneProblem(): 선택된 고민의 상세정보 요청해 저장하기 
        # TODO updatePage4() : 타인 고민 답장 UI 정보 업데이트시키기
        # goToPage4() : 4번 페이지 (타인 고민 답장) 로 페이지 전환하기
    
    def goToPage4(self):
        ''' 3번 페이지 (타인 고민 선택) -> 4번 페이지 (타인 고민 답장)'''
        print(f'{Fore.BLACK}{Back.WHITE}[goToPage4() - 실행됨] : Page3 (타인 고민 선택) -> Page4 (타인 고민 답장) 으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(4)

    
    
    #### 4번 페이지 (타인 고민 답장)  UI 함수들 ####
    # [3번 페이지 (타인 고민 선택) 페이지로 넘어갈 때]
        # backToPage3() : 3번 페이지로 넘어가기
    # [5번 페이지 (대기화면) 페이지로 넘어갈 때]
        # postReply() : 입력된 답장 정보 서버로 올리기
        # timer.start(): 타이머 실행시키기
        # goToPage5() : 5번 페이지로 넘어가기
    def backToPage3(self):
        ''' 4번 페이지 (타인 고민 답장) -> 3번 페이지 (타인 고민 선택)'''
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage3() - 실행됨] : Page4 (타인 고민 답장) -> Page3 (타인 고민 선택) 으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def onPostReplyBtnClicked(self):
        ''' 입력된 답장 정보 서버로 올림 => 타이머 실행시킴'''
        # 타인의 고민에 대한 답장 정보를 수집함 (내가 씀)
        self.replyDictAboutOther['problemId'] = self.problemDictAboutOther['problemId']
        self.replyDictAboutOther['replyTitle'] = self.ui.replyTitleTextEdit.toPlainText()
        self.replyDictAboutOther['replyAuthor'] = self.problemDictAboutMe['problemAuthor']
        self.replyDictAboutOther['replyTime'] = datetime.now(pytz.timezone('Asia/Seoul')).strftime(r'%Y-%m-%d %H:%M:%S')
        self.replyDictAboutOther['replyContent'] = self.ui.replyContentTextEdit.toPlainText()
        
        # 수집한 답장 정보를 콘솔에서 확인
        print(f"{Fore.WHITE}{Back.BLUE}[서버로 답장 올리기 - GUI에서 받아온 전달인자들 확인] :")
        print(f"    self.replyDictAboutOther['problemId'] | {self.replyDictAboutOther['problemId']}")
        print(f"    self.replyDictAboutOther['replyTitle'] | {self.replyDictAboutOther['replyTitle']}")
        print(f"    self.replyDictAboutOther['replyTime'] | {self.replyDictAboutOther['replyTime']}")
        print(f"    self.replyDictAboutOther['replyAuthor'] | {self.replyDictAboutOther['replyAuthor']}")
        print(f"    self.replyDictAboutOther['replyContent'] | {self.replyDictAboutOther['replyContent'] }")
    
        # 서버로 답장 정보를 올림
        resDict_postReply = requestFunc.postReply(
            f_problemId = self.replyDictAboutOther['problemId'],
            f_title = self.replyDictAboutOther['replyTitle'],
            f_author = self.replyDictAboutOther['replyAuthor'],
            f_time = self.replyDictAboutOther['replyTime'],
            f_content = self.replyDictAboutOther['replyContent'],
            )
        if int(resDict_postReply['StatusCode']) == 400:
            self.ui.consoleLabel.setText('답장을 서버에 성공적으로 업로드했습니다!')
        else : 
            self.ui.consoleLabel.setText("답장을 서버에 업로드하는데 실패했습니다!")

        # 타이머를 실행시킴
        self.timer.start()

        # 5번 페이지로 넘어감
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage3() - 실행됨] : Page4 (타인 고민 답장) -> Page5 (대기화면) 으로 이동합니다.')
        self.ui.stackedWidget.setCurrentIndex(5)
    
    #### 5번 페이지 (대기화면) UI 함수 ####
    def checkNewReply(self, f_problemId):
        ''' 내가 보낸 고민에 답장이 달렸는지를 웹사이트에 요청해서 체크해주는 함수. '''
        print("[checkNewReply() - 실행됨]")

        res = requests.get(f'http://127.0.0.1:5000/problems/{f_problemId}/reply')
        res_json = res.json()

        if res_json['Counts'] >= 1:
            print(f'{Fore.WHITE}{Back.GREEN}[checkNewReply()] : 새로운 답장이 달렸습니다!')
            print('[checkNewReply()] : 타이머를 정지합니다.')
            self.timer.stop()
            
            if res_json['Counts'] == 1:
                self.replyDictAboutMe['replyId'] = res_json['Replys'][0]['replyId']
                resDict_requestOneReply = requestFunc.requestOneReply(
                    f_problemId = f_problemId,
                    f_replyId = self.replyDictAboutMe['replyId']
                )

                # 받아온 나의 고민에 대한 답장 정보를 저장함
                replyData = resDict_requestOneReply['ReplyData']
                self.replyDictAboutMe['problemId'] = self.problemDictAboutMe['problemId']
                self.replyDictAboutMe['replyTitle'] = replyData['replyTitle']
                self.replyDictAboutMe['replyAuthor'] = replyData['replyAuthor']
                self.replyDictAboutMe['replyTime'] = replyData['replyTime']
                self.replyDictAboutMe['replyContent'] = replyData['replyContent']

                # 받아온 나의 고민에 대한 답장 정보를 콘솔에서 확인함
                print(f"{Fore.WHITE}{Back.BLUE}[checkNewReply() - 내 고민의 답장 정보 확인]:")
                print(f"    self.replyDictAboutMe['replyId'] : {self.replyDictAboutMe['replyId']}")
                print(f"    self.replyDictAboutMe['problemId'] : {self.replyDictAboutMe['problemId']}")
                print(f"    self.replyDictAboutMe['replyTitle'] : {self.replyDictAboutMe['replyTitle']}")
                print(f"    self.replyDictAboutMe['replyAuthor'] : {self.replyDictAboutMe['replyAuthor']}")
                print(f"    self.replyDictAboutMe['replyTime'] : {self.replyDictAboutMe['replyTime']}")
                print(f"    self.replyDictAboutMe['replyContent'] : {self.replyDictAboutMe['replyContent']}")
                self.goToPage6()
                return

            else :
                # TODO : 답장 선택하는 화면 구현해 replyId 고르도록 하기
                pass
            
            return

        else :
            return

    def goToPage6(self):
        ''' 5번 페이지 (대기화면) -> 6번 페이지 (내 답장화면)
            저장된 나의 고민에 대한 답장 데이터를 화면에 업데이트 시키고 전환함'''
        
        print(f'{Fore.BLACK}{Back.WHITE}[backToPage3() - 실행됨] : Page5 (대기화면) -> Page6 (내 답장화면) 으로 이동합니다.')
        # 나의 고민이 뜰 부분에 텍스트를 만들어서 채움
        resultMyProblemText = (
            f"제목 : {self.problemDictAboutMe['problemTitle']}\n"
            f"by {self.problemDictAboutMe['problemAuthor']}, {self.problemDictAboutMe['problemTime']}\n"
            "\n"
            f"{self.problemDictAboutMe['problemContent']}"
        )
        self.ui.myProblemTextBrowser.setPlainText(resultMyProblemText)
        
        # 내 고민에 대한 답장이 뜰 부분에 텍스트를 만들어서 채움
        resultMyReplyText = (
            f"제목 : {self.replyDictAboutMe['replyTitle']}\n"
            f"by {self.replyDictAboutMe['replyAuthor']}, {self.replyDictAboutMe['replyTime']}\n"
            "\n"
            f"{self.replyDictAboutMe['replyContent']}"
        )
        self.ui.otherReplyTextBrowser.setPlainText(resultMyReplyText)

        self.ui.stackedWidget.setCurrentIndex(6)
        

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MainWindow() 
    myWindow.show()
    app.exec_()
    GPIO.cleanup()