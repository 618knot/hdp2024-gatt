from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup([20, 21], GPIO.IN)

try:
    while True:
        input20 = GPIO.input(20)
        input21 = GPIO.input(21)
        print(f"20: {input20}, 21: {input21}")
        sleep(1)
except:
    GPIO.cleanup()
    print("stop")
