from RPi import GPIO as GPIO
import time
import os
from twilio.rest import Client

input_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

account_sid = 'Insert your own Twilio Account SID'

apiToken = 'Insert your own Twilio API Token'

client = Client(account_sid, apiToken)


previous_state = None

def check_sensor():
    global previous_state
    try:
        sensor_state = GPIO.input(input_pin)
        
        if sensor_state == GPIO.HIGH:
            print('Sensor is NOT blocked (GPIO HIGH)')
            if previous_state == GPIO.LOW: 
                print("Clear")
                time.sleep(2)
        else:
            print('Sensor is blocked (GPIO LOW)')
            if previous_state != GPIO.LOW: 
                print("Tripped          Sending notification...")
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    to='whatsapp:+{Insert Your Phone Number in format: 11234567890 -> Country Code, Area Code, Phone Number}',
                    body='Motion Detected'
                )
                print(f"Alert dispatched: {message.sid}")
                time.sleep(2)
        
        previous_state = sensor_state

    except Exception as e:
        print(f"Error: {e}")
        GPIO.cleanup()

# Main loop
try:
    print
    while True:
        check_sensor()
        time.sleep(0.1) 
except KeyboardInterrupt:
    print("Exiting program...")
    GPIO.cleanup()
