import RPi.GPIO as GPIO
from flask import Flask, render_template, request, Response
import time

# GPIO 제어코드
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)

#TRIG와 ECHO핀에 사용한 GPIO핀번호를 변수를 통해 초기화하고, 
# 초음파 신호를 주고 받을 수 있도록 setup함수를 이용하여 설정한다.
TRIG = 23                                  
ECHO = 24
RIGHT_FORWARD = 26                                  
RIGHT_BACKWARD = 19                                   
RIGHT_PWM = 13
LEFT_FORWARD = 21                                  
LEFT_BACKWARD = 20                                   
LEFT_PWM = 16 

GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(RIGHT_FORWARD,GPIO.OUT)                  
GPIO.setup(RIGHT_BACKWARD,GPIO.OUT)
GPIO.setup(RIGHT_PWM,GPIO.OUT)
GPIO.output(RIGHT_PWM, 0)
RIGHT_MOTOR = GPIO.PWM(RIGHT_PWM, 100)
RIGHT_MOTOR.start(0)
RIGHT_MOTOR.ChangeDutyCycle(0)

GPIO.setup(LEFT_FORWARD,GPIO.OUT)                  
GPIO.setup(LEFT_BACKWARD,GPIO.OUT)
GPIO.setup(LEFT_PWM,GPIO.OUT)
GPIO.output(LEFT_PWM, 0)
LEFT_MOTOR = GPIO.PWM(LEFT_PWM, 100)
LEFT_MOTOR.start(0)
LEFT_MOTOR.ChangeDutyCycle(0)


def getDistance():
  GPIO.output(TRIG, GPIO.LOW)                 
  time.sleep(1)                            

  GPIO.output(TRIG, GPIO.HIGH)                  
  time.sleep(0.00001)                      
  GPIO.output(TRIG, GPIO.LOW)

  #When the ECHO is LOW, get the purse start tim
  while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
    pulse_start = time.time()              #Saves the last known time of LOW pulse

  #When the ECHO is HIGN, get the purse end time
  while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
    pulse_end = time.time()                #Saves the last known time of HIGH pulse 

  #Get pulse duration time
  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  #Multiply pulse duration by 17150 to get distance and round
  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  return distance

#Right Motor Control 
def rightMotor(forward, backward, pwm):
  GPIO.output(RIGHT_FORWARD,forward)
  GPIO.output(RIGHT_BACKWARD,backward)
  RIGHT_MOTOR.ChangeDutyCycle(pwm)

#Left Motor Control 
def leftMotor(forward, backward, pwm):
  GPIO.output(LEFT_FORWARD,forward)
  GPIO.output(LEFT_BACKWARD,backward)
  LEFT_MOTOR.ChangeDutyCycle(pwm)

#Forward Car
def forward():
    rightMotor(1, 0, 70)
    leftMotor(1, 0, 70)
    time.sleep(1)

#Left Car
def left():
    rightMotor(0, 0, 0)
    leftMotor(1, 0, 70)
    time.sleep(0.3)

#Right Car
def right():
    rightMotor(1, 0, 70)
    leftMotor(0, 0, 0)
    time.sleep(0.3)

#Stop Car
def stop():
    rightMotor(0, 0, 0)
    leftMotor(0, 0, 0)#Forward Car
def forward():
    rightMotor(1, 0, 70)
    leftMotor(1, 0, 70)
    time.sleep(1)

#Left Car
def left():
    rightMotor(1, 0, 70)
    leftMotor(0, 0, 70)
    time.sleep(0.3)

#Right Car
def right():
    rightMotor(0, 0, 70)
    leftMotor(1, 0, 70)
    time.sleep(0.3)

#Backward Car
def backward():
    rightMotor(0, 1, 70)
    leftMotor(0, 1, 70)
    time.sleep(0.3)

#Stop Car
def stop():
    rightMotor(0, 0, 0)
    leftMotor(0, 0, 0)

@app.route("/<command>")
def action(command):
    distance_value = getDistance()
    if command == "F":
        forward()
        message = "Moving Forward"
    elif command == "L":
        left() 
        message = "Turn Left"
    elif command == "R":
        right()   
        message = "Turn Right"
    elif command == "S":
        stop()   
        message = "Stop"  
    elif command == "B":
        backward()   
        message = "Moving Backward"
    else:
        stop()
        message = "Unknown Command [" + command + "] " 

    msg = {
        'message' : message,
        'distance': str(distance_value)
    }
        
    return render_template('video.html', **msg)

#getDistance()함수를 이용하여 장애물간의 거리를 구한다
#1초간격으로 초음파 센서를 껐다 켜면서 초음파 센서를 작동하도록 한다. 
#껐다 켤때의 시간을 start 와 end 변수에 나눠 담고, 
# 둘의 차를 계산한뒤 17150을 곱하여 거리를 측정한다.

if __name__ == '__main__':
  try:
    while True:
      distance_value = getDistance()
      #Check whether the distance is 50 cm
      if distance_value > 50:      
          #Forward 1 seconds
          print ("Forward " + str(distance_value))
          rightMotor(1, 0, 70)
          leftMotor(1, 0, 70)
          time.sleep(1)
      else:
          #Left 1 seconds
          print ("Left " + str(distance_value))
          rightMotor(0, 0, 0)
          leftMotor(1, 0, 70)
          time.sleep(1)

  except KeyboardInterrupt:
    print ("Terminate program by Keyboard Interrupt")
    GPIO.cleanup()