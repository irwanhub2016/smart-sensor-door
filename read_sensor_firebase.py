import uuid
import time
import RPi.GPIO as GPIO
import firebase_admin
import os
import time
import datetime
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from firebase_admin import credentials
from firebase_admin import db

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

cred = credentials.Certificate(os.getenv("KEY"))

firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_HOST")
})

def read_sensor():
        global code
        global goto
        global status
        try:
                while True:
                        operate = datetime.datetime.now()
                        schedule = operate.strftime("%Y-%m-%d %H:%M")
                        if GPIO.input(25):
                                print ("HIGH")
                                print ('Warung: ' + mac_address)
                                print ("Warung Buka")
                                goto = schedule
                                print (goto)
#                               code
#                               global code
                                code = 1
                                status = 'Warung lagi buka'
                        else:
                                print ("LOW")
                                print ('Warung: ' + mac_address)
                                print ("Warung Tutup")
                                goto = schedule
                                print (goto)
#                               code
#                               global code
                                code = 0
                                status = 'Warung lagi tutup'
                        update_sensor()
                        time.sleep(1)

        except:
                GPIO.cleanup()

def submit_sensor(value):
    value['sensor_value'] = code
    value['time_operational'] = goto
    value['operational_status'] = status
    return value

def update_sensor():
    print('mark done')
    try:
        ref = db.reference("nodes/" + mac_address)
        ref.transaction(submit_sensor)
        print('Push data sensor success !')
    except db.TransactionError:
        print('Fail !')
    print("Completed")

    print("done")

read_sensor()

