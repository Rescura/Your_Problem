from flask import Flask
from flask_restful import Resource, Api, reqparse
import database 
import os

from colorama import init, Fore

init(autoreset=True)

app = Flask(__name__)
api = Api(app)

# uri : /problems
class ProblemsIndex(Resource):
    def get(self)->list:
        """ ProblemsIndex.get : db에서 고민 목록을 받아와 간략한 정보를 json으로 반환함 """
        problemsList = database.get_problems_list()
        problemsCount = len(problemsList)
        problemsJsonList = list(map(lambda p:
        {
            "problemId" : p[0],
            "problemTitle" : p[1],
            "problemAuthor" : p[2],
            "problemTime" : p[3],
            "problemContent" : p[4][0:50]
        } ,problemsList))

        return {
            "StatusCode" : 400,
            "Message" : "Get Successful", 
            "Counts" : problemsCount,
            "Problems" : problemsJsonList
            }

    def post(self):
        """ ProblemsIndex.post : post로 json형식으로 보낸 나의 고민 정보를 데이터베이스에 추가시켜줌 """

        try:
            # argument 값이 이상하게 들어오면 400 에러를 표시
            parser = reqparse.RequestParser()
            parser.add_argument('problemTitle', type=str)
            parser.add_argument('problemAuthor', type=str)
            parser.add_argument('problemTime', type=str)
            parser.add_argument('problemContent', type=str)
            args = parser.parse_args()
            
            resultId = database.insert_problem(
                args['problemTitle'],
                args['problemAuthor'],
                args['problemTime'],
                args['problemContent']
                )

            return {'StatusCode' : '400', 'Message' : 'Post Successful', 'ResultId' : resultId}

        except Exception as e:
            return {'StatusCode' : '1000', 'Message' : f'Post Failed : {e}', 'ResultId' : -1}
        

# uri : /problems/<int:problem_id>/problem
class Problems(Resource) :
    def get(self, problem_id):
        """ Problems.get : db에서 problemId == problem_id 인 고민의 정보 전체를 json으로 반환함 """
        problemData = database.get_problem(problem_id)
        return {
            "StatusCode" : 400,
            "Message" : "Get Successful",
            "ProblemData" : { 
                "problemId" : problemData[0],
                "problemTitle" : problemData[1],
                "problemAuthor" : problemData[2],
                "problemTime" : problemData[3],
                "problemContent" : problemData[4]
            }
        }

# uri : /problems/<int:id>/replys
class ReplysIndex(Resource):
    def get(self, problem_id):
        """ problemId == id 인 고민 정보를 최신순으로 모두 json형태로 반환한다. """
        replysList = database.get_replys_list(problem_id)
        replysCount = len(replysList)
        replysJsonList = list(map(lambda reply:
        {
            "replyId" : reply[0],
            "problemId" : reply[1],
            "replyTitle" : reply[2],
            "replyAuthor" : reply[3],
            "replyTime" : reply[4],
            "replyContent" : reply[5][0:50]
        } ,replysList))

        return { 
            "StatusCode" : 400,
            "Message" : "Get Successful",
            "Counts" : replysCount,
            "Replys" : replysJsonList
            }

    def post(self, problem_id):
        """ problemId == id인 고민에 대한 답장 정보를 받아 DB에 추가한다. 그 후 응답을 한다. """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('replyTitle', type=str)
            parser.add_argument('replyAuthor', type=str)
            parser.add_argument('replyTime', type=str)
            parser.add_argument('replyContent', type=str)
            args = parser.parse_args()
            
            database.insert_reply(
                problem_id,
                args['replyTitle'],
                args['replyAuthor'],
                args['replyTime'],
                args['replyContent']
                )

            return {'StatusCode' : '400', 'Message' : 'Post Successful'}

        except Exception as e:
            return {'StatusCode' : '1000', 'Message' : f'Post Failed : {e}'}

#uri : /problems/<int:problem_id>/replys/<int:reply_id>
class Replys(Resource):
    def get(self, problem_id, reply_id):
        """ Replys.get : replyId == reply_id 인 답장의 전체 내용을 json파일로 보내준다. """
        replyData = database.get_reply(reply_id)
        return {
            "StatusCode" : 400,
            "Message" : "Get Successful",
            "ReplyData":{
                "problemId" : replyData[0],
                "replyTitle" : replyData[1],
                "replyAuthor" : replyData[2],
                "problemTime" : replyData[3],
                "replyTime" : replyData[4],
                "replyContent" : replyData[5]
            }
        }

# uri : /lights/setLevel<int:level>
class Lights(Resource):
    def get(self, level):
        print(f"[api.py /lights/setLevel/<int:level>] : setting Level to {level}")
        try :
            print(f"Successfully set light level to {level}")
            return {"Message": f"Successfully set light level to {level}"}

        except Exception as e:
            print(f"Failed to set light level to {level}")
            return {"Message": f"Failed to Set light level to {level} | {e}" }


api.add_resource(ProblemsIndex, '/problems/')
api.add_resource(Problems, '/problems/<int:problem_id>/problem')
api.add_resource(ReplysIndex, '/problems/<int:problem_id>/reply')
api.add_resource(Replys, '/problems/<int:problem_id>/reply/<int:reply_id>')
api.add_resource(Lights, '/lights/setLevel<int:level>')

def runServer(f_debug: bool= False) : 
    database.create_table()
    app.run(debug=True)

if __name__ == '__main__':
    runServer(f_debug=True)
