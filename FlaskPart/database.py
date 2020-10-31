import pymysql
import datetime
import pytz

def create_table() -> None:
    """ PROBLEMS 테이블과 REPLYS 테이블을 생성한다. """

    db = pymysql.connect(host='localhost', user='Admin_Your_Problem', password='admin1234', db='Your_Problem', charset='utf8')
    cur = db.cursor()
    cur.execute( '''
        CREATE TABLE IF NOT EXISTS PROBLEMS( 
            problemId INT PRIMARY KEY AUTO_INCREMENT,
            problemTitle TEXT NOT NULL,
            problemAuthor TEXT NOT NULL,
            problemTime VARCHAR(19),
            problemContent TEXT NOT NULL
        )'''
    )

    # REPLYS 테이블 생성하기
    cur.execute('''
        CREATE TABLE IF NOT EXISTS REPLYS(
            replyId INT PRIMARY KEY AUTO_INCREMENT,
            problemId INT NOT NULL,
            replyTitle TEXT NOT NULL,
            replyAuthor TEXT NOT NULL,
            replyTime VARCHAR(19),
            replyContent TEXT NOT NULL,
            FOREIGN KEY(problemId) REFERENCES PROBLEMS(problemId)
        )'''
    ) 

    #위에서 실행한 명령어를 DB에 적용시키기
    db.commit()

def get_problems_list() -> list:
    """ PROBLEMS 테이블에서 최신순으로 고민 10개의 모든 정보를 반환한다. """
    
    db = pymysql.connect(host='localhost', user='Admin_Your_Problem', password='admin1234', db='Your_Problem', charset='utf8')
    cur = db.cursor()
    try :
        print('[database.py] : get_problems_list() 실행됨')
        cur = db.cursor()
        cur.execute("SELECT * FROM PROBLEMS ORDER BY problemTime")
        result = cur.fetchmany(10)
        return result

    except Exception as e:
        raise e

def get_problem(f_problemId:int) -> tuple:
    """ problemId == f_problemId 인 고민의 모든 정보를 반환한다. """

    db = pymysql.connect(host='localhost', user='Admin_Your_Problem', password='admin1234', db='Your_Problem', charset='utf8')
    cur = db.cursor()
    try : 
        print(f'[database.py] : get_problem({f_problemId}, {type(f_problemId)}) 실행됨')
        cur = db.cursor()
        cur.execute("SELECT * FROM PROBLEMS WHERE problemId = %s", (f_problemId))
        result = cur.fetchone()
        return result

    except Exception as e:
        raise e

def insert_problem(f_title, f_author, f_time, f_content) -> int:
    print(f'{Fore.BLUE}[database.py | insert_problem()]')
    db = pymysql.connect(host='localhost', user='Admin_Your_Problem', password='admin1234', db='Your_Problem', charset='utf8')
    cur = db.cursor()
    try :
        cur = db.cursor()
        cur.execute("INSERT INTO PROBLEMS (problemTitle, problemAuthor, problemTime, problemContent) VALUES (%s, %s, %s, %s)", (f_title, f_author, f_time, f_content))  #DB에 데이터 넣는 부분
        cur.execute('SELECT problemId FROM PROBLEMS WHERE problemTitle = %s AND problemAuthor = %s, problemContent = %s ORDER BY problemTime', (f_title, f_author, f_content))
        resultId = cur.fetchOne()[0]
        print("[database.py] : Inserted Label's problemId : {resultId}")
        db.commit()
        
        return resultId
    
    except Exception as e:
        raise e

def get_replys_list(f_id) -> list:
    """ REPLY 테이블에서 problemId == f_id 인 고민에 대한 최신 응답 10개의 간략한 정보들을 반환한다. """
    
    db = pymysql.connect(host='localhost', user='Admin_Your_Problem', password='admin1234', db='Your_Problem', charset='utf8')
    cur = db.cursor()
    try :
        print('[database.py] : get_replys_list() 실행됨')
        cur = db.cursor()
        cur.execute("SELECT * FROM REPLYS WHERE problemId = %s ORDER BY replyTime", (f_id,))
        result = cur.fetchmany(10)
        return result

    except Exception as e:
        raise e

def get_reply(f_replyId:int) -> tuple:
    """ replyId == f_replyId 인 고민의 모든 정보를 반환한다. """

    db = pymysql.connect(host='localhost', user='Admin_Your_Problem', password='admin1234', db='Your_Problem', charset='utf8')
    cur = db.cursor()
    try : 
        print(f'[database.py] : get_reply({f_replyId}, {type(f_replyId)}) 실행됨')
        cur = db.cursor()
        cur.execute("SELECT * FROM REPLYS WHERE replyId = %s", (f_replyId, ))
        result = cur.fetchone()
        return result

    except Exception as e:
        raise e

def insert_reply(f_problemId, f_title, f_author, f_time, f_content):
    
    db = pymysql.connect(host='localhost', user='Admin_Your_Problem', password='admin1234', db='Your_Problem', charset='utf8')
    cur = db.cursor()
    try :
        cur = db.cursor()
        cur.execute("INSERT INTO REPLYS (problemId, replyTitle, replyAuthor, replyTime, replyContent) VALUES (%s, %s, %s, %s, %s)", (f_problemId, f_title, f_author, f_time, f_content))
        db.commit()
    except Exception as e:
        raise e