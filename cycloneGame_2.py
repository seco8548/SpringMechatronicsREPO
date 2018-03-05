
import RPi.GPIO as GPIO
import time

#setup GPIO using Board numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
count = 18
#def checkButton()
GPIO.add_event_detect(5, GPIO.RISING)

def lightLED(count):
    GPIO.setup(count, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    time.sleep(0.5)
    GPIO.setup(count, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:

    if count < 25:
        lightLED(count)
        #if GPIO.input(5) ==1:
        if GPIO.event_detected(5):
            print(count)
            if count ==21:
                GPIO.setup(count, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
                time.sleep(5)
                GPIO.setup(count, GPIO.IN, pull_up_down = GPIO.PUD_UP)
                break
        count=count+1
    else:
        count=18
#GPIO.cleanup()
