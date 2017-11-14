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



