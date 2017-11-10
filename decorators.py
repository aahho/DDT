from flask import Flask, session, redirect, request
from Exceptions.ExceptionHandler import DDTException
from Auth.AuthRepository import UserTokenRepository
from models import UserToken
import jwt
from app import app

def login_required(func):
	def wraps(*args, **kwargs):
		if session.has_key('token'):
			repo = UserTokenRepository()
			tokenObj = repo.check_valid_token(UserToken, session['token'])
			if hasattr(tokenObj, 'token'):
			 	return func(*args, **kwargs)
		return redirect('/admin/')
	wraps.func_name = func.func_name
	return wraps

def api_login_required(func):
	def wraps(*args, **kwargs):
		if request.headers.has_key('access-token'):
			repo = UserTokenRepository()
			token = request.headers['access-token']
			tokenObj = repo.check_valid_token(UserToken, token)
			if hasattr(tokenObj, 'token'):
				request.__setattr__('user', tokenObj.transform()['user'])
			 	return func(*args, **kwargs)
		raise DDTException('Unauthorized request', 401)
	wraps.func_name = func.func_name
	return wraps

def validate_jwt_token(func):
	def wraps(*args, **kwargs):
		if request.headers.has_key('app-token'):
			token = request.headers['app-token']
			try:
				payload = jwt.decode(token, app.config['APP_SECRET'], algorithm='HS256')
			except Exception as e:
				raise DDTException('Unauthorized request', 401)
			if payload['app_name'] == app.config['APP_NAME']:
				return func(*args, **kwargs)
		raise DDTException('Unauthorized request', 401)
	wraps.func_name = func.func_name
	return wraps