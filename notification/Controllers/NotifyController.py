from flask import Flask 
from models import DeviceFcmToken, db
import helpers
from Exceptions.ExceptionHandler import DDTException

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