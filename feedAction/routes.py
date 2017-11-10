from flask import Flask, Blueprint, request, json, jsonify
from flask import render_template
from App.Response import *
import feedparser
from decorators import validate_jwt_token

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

@feed_action.route('/users/<user_id>/articles/<article_id>/save', methods = ['GET'])
@validate_jwt_token		
def save_article_for_user(user_id, article_id):
	response = UserController.save_article(user_id, article_id)
	if response:
		return respondOk('Saved Successfully')
	return respondWithError('Failed to save')

@feed_action.route('/users/<user_id>/articles/<article_id>/remove', methods = ['DELETE'])
@validate_jwt_token		
def remove_article_form_user(user_id, article_id):
	response = UserController.remove_article(user_id, article_id)
	if response:
		return respondOk('Removed Successfully')
	return respondWithError('Failed to remove')

@feed_action.route('/users/<user_id>/articles', methods = ['GET'])
@validate_jwt_token		
def list_of_save_article(user_id):
	response = UserController.article_list(user_id)
	return respondWithArray(response)

@feed_action.route('/users/<user_id>/articles/archived', methods = ['GET'])
@validate_jwt_token		
def list_of_archived_article(user_id):
	response = UserController.archived_article_list(user_id)
	return respondWithArray(response)

@feed_action.route('/feeds/keywords', methods = ['GET'])
@validate_jwt_token		
def kqywords():
	response = keyword_list(request)
	return respondWithArray(response['data'])