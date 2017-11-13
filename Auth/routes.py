from flask import Flask, Blueprint, request, session
from flask import render_template, jsonify
from App.Response import *
from Controllers.AuthController import *
from decorators import api_login_required

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/users/register', methods=['POST'])
def register():
    data = request.json
    user = create_user(data)
    return respondWithItem(user, statusCode=201)

@auth.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = legacy_login_api(data)
    return respondWithItem(user, statusCode=200)

@auth.route('/api/google', methods=['GET'])
def google():
    token = request.args.get('token')
    device = request.args.get('device')
    response = api_google_login(token, device)
    return respondWithItem(response, statusCode=200)

@auth.route('/app/signin', methods=['GET'])
def signin():
    return social_signin(request.args.get('provider'))

@auth.route('/app/auth', methods=['GET'])
def app_auth():
    response = social_app_login(request)
    print response
    return respondWithItem(response, statusCode=200)
    
@auth.route('/app/logout', methods=['GET'])
@api_login_required
def app_logout():
    token = request.headers['access-token']
    response = logout(token)
    return respondOk('Successfully Logout');

@auth.route('/api/logout', methods=['GET'])
@api_login_required
def api_logout():
    token = request.headers['access-token']
    response = logout(token)
    return respondOk('Successfully Logout');