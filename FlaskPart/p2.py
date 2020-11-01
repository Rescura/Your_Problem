import RPi.GPIO as GPIO
import pymysql

from flask import Flask, request

app = Flask(__name__)


db=pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')

cur = db.cursor()
cur.execute("SELECT * FROM test")
rows = cur.fetchall()
print(rows)
db.close()


btn=5
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn, GPIO.OUT, initial=GPIO.LOW )

#동적 라우팅 <산형 괄호>
#hello/on
'''
@app.route("/hello/<state>")
def hello(state):
    if state == "on":
        GPIO.output(btn, GPIO.HIGH)
    elif state == "off":
        GPIO.output(btn, GPIO.LOW)
    return "LED " + state
'''



#http://0.0.0.0:5001/btn?state=off 이런식으로 호출
# 동적 라우팅<쿼리 스트링 사용>


@app.route("/btn")
def led():
    state = request.values.get("state", "error")
    if state == "on":
        GPIO.output(btn, GPIO.HIGH)
    elif state == "off":
        GPIO.output(btn, GPIO.LOW)
    elif state == "error":
        return "쿼리 스트링 state가 전달 되지 않았음."
    else:
        return "잘못된 쿼리스트링이 전달되었습니다."
    return "LED " + state

@app.route("/지원이바보")
def 지원이바보2():

    return "정현이 바보22"

@app.route("/gpio/cleanup")
def gpio_cleanup():
    GPIO.cleanup()
    return "GPIO CLEANUP"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)