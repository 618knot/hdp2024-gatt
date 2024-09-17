import RPi.GPIO as GPIO



X_PIN = 20
Y_PIN = 21



# テスト用。後で消す
# from time import sleep
# try:
#     while True:
#         input_x = GPIO.input(X_PIN)
#         input_y = GPIO.input(Y_PIN)
#         print(f"x: {input_x}, y: {input_y}")
#         sleep(1)
# except:
#     GPIO.cleanup()
#     print("stop")

class Joystick:
    # default values
    input_x = 0
    input_y = 0
    
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([X_PIN, Y_PIN], GPIO.IN)
        
    def get_values(self):
        input_x = GPIO.input(X_PIN)
        input_y = GPIO.input(Y_PIN)
        
        return { "x": input_x, "y": input_y }

    def cleanup(self):
        GPIO.cleanup()
