from django.shortcuts import render
import pyrebase
import json
import os.path
import datetime
import socket


def getData():
	scriptpath = os.path.dirname(__file__)
	filename = os.path.join(scriptpath, '****')

	config = {
	  "apiKey": "****",
	  "authDomain": "****",
	  "databaseURL": "****",
	  "storageBucket": "****",
	  "serviceAccount": filename
	}

	firebase = pyrebase.initialize_app(config)

	auth = firebase.auth()
	user = auth.sign_in_with_email_and_password("****", "****")

	#print (user)

	db = firebase.database()

	#getting the latest record
	tempID = 0

	while (db.child(tempID).get(user['idToken']).val() != None):
		tempID = tempID+1

	latestID =  tempID - 1

	latestRecord = db.child(latestID).get(user['idToken']).val()

	latestRecordJson = json.dumps(latestRecord, sort_keys=True,
							indent=4, separators=(',', ': '))

	x = json.loads(latestRecordJson)

	temp = x['temperature']
	press = x['pressure']
	light = x['light']
	motion = x['motion']
	timestamp = x['lastUpdated']
	status = x['time']
	#decoding datetime str
	tempVar = datetime.datetime.strptime(status, "%Y-%m-%d %H:%M:%S.%f") - datetime.timedelta(hours= 3)# minusing 3 hours to make it gmt like the server time
	currentTime = datetime.datetime.now()
	diff = currentTime - tempVar
	#if the diff is greater than 1 hour than the rasp pi is offline
	if diff > datetime.timedelta(hours= 1):
		status = '<span class="uk-label uk-label-danger">Offline</span>'
	else:
		status = '<span class="uk-label uk-label-success">Online</span>'


	return temp, press, light, motion, timestamp, status


def index(request):
	temp, press, light, motion, timestamp,status = getData()
	host =  request.META['HTTP_HOST']
	return render(request, 'index.html', {"temp": temp, "press" : press, "light" : light, "motion": motion, "timestamp" : timestamp, "status":status, 'h': host})

def success(request):
	#the host ipaddress and port
	s = request.META['HTTP_HOST']
	return render(request, 'success.html' )
