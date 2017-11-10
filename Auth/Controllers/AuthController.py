from flask import Flask, render_template, redirect, flash, url_for, session
from models import User, UserToken, UserDetail
from Exceptions.ExceptionHandler import DDTException
from Auth.AuthRepository import AuthRepository, UserTokenRepository, UserDetailsRepository
import helpers, datetime
from Auth.AuthValidator import create_user_rule
from wrapper import GoogleAuthentication
from wrapper import FacebookAuthentication
from wrapper import GithubAuthentication
import AuthController
import models

def create_user(data):
	create_user_rule(data)
	repo = AuthRepository()
	user_detail_repo = UserDetailsRepository()
	inputs = {
		'id' : helpers.generate_unique_code().__str__(),
		'email' : data['email'],
		'password' : helpers.hash_password(data['password']), 
		'display_name' : data['displayName'],
		'is_password_change_required' : data['is_password_change_required']\
			if 'is_password_change_required' in data else False
	}
	user = repo.store(User, inputs)
	user_detail = {
		'id' : helpers.generate_unique_code().__str__(),
		'user_id' : user.id,
		'first_name' : data['firstName']\
			if 'firstName' in data else None,
		'last_name' : data['lastName']\
			if 'lastName' in data else None
	}
	user_detail_repo.create_user_details(UserDetail, user_detail)
	return user


def legacy_login_api(data):
	repo = AuthRepository()
	tokenRepo = UserTokenRepository()
	userObj = repo.filter_attribute(User, {'email': data['email']})
	if hasattr(userObj, 'email'):
		isValid = helpers.validate_hash_password(data['password'], userObj.password)
		if isValid:
			token = helpers.access_token()
			return tokenRepo.store(UserToken, 
				{
				'id' : helpers.generate_unique_code().__str__(),
				'token' : token, 
				'user_id' : userObj.id
				})
	raise DDTException('Invalid credentials', 422)

def social_signin(provider):
	return getattr(AuthController, helpers.get_redirect_resolver(provider))()
	# return locals()[helpers.get_redirect_resolver(provider)]()

def google_redirect():
	return GoogleAuthentication.redirectTo()

def facebook_redirect():
	return FacebookAuthentication.redirectTo()

def github_redirect():
	return GithubAuthentication.redirectTo()

def social_app_login(request):
	return getattr(AuthController, helpers.get_authrize_resolver(request.args.get('provider')))(request)

def google_authorize(request):
	return google_login(GoogleAuthentication.authorize(request))

def facebook_authorize(request):
	return facebook_login(FacebookAuthentication.authorize(request))

def github_authorize(request):
	return github_login(GithubAuthentication.authorize(request))

def google_login(token):
	user_info = GoogleAuthentication.get_user_details(token)
	user = AuthRepository().filter_attribute(models.User, {'email' : user_info['email']})
	if user is None:
		data = {
			'email' : user_info['email'],
			'password' : None,
			'rePassword' : None,
			'displayName' : user_info['display_name'],
			'firstName' : user_info['first_name'],
			'last_Name' : user_info['last_name'],
			'is_password_change_required' : False
		}
		user = create_user(data)
	tokenRepo = UserTokenRepository()
	user_token = helpers.access_token()
	return tokenRepo.store(UserToken, 
		{
		'id' : helpers.generate_unique_code().__str__(),
		'token' : user_token, 
		'user_id' : user.id
		})
	# return user_info
	# social = GoogleSocialAuthentication()
 	#return social.redirect('user')

def facebook_login(token):
	user_info = FacebookAuthentication.get_user_details(token)
	user = AuthRepository().filter_attribute(models.User, {'email' : user_info['email']})
	if user is None:
		data = {
			'email' : user_info['email'],
			'password' : None,
			'rePassword' : None,
			'displayName' : user_info['display_name'],
			'firstName' : user_info['first_name'],
			'last_Name' : user_info['last_name'],
			'is_password_change_required' : False
		}
		user = create_user(data)
	tokenRepo = UserTokenRepository()
	user_token = helpers.access_token()
	return tokenRepo.store(UserToken, 
		{
		'id' : helpers.generate_unique_code().__str__(),
		'token' : user_token, 
		'user_id' : user.id
		})

def github_login(token):
	user_info = GithubAuthentication.get_user_details(token)
	user = AuthRepository().filter_attribute(models.User, {'email' : user_info['email']})
	if user is None:
		data = {
			'email' : user_info['email'],
			'password' : None,
			'rePassword' : None,
			'displayName' : user_info['display_name'],
			'firstName' : user_info['first_name'],
			'last_Name' : user_info['last_name'],
			'is_password_change_required' : False
		}
		user = create_user(data)
	tokenRepo = UserTokenRepository()
	user_token = helpers.access_token()
	return tokenRepo.store(UserToken, 
		{
		'id' : helpers.generate_unique_code().__str__(),
		'token' : user_token, 
		'user_id' : user.id
		})

def api_google_login(token):
	user_info = GoogleAuthentication.authenticate_token(token)
	user = AuthRepository().filter_attribute(models.User, {'email' : user_info['email']})
	if user is None:
		data = {
			'email' : user_info['email'],
			'password' : None,
			'rePassword' : None,
			'displayName' : user_info['display_name'],
			'firstName' : user_info['first_name'],
			'last_Name' : user_info['last_name'],
			'is_password_change_required' : False
		}
		user = create_user(data)
	tokenRepo = UserTokenRepository()
	user_token = helpers.access_token()
	return tokenRepo.store(UserToken, 
		{
		'id' : helpers.generate_unique_code().__str__(),
		'token' : user_token, 
		'user_id' : user.id
		})

def logout(token):
	tokenRepo = UserTokenRepository()
	return tokenRepo.deleteToken(UserToken, token)

