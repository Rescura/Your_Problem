from flask import Flask
from flask_restful import Resource, Api, reqparse
import database 

app = Flask(__name__)
api = Api(app)

# uri : /problems
class ProblemsIndex(Resource) :
    def get(self):
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

        return { "counts" : problemsCount, "problems" : problemsJsonList}

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
            
            database.insert_problem(
                args['problemTitle'],
                args['problemAuthor'],
                args['problemTime'],
                args['problemContent']
                )

            return {'StatusCode' : '400', 'Message' : 'Post Successful'}

        except Exception as e:
            return {'StatusCode' : '1000', 'Message' : f'Post Failed : {e}'}
        

# uri : /problems/<int:problem_id>/problem
class Problems(Resource) :
    def get(self, problem_id):
        """ Problems.get : db에서 problemId == problem_id 인 고민의 정보 전체를 json으로 반환함 """
        problemData = database.get_problem(problem_id)
        return {
            "problemId" : problemData[0],
            "problemTitle" : problemData[1],
            "problemAuthor" : problemData[2],
            "problemTime" : problemData[3],
            "problemContent" : problemData[4]
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

        return { "counts" : replysCount, "problems" : replysJsonList}

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
            "problemId" : replyData[0],
            "replyTitle" : replyData[1],
            "replyAuthor" : replyData[2],
            "problemTime" : replyData[3],
            "replyTime" : replyData[4],
            "replyContent" : replyData[5]
        }

# uri : /lights/<str:mode>
class Lights(Resource):
    def get(self, mode):
        if mode == 'on' :
            # TODO : LED를 켜는 함수 붙여넣기
            pass
        elif mode == 'off':
            # TODO : LED를 끄는 함수 붙여넣기
            pass
        elif mode == 'brighter' :
            # TODO : LED를 밝게 하는 함수 붙여넣기
            pass
        elif mode == 'dimmer' :
            # TODO : LED를 어둡게 하는 함수 붙여넣기
            pass

api.add_resource(ProblemsIndex, '/problems/')
api.add_resource(Problems, '/problems/<int:problem_id>/problem')
api.add_resource(ReplysIndex, '/problems/<int:problem_id>/reply')
api.add_resource(Replys, '/problems/<int:problem_id>/reply/<int:reply_id>')
api.add_resource(Lights, '/lights/<str:mode>')

def runServer() : 
    database.create_table()
    app.run()

if __name__ == '__main__':
    runServer()