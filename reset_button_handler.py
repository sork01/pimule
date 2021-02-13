from threading import Thread
import RPi.GPIO as GPIO
import time

class GPIOButtonHandler(Thread):
    def __init__(self, function, pin):
        Thread.__init__(self)
        self.function = function
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN)

    def execute_function(self):
        print('button pressed!')
        self.function()

    def run(self):
        input = GPIO.input(self.pin)
        lastpress = 0
        while True:
            if input and lastpress == 0:
                self.execute_function()
                time.sleep(2)
            time.sleep(0.1)
            lastpress = input
            input = GPIO.input(self.pin)