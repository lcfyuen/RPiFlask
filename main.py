import RPi.GPIO as GPIO
import time

ledPin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

# while 1:
GPIO.output(ledPin, True)
time.sleep(1)
GPIO.output(ledPin, False)
time.sleep(1)

GPIO.cleanup()
