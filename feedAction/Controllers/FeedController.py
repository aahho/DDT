from flask import Flask
import jwt
from models import *
import helpers, requests
from app import app
from Auth.AuthRepository import UserTokenRepository
from Exceptions.ExceptionHandler import DDTException

def filter_feed(request):
    type = request.args.get('type', None)
    qstr = request.query_string
    if type:
        category_ids = get_user_category(request)
        server_url = helpers.get_feedr_url()+'/feeds/articles/filter?'+qstr+'&category_id='+category_ids
    else :
        server_url = helpers.get_feedr_url()+'/feeds/articles/filter?'+qstr
    headers = {
        "app-token" : app.config['FEEDR_ACCESS_CODE']
    }
    response = requests.get(server_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else : 
        raise DDTException('Something went worng', 422)

def get_article_data(id):
    server_url = helpers.get_feedr_url()+'/feeds/articles/'+id
    headers = {
        "app-token" : app.config['FEEDR_ACCESS_CODE']
    }
    response = requests.get(server_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else : 
        raise DDTException('Something went worng', 422)

def get_user_category(request):
    category_ids = []
    if request.headers.has_key('access-token'):
        repo = UserTokenRepository()
        token = request.headers['access-token']
        tokenObj = repo.check_valid_token(UserToken, token)
        if hasattr(tokenObj, 'token'):
            categories = tokenObj.user.categories
            for cat in categories:
                category_ids.append(str(cat.category_id))
            return (",".join(category_ids))
        else:
            raise DDTException('Invalid user')
    else : 
        raise DDTException('Invalid user')

def keyword_list(request):
    server_url = helpers.get_feedr_url()+'/feeds/keywords'
    headers = {
        "app-token" : app.config['FEEDR_ACCESS_CODE']
    }
    response = requests.get(server_url, headers=headers)
    if response.status_code == 200:
        keys = response.json()['data']  
        if request.args.get('q') is not None:
            search_key = request.args.get('q')
            matching = [key for key in keys if search_key in key]
            return {'data' : matching}
        return {'data' : keys}
    else : 
        raise DDTException('Something went worng', 422)

def category_list(request):
    server_url = helpers.get_feedr_url()+'/feeds/categories'
    headers = {
        "app-token" : app.config['FEEDR_ACCESS_CODE']
    }
    response = requests.get(server_url, headers=headers)
    if response.status_code == 200:
        return response.json() 
        # if request.args.get('q') is not None:
        #     search_key = request.args.get('q')
        #     matching = [key for key in keys if search_key.lower() in key.lower()]
        #     return {'data' : matching}
        # return {'data' : keys}
    else : 
        raise DDTException('Something went worng', 422)

def get_category_by_id(id):
    server_url = helpers.get_feedr_url()+'/feeds/categories/'+ str(id)
    headers = {
        "app-token" : app.config['FEEDR_ACCESS_CODE']
    }
    response = requests.get(server_url, headers=headers)
    if response.status_code == 200:
        return response 
    raise DDTException('Invalid Category Id', 422)
