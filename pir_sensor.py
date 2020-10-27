#!/usr/bin/env python3
import config
import logging
import requests
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

def MOTION(PIR_PIN):
	url = create_request(config.DOMOTICZ_SERVER_IP, config.DOMOTICZ_SERVER_PORT, config.IDX, 'On')
	send_to_domoticz(url)
	print ('Motion Detected!')

def create_request(server, port, idx, state):
	url = (
		f"http://{server}:{port}"
		f"/json.htm?type=command&param=switchlight&idx={idx}"
		f"&switchcmd={state}")
	logging.info(f"The request is {url}")
	return url

def send_to_domoticz(url):
	resp = requests.get(url, auth=(config.DOMOTICZ_USERNAME, config.DOMOTICZ_PASSWORD))
	logging.info(f"The response is {resp}")

logging.basicConfig(filename='loginfo.log', level=logging.INFO)
logging.info('Start script...')
logging.info(	f"Input parameters:\r\n"
				f"Domoticz Server IP: {config.DOMOTICZ_SERVER_IP}\r\n"
				f"Domoticz Server Port: {config.DOMOTICZ_SERVER_PORT}\r\n"
				f"Domoticz Server User: {config.DOMOTICZ_USERNAME}\r\n"
				f"Domoticz Server Password: {config.DOMOTICZ_PASSWORD}")

try:
	GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
	while 1:
		time.sleep(100)
except KeyboardInterrupt:
	print ('Quit')
	GPIO.cleanup()
