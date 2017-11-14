from flask import Flask, Blueprint, request, json, jsonify
from flask import render_template
from Controllers.NotifyController import *
from App.Response import *
from decorators import validate_jwt_token, api_login_required
from Exceptions.ExceptionHandler import DDTException

notify = Blueprint('notify', __name__, template_folder='templates')

@notify.route('/fcm', methods=['POST'])
@validate_jwt_token
def store_fcm():
	data = request.json
	response =  add_fcm(data)
	if response:
		return respondOk("token saved")
	raise DDTException("Failed to save Token")

@notify.route('/notify', methods=['GET'])
@validate_jwt_token
def notify_all():
	response = notify_device()
	if response:
		return respondOk("notification send")
	return respondWithError("Failed To send notification")

