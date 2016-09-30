import RPi.GPIO as GPIO

ledPin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

while 1:
  GPIO.output(ledPin, GPIO.HIGH)
  time.sleep(0.2)
  GPIO.output(ledPin, GPIO.LOW)
  time.sleep(0.2)