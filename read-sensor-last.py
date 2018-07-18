import uuid
import time
import RPi.GPIO as GPIO
import firebase_admin
import os
import time
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from firebase_admin import credentials
from firebase_admin import db

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

# Fetch the service account key JSON file contents
cred = credentials.Certificate(os.getenv("KEY"))

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv("FIREBASE_HOST")
})

def read_sensor():
	global code
	try:
	        while True:
                        sec=int(time.strftime("%S"))
                        if GPIO.input(25):
	                        print ("HIGH")
	                        print ('Warung: ' + mac_address)
	                        print ("Buka")
#				code
#	                        global code
	                        code = 1
                        else:
	                        print ("LOW")
	                        print ('Warung: ' + mac_address)
	                        print ("Warung Tutup")
#				code
#	                        global code
	                        code = 0
	                update_sensor()
	                time.sleep(1)

	except:
	        GPIO.cleanup()

def submit_sensor(value):
    #operate_time =  datetime.datetime.now()
    #print(now.hour + ':' + now.minute)
    value['sensor_value'] = code
    #value['operational_time'] = sec
    return value

def update_sensor():
    print('mark done')
    try:
        ref = db.reference("nodes/" + mac_address)
        ref.transaction(submit_sensor)
        print('Transaction completed')
    except db.TransactionError:
        print('Transaction failed to commit')
    print("submitted")

    print("done")

read_sensor()

