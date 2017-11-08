from flask import Flask 
from datetime import datetime
import models, helpers
from models import db
from  feedAction.UserRepository import UserRepository
from feedAction.FeedRepository import FeedArticleRepository
from Exceptions.ExceptionHandler import DDTException
from feedAction.Controllers import FeedController

def save_article(user_id, article_id):
	user = UserRepository().get_user_by_id(user_id)
	article = FeedController.get_article_data(article_id)
	if user is not None and len(article['data']) is not 0:
		try:
			user_article = models.UserArticle(
			id=helpers.generate_unique_code(),
			feed_article_title=article['data']['title'],
			user_id=user.id,
			feed_article_id=article['data']['id']
			)
			db.session.add(user_article)
			db.session.commit()
			return True
		except Exception as e:
			db.session.rollback()
			# user_article = models.UserArticle().query.filter(\
			# models.UserArticle.user_id==user_id and modles.UserArticle.feed_article_id==article_id\
			# ).first()
			# print user_article.transform()
			# print user_article.saved_at, '------'
			# print user_article.id
			# if user_article.deleted_at is not None:
			# 	user_article.deleted_at = None
			# 	db.session.commit()
			# 	return True
			raise DDTException('Duplicate entry', 422)
	raise DDTException('Invalid user or article id', 422)

def remove_article(user_id, article_id):
	user = UserRepository().get_user_by_id(user_id)
	if user is not None:
		user_article = models.UserArticle().query.filter(\
			models.UserArticle.user_id==user_id and modles.UserArticle.feed_article_id==article_id\
			).first()
		user_article.deleted_at=datetime.now()
		db.session.commit()
		return True
	raise DDTException('Invalid user or article id', 422)

def article_list(user_id):
	user = UserRepository().get_user_by_id(user_id)
	if user is not None:
		return user.transformed_articles()
	raise DDTException('Invalid User', 422)