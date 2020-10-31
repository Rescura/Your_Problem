# -*- coding: utf-8 -*-
from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO

app = Flask(__name__)
LED = 8

GPIO.setmode(GPIO.BOARD) #BOARD는 커넥터 pin번호 사용
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/led/on")
def led_on():
    try:
        GPIO.output(LED, GPIO.HIGH)
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/led/off")
def led_off():
    try:
        GPIO.output(LED, GPIO.LOW)
        return "ok"
    except expression as identifier:
        return "fail"

@app.route("/gpio/clean")
def gpio_clean():
    GPIO.cleanup()
    return "GPIO CLEANUP"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
