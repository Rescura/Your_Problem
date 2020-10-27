# -*- coding: utf-8 -*-
# 필요한 모듈을 불러옵니다.
import RPi.GPIO as GPIO
import time
# 사용할 GPIO핀의 번호를 선정합니다.
LED = 8

# 사용할 GPIO모드를 선택합니다. BOARD는 순서, BCM은 사전예약 순서
GPIO.setmode(GPIO.BOARD)

GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)

for i in range(10):
	GPIO.output(LED, GPIO.HIGH)
	time.sleep(0.5)
			
	GPIO.output(LED, GPIO.LOW)
	time.sleep(0.5)

# GPIO 설정 초기화
GPIO.cleanup()      
