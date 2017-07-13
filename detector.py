#!/usr/bin/python
import MySQLdb
import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from datetime import datetime

hostname = 'localhost'
username = 'root'
password = 'charlie724'
database = 'USER_STORAGE'

def readfile(filename):
    #with open(filename, 'rb') as f:
     #   photo = f.read()
    fin = open(filename)
    photo = fin.read()
    return photo

def insert_photo(conn, filename, date, time):
    cur = conn.cursor()
    
    data = readfile(filename)
    
    #query =
    print "filename: %s"%filename
#    print "data: %s"%data
#    query= "INSERT INTO USERPHOTOS VALUES(%s,%s,%s,%s)"
    query = "INSERT INTO USERPHOTOS VALUES(LOAD_FILE(%s),%s,%s,%s)"
    print query
#    cur.execute(query,(data,date,time,filename))
    cur.execute(query,(filename,date,time,filename))
    print "rows inserted: %s" % cur.rowcount
    conn.commit()
    
    
    #args = (filename, date, time)

    #db = MySQLdb.connect("raspberrypi", "root","charlie724","USER_STORAGE")

    #cursor = db.cursor()

    #try:
     #   cursor.execute(query,args)
      #  db.commit()
    #except:
     #   db.rollback()

     #db.close()
def connect(filename,date,time):
    myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
    insert_photo(myConnection, filename, date, time)
    myConnection.close()
     
def runpi():
    print("runpi")
    sensor = 4

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

    previous_state = False
    current_state = False
    camera = PiCamera()
    loop = True
    while True:
        
        time.sleep(0.1)
        previous_state = current_state
        current_state = GPIO.input(sensor)
        i = 0
        if current_state:
            #if loop == False:
             #   exit()
            i = time.clock()
            print("motion detected %s" % (i)) 
            if i > 0.05:
                print("time limit met")
                take_pic = raw_input('Take image? (y/n)')
                if take_pic == 'n':
                   # loop = False
                    #continue
                    exit()
                if take_pic == 'y':
                    #loop = True
    #                filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
   #                 camera.capture("/home/pi/detector/images/%s"%filename)
  #                  file = "/home/pi/detector/images/%s"%filename
 #                   date = datetime.now().strftime("%Y-%m-%d")
#                    p_time = datetime.now().strftime("%H.%M.%S")
                #            camera.capture("%s.jpg" % filename)
                    print("picture taken!")
                    save_img = raw_input("Save image? (y/n)")
                    if save_img == 'n':
                      exit()
                    if save_img == 'y':
                        filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
                        file = "/home/pi/detector/images/%s"%filename
                        camera.capture("%s"%file)
                        date = datetime.now().strftime("%Y-%m-%d")
                        p_time = datetime.now().strftime("%H.%M.%S")
                        connect(file,date,p_time)
                    #else:
                        #continue
                        
                   # update_blob(file,date,p_time)
            #else:
                #exit()
                #continue
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

runpi()
