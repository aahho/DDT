from flask import Flask
import jwt
from models import *
import helpers, requests
from app import app
from Exceptions.ExceptionHandler import DDTException
# from urllib.parse import urlencode

def filter_feed(request):
    qstr = request.query_string
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
