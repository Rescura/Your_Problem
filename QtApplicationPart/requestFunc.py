from colorama import init, Fore, Back, Style
from pprint import pprint
import requests

init(autoreset=True)

def postProblem(f_title, f_author, f_time, f_content) -> dict:
        ''' 내가 적은 나의 고민을 서버에 올린다. 응답객체를 dict형으로 반환한다.'''
        
        print(f"{Fore.BLACK}{Back.WHITE}[postProblem() - 실행됨]")
        
        print(f"{Fore.BLACK}{Back.MAGENTA}[postProblem() - 서버에 고민 업로드] : 서버에 업로드를 시도합니다.")
        res = requests.post('http://127.0.0.1:5000/problems/',
            data={
                "problemTitle" : f_title,
                "problemAuthor" : f_author,
                "problemTime" : f_time,
                "problemContent" : f_content
                })
        res_json = res.json()
        res_statusCode = int(res_json['StatusCode'])
        res_message = res_json['Message']

        if res_statusCode == 400 :
            print(f'{Fore.GREEN}{Back.MAGENTA}{Style.DIM}[postProblem() - 서버 응답]')
        else:
            print(f'{Fore.RED}{Back.MAGENTA}{Style.DIM}[postProblem() - 서버 응답]')
        print(f'    StatusCode : {res_statusCode}')
        print(f'    Message : {res_message}')

        print(f"{Fore.BLACK}{Back.WHITE}[postProblem() - 종료됨]")
        return res_json
        
def requestProblems() -> dict:
        ''' 서버에 존재하는 다른 사람의 고민들을 요청해 그중 하나의 ID를 저장한다.
            postProblemBtn.clicked -> requestProblems() '''

        print(f'{Fore.BLACK}{Back.WHITE}[requestProblems() - 실행됨]')
        print(f"{Fore.BLACK}{Back.MAGENTA}[requestProblems() - 서버에 타인 고민 여러개 요청] : 타인의 고민 여러개를 서버에 요청합니다.")
        res = requests.get('http://127.0.0.1:5000/problems/')
        res_json = res.json()
        res_statusCode = int(res_json['StatusCode'])
        res_message = res_json['Message']

        if res_statusCode == 400 :
            print(f'{Fore.GREEN}{Back.MAGENTA}{Style.DIM}[requestProblems() - 서버 응답]')
        else:
            print(f'{Fore.RED}{Back.MAGENTA}{Style.DIM}[requestProblems() - 서버 응답]')
        print(f'    StatusCode : {res_statusCode}')
        print(f'    Message : {res_message}')

        print(f"{Fore.BLACK}{Back.WHITE}[requestProblems() - 종료됨]")
        return res_json

def requestOneProblem(f_id) -> dict:
        ''' problemId == f_id 인 고민의 상세정보를 서버에서 받아와 응답객체를 반환한다.
            requestProblems() -> requestOneProblem()'''
        
        print(f'{Fore.BLACK}{Back.WHITE}[requestOneProblem() - 실행됨]')
        
        print(f"{Fore.BLACK}{Back.MAGENTA}[requestOneProblem() - 타인의 고민 상세정보 요청] : problemId = {f_id}인 고민의 상세정보를 서버에 요청합니다.")
        res = requests.get(f'http://127.0.0.1:5000/problems/{f_id}/problem')
        res_json = res.json()
        res_statusCode = res_json['StatusCode']
        res_message = res_json['Message']
        
        if res_statusCode == 400 :
            print(f'{Fore.GREEN}{Back.MAGENTA}{Style.DIM}[requestOneProblem() - 서버 응답]')
        else:
            print(f'{Fore.RED}{Back.MAGENTA}{Style.DIM}[requestOneProblem() - 서버 응답]')
        print(f'    StatusCode : {res_statusCode}')
        print(f'    Message : {res_message}')

        print(f"{Fore.BLACK}{Back.WHITE}[requestOneProblem() - 종료됨]")
        return res_json

def postReply(f_problemId, f_title, f_author, f_time, f_content) -> dict:
        ''' 내가 적은 타인의 고민 답장을 서버에 올린다. 응답객체를 dict형으로 반환한다.'''
        
        print(f"{Fore.BLACK}{Back.WHITE}[postReply() - 실행됨]")
        
        print(f"{Fore.BLACK}{Back.MAGENTA}[postReply() - 서버에 답장 업로드] : 서버에 업로드를 시도합니다.")
        res = requests.post(f"http://127.0.0.1:5000/problems/{f_problemId}/reply",
            data={
                "replyTitle" : f_title,
                "replyAuthor" : f_author,
                "replyTime" : f_time,
                "replyContent" : f_content
                })
        res_json = res.json()
        res_statusCode = int(res_json['StatusCode'])
        res_message = res_json['Message']

        if res_statusCode == 400 :
            print(f'{Fore.GREEN}{Back.MAGENTA}{Style.DIM}[postProblem() - 서버 응답]')
        else:
            print(f'{Fore.RED}{Back.MAGENTA}{Style.DIM}[postProblem() - 서버 응답]')
        print(f'    StatusCode : {res_statusCode}')
        print(f'    Message : {res_message}')

        print(f"{Fore.BLACK}{Back.WHITE}[postProblem() - 종료됨]")
        return res_json

def requestOneReply(f_problemId, f_replyId) -> dict:
        ''' replyId == f_replyId 인 답장의 상세정보를 요청한 후 응답객체를 dict형으로 반환한다. '''
        print(f'{Fore.BLACK}{Back.WHITE}[requestOneReply() - 실행됨]:')

        print(f"{Fore.BLACK}{Back.MAGENTA}[requestOneReply() - 내 고민의 답장 상세정보 요청] : replyId = {f_replyId}인 고민의 상세정보를 서버에 요청합니다.")
        res = requests.get(f'http://127.0.0.1:5000/problems/{f_problemId}/reply/{f_replyId}')
        res_json = res.json()
        res_statusCode = res_json['StatusCode']
        res_message = res_json['Message']

        if res_statusCode == 400 :
            print(f'{Fore.GREEN}{Back.MAGENTA}{Style.BRIGHT}[requestOneReply() - 서버 응답]')
        else:
            print(f'{Fore.RED}{Back.MAGENTA}{Style.BRIGHT}[requestOneReply() - 서버 응답]')
        print(f'    StatusCode : {res_statusCode}')
        print(f'    Message : {res_message}')

        print(f"{Fore.BLACK}{Back.WHITE}[requestOneReply() - 종료됨]")

        return res_json
        
# TODO : 함수를 get, post로 나누어 간추릴것