import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from datetime import datetime

sensor = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

previous_state = False
current_state = False
camera = PiCamera()

while True:
    time.sleep(0.1)
    previous_state = current_state
    current_state = GPIO.input(sensor)
    i = 0
    if current_state:
        i = time.clock()
        print("motion detected %s" % (i)) 
        if i > 0.05:
            print("time limit met")
            filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
            camera.capture("/home/pi/detector/images/%s"%filename)
            #            camera.capture("%s.jpg" % filename)
        else:
            continue
            #   camera.start_recording(filename)
    #if !current_state:
        #camera.stop_recording()

    # if current_state != previous_state:
    #     new_state = "HIGH" if current_state else "LOW"
    #     print("GPIO pin %s is %s" % (sensor, new_state))
    #     timing = 0.0
    #     if new_state == "HIGH":
    #         timing = time.clock()
    #         if timing >= 5:
    #             print("time limit reached")
