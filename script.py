
'''
jac6AYjjy9uPDr_P0b_YhrhgRvo_rjO7
'''

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # pin numbering according to SoC
ir_sensor = 2 # ir sensor cnnected to pin 2
led1 = 3   # output for load 1
buzzer = 27
led2 = 4   # output for load 2
flame_sensor = 17
GPIO.setup(ir_sensor, GPIO.IN) # configure as input pin
GPIO.setup(flame_sensor, GPIO.IN) # configure as input pin
GPIO.setup(led1, GPIO.OUT, initial=GPIO.HIGH) # configure as output pin
GPIO.setup(led2, GPIO.OUT, initial=GPIO.HIGH) # configure as output pin
GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW) # configure as output pin
import BlynkLib  # blynk module

BLYNK_AUTH = 'jac6AYjjy9uPDr_P0b_YhrhgRvo_rjO7' # token api for authorisation

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)   # for on/off load 1
def my_write_handler(value):
    print('Current V1 value: {}'.format(value[0]))
    if int(format(value[0])) == 1:
        GPIO.output(led1, GPIO.HIGH) # Turn on
    else:
        GPIO.output(led1, GPIO.LOW) # Turn off

@blynk.VIRTUAL_WRITE(2) # for on/off load 2
def my_write_handler(value):
    print('Current V2 value: {}'.format(value[0]))
    if int(format(value[0])) == 1:
        GPIO.output(led2, GPIO.HIGH) # Turn on
    else:
        GPIO.output(led2, GPIO.LOW) # Turn off

@blynk.VIRTUAL_READ(3)
def my_read_handler():
    if(GPIO.input(ir_sensor)):
        blynk.virtual_write(3,"Intruder Detected")
    else:
        blynk.virtual_write(3,"Intruder Not Detected")
    
try:
    while True: 
        blynk.run()
#        my_write_handler
        if(GPIO.input(ir_sensor)):  # no output from ir sensor
            blynk.virtual_write(3,"No Intruder")
            GPIO.output(buzzer, GPIO.LOW) # Turn on
            print("No Intruder")
        else:  # when ir sensor detects object
            blynk.virtual_write(3,"Intruder")
            GPIO.output(buzzer, GPIO.HIGH) # Turn on
            sleep(2)
            GPIO.output(buzzer, GPIO.LOW) # Turn on
            print("Intruder")
            
        if(GPIO.input(flame_sensor)):  # no output from flane sensor
            blynk.virtual_write(3,"No Flame")
            GPIO.output(buzzer, GPIO.LOW) # Turn on
            print("No Flame")
        else:  # when flame sensor detects object
            blynk.virtual_write(3,"Flame")
            GPIO.output(buzzer, GPIO.HIGH) # Turn on
            sleep(2)
            GPIO.output(buzzer, GPIO.LOW) # Turn on
            print("Flame")
            
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit(0)
