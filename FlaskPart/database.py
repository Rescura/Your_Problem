import sqlite3


def create_table() -> None:
    """ PROBLEMS 테이블과 REPLYS 테이블을 생성한다. """
    conn = sqlite3.connect('your_problems.db')
    with conn:
        #DB 커서 객체 생성하기
        cur = conn.cursor() 

        # PROBLEMS 테이블 생성하기
        cur.execute( '''
            CREATE TABLE IF NOT EXISTS PROBLEMS( 
                problemId integer PRIMARY KEY AUTOINCREMENT,
                problemTitle text NOT NULL,
                problemAuthor text NOT NULL,
                problemTime timestamp,
                problemContent text NOT NULL
            )'''
        ) 

        # REPLYS 테이블 생성하기
        cur.execute('''
            CREATE TABLE IF NOT EXISTS REPLYS(
                replyId integer PRIMARY KEY AUTOINCREMENT,
                problemId integer NOT NULL,
                replyTitle text NOT NULL,
                replyAuthor text NOT NULL,
                replyTime timestamp,
                replyContent text NOT NULL,
                FOREIGN KEY(problemId) REFERENCES PROBLEMS(problemId)
            )'''
        ) 

        #위에서 실행한 명령어를 DB에 적용시키기
        conn.commit() 

def get_problems_list() -> list:
    """ PROBLEMS 테이블에서 최신순으로 고민 10개의 모든 정보를 반환한다. """
    conn = sqlite3.connect('your_problems.db')
    with conn:
        try :
            print('[database.py] : get_problems_list() 실행됨')
            cur = conn.cursor()
            cur.execute("SELECT * FROM PROBLEMS ORDER BY problemTime")
            result = cur.fetchmany(10)

            return result
        except Exception as e:
            raise e

def get_problem(f_problemId:int) -> tuple:
    """ problemId == f_problemId 인 고민의 모든 정보를 반환한다. """

    conn = sqlite3.connect('your_problems.db')
    with conn:
        try : 
            print(f'[database.py] : get_problem({f_problemId}, {type(f_problemId)}) 실행됨')
            cur = conn.cursor()
            result = cur.execute("SELECT * FROM PROBLEMS WHERE problemId == ?", (f_problemId, )).fetchone()

            return result
        except Exception as e:
            raise e

def insert_problem(f_title, f_author, f_time, f_content):
    conn = sqlite3.connect('your_problems.db')
    with conn:
        try :
            cur = conn.cursor()
            cur.execute("INSERT INTO PROBLEMS (problemTitle, problemAuthor, problemTime, problemContent) VALUES (?, ?, ?, ?)", (f_title, f_author, f_time, f_content))  #DB에 데이터 넣는 부분
            conn.commit()
        except Exception as e:
            raise e

def get_replys_list(f_id) -> list:
    """ REPLY 테이블에서 problemId == f_id 인 고민에 대한 최신 응답 10개의 간략한 정보들을 반환한다. """
    conn = sqlite3.connect('your_problems.db')
    with conn:
        try :
            print('[database.py] : get_replys_list() 실행됨')
            cur = conn.cursor()
            cur.execute("SELECT * FROM REPLYS WHERE problemId == ? ORDER BY replyTime", (f_id,))
            result = cur.fetchmany(10)

            return result
        except Exception as e:
            raise e

def get_reply(f_replyId:int) -> tuple:
    """ replyId == f_replyId 인 고민의 모든 정보를 반환한다. """

    conn = sqlite3.connect('your_problems.db')
    with conn:
        try : 
            print(f'[database.py] : get_reply({f_replyId}, {type(f_replyId)}) 실행됨')
            cur = conn.cursor()
            cur.execute("SELECT * FROM REPLYS WHERE replyId == ?", (f_replyId, ))
            result = cur.fetchone()
            return result
        except Exception as e:
            raise e

def insert_reply(f_problemId, f_title, f_author, f_time, f_content):
    conn = sqlite3.connect('your_problems.db')
    with conn:
        try :
            cur = conn.cursor()
            cur.execute("INSERT INTO REPLYS (problemId, replyTitle, replyAuthor, replyTime, replyContent) VALUES (?, ?, ?, ?, ?)", (f_problemId, f_title, f_author, f_time, f_content))
            conn.commit()
        except Exception as e:
            raise e