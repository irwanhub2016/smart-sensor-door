import uuid
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

try:
        while True:
                if GPIO.input(25):
#                if button_state == GPIO.HIGH:
                        print ("HIGH")
#                       print (hex(uuid.getnode()))
                        print ('Warung: ' + mac_address)
                        print("Buka")
                else:
                        print ("LOW")
#                       print (hex(uuid.getnode()))
                        print ('Warung: ' + mac_address)
                        print ("Warung Tutup")
                time.sleep(2)

except:
        GPIO.cleanup()

