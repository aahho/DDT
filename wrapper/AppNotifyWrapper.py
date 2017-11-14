from flask import Flask 
# Send to single device.
from pyfcm import FCMNotification
from app import app

def notify_all(fcm_tokens, message_title, message_body):
	push_service = FCMNotification(api_key=app.config['FIREBASE_KEY'])
	push_service = FCMNotification(api_key=app.config['FIREBASE_KEY'])
	# Send to multiple devices by passing a list of ids.
	registration_ids = fcm_tokens
	message_title = message_title
	message_body = message_body

	# data_message = {
	# 	'title' : message_title,
	# 	'message_body' : message_body,
	# 	'image' : 'https://www.google.co.in/search?q=images&safe=active&rlz=1C5CHFA_enIN701IN701&source=lnms&tbm=isch&sa=X&ved=0ahUKEwi0ttb1vb7XAhXLYo8KHYemBvYQ_AUICigB&biw=1280&bih=703#imgrc=mVrwcCQle9g31M:'
	# }
	# To support rich notifications on iOS 10, set
	extra_kwargs = {
	    'mutable_content': True
	}
	result = push_service.notify_multiple_devices(registration_ids=registration_ids,\
		 message_title=message_title, message_body=message_body, extra_kwargs=extra_kwargs)
	# result = push_service.notify_multiple_devices(registration_ids=registration_ids,\
	# 	 message_title=message_title, data_message=data_message, extra_kwargs=extra_kwargs)

	return result