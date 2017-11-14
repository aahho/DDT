from flask import Flask 
from models import DeviceFcmToken, db
import helpers, requests
from Exceptions.ExceptionHandler import DDTException
from wrapper import AppNotifyWrapper
from app import app

def add_fcm(data):
	fcm_token = data['fcm_token']
	device = data['device']
	existing_token = DeviceFcmToken.query.filter(DeviceFcmToken.fcm_token == fcm_token).first()
	if not existing_token:
		new_token = DeviceFcmToken(
			id = helpers.generate_unique_code(),
			fcm_token = fcm_token,
			device = device
		)
		db.session.add(new_token)
		db.session.commit()
		return new_token
	raise DDTException("token already registerd")

def notify_device():
	fcm_data = DeviceFcmToken.query.all()
	server_url = helpers.get_feedr_url()+'/latestNews'
	headers = {
        "app-token" : app.config['FEEDR_ACCESS_CODE']
    }
	letest_news = requests.get(server_url, headers=headers)
	if letest_news.status_code == 200:
		fcm_tokens = []
		message_title = letest_news.json()['data']['title']
		message_body = letest_news.json()['data']['summary'].split('.')[0]
		for data in fcm_data:
			fcm_tokens.append(data.fcm_token)
		notify = AppNotifyWrapper.notify_all(fcm_tokens, message_title, message_body)
		return True
	return False

