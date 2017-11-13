from flask import Flask, Blueprint, request, json, jsonify
from flask import render_template
from App.Response import *
import feedparser
from decorators import validate_jwt_token, api_login_required

from Controllers.FeedController import *
from Controllers import UserController
from models import *

feed_action = Blueprint('feed_action', __name__, template_folder='templates')


@feed_action.route('/feeds/articles/filter', methods = ['GET'])
@validate_jwt_token
def filter():
	response = filter_feed(request)
	return respondWithPaginatedCollection(response['data'], response['meta']['pagination'])

@feed_action.route('/feeds/articles/<id>', methods = ['GET'])
@validate_jwt_token
def get_artical(id):
	response = get_article_data(id)
	return json.jsonify(response)

@feed_action.route('/articles/<article_id>/save', methods = ['GET'])
@validate_jwt_token	
@api_login_required	
def save_article_for_user(article_id):
	user_id = request.user.get('id')
	response = UserController.save_article(user_id, article_id)
	if response:
		return respondOk('Saved Successfully')
	return respondWithError('Failed to save')

@feed_action.route('/articles/<article_id>/remove', methods = ['DELETE'])
@validate_jwt_token	
@api_login_required	
def remove_article_form_user(article_id):
	user_id = request.user.get('id')
	response = UserController.remove_article(user_id, article_id)
	if response:
		return respondOk('Removed Successfully')
	return respondWithError('Failed to remove')

@feed_action.route('/categories', methods = ['POST'])
@validate_jwt_token	
@api_login_required	
def add_categories_from_user():	
	user_id = request.user.get('id')
	response = UserController.add_user_article_categories(request, user_id)
	if response:
		return respondOk('Added Successfully')

@feed_action.route('/categories/remove', methods = ['DELETE'])
@validate_jwt_token	
@api_login_required	
def remove_categories_froms_user():	
	user_id = request.user.get('id')
	response = UserController.remove_user_article_categories(request, user_id)
	if response:
		return respondOk('Removed Successfully')


@feed_action.route('/articles', methods = ['GET'])
@validate_jwt_token	
@api_login_required	
def list_of_save_article():
	user_id = request.user.get('id')
	response = UserController.article_list(user_id)
	return respondWithArray(response)

@feed_action.route('/articles/archived', methods = ['GET'])
@validate_jwt_token	
@api_login_required	
def list_of_archived_article():
	user_id = request.user.get('id')
	response = UserController.archived_article_list(user_id)
	return respondWithArray(response)

@feed_action.route('/feeds/keywords', methods = ['GET'])
@validate_jwt_token		
def kqywords():
	response = keyword_list(request)
	return respondWithArray(response['data'])

@feed_action.route('/feeds/categories', methods = ['GET'])
@validate_jwt_token		
def categories():
	response = category_list(request)
	return respondWithArray(response['data'])\

@feed_action.route('/users/categories', methods = ['GET'])
@validate_jwt_token		
@api_login_required	
def user_categories():
	user_id = request.user.get('id')
	response = user_category_list(user_id)
	return respondWithCollection(response)
