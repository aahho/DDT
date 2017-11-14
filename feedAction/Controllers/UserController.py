from flask import Flask 
from datetime import datetime
import models, helpers
from models import db
from  feedAction.UserRepository import UserRepository
from Exceptions.ExceptionHandler import DDTException
from feedAction.Controllers import FeedController

def save_article(user_id, article_id):
	# user = UserRepository().get_user_by_id(user_id)
	article = FeedController.get_article_data(article_id)
	if  len(article['data']) is not 0:
		try:
			user_article = models.UserArticle(
			id=helpers.generate_unique_code(),
			feed_article_title=article['data']['title'],
			user_id=user_id,
			feed_article_id=article['data']['id']
			)
			db.session.add(user_article)
			db.session.commit()
			return True
		except Exception as e:
			db.session.rollback()
			user_article = models.UserArticle().query.filter(\
			models.UserArticle.user_id==user_id, models.UserArticle.feed_article_id==article_id\
			).first()
			if user_article.deleted_at is not None:
				user_article.deleted_at = None
				db.session.commit()
				return True
			raise DDTException('Duplicate entry', 422)
	raise DDTException('Invalid user or article id', 422)

def remove_article(user_id, article_id):
	user_article = models.UserArticle().query.filter(\
		models.UserArticle.user_id==user_id, models.UserArticle.feed_article_id==article_id\
		).first()
	user_article.deleted_at=datetime.now()
	db.session.commit()
	return True

def add_user_article_categories(request, user_id):
	categories_id = request.json
	for cat_id in categories_id:
		category = FeedController.get_category_by_id(cat_id).json()
		try:
			user_article_category = models.UserArticleCategory(
			id=helpers.generate_unique_code(),
			category_name=category['data']['name'],
			user_id=user_id,
			category_id=category['data']['id']
			)
			db.session.add(user_article_category)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			user_article_category = models.UserArticleCategory().query.filter(\
			models.UserArticleCategory.user_id==user_id, models.UserArticleCategory.category_id==cat_id\
			).first()
			if not user_article_category :
				raise DDTException('Something went wrong')
			elif user_article_category.deleted_at is not None:
				user_article_category.deleted_at = None
				db.session.commit()
	return True

def update_user_article_categories(request, user_id):
	categories_id = request.json
	models.UserArticleCategory().query.filter(\
		models.UserArticleCategory.user_id==user_id).delete()
	# db.session.delete(user_article_categories)
	db.session.commit()
	for cat_id in categories_id:
		category = FeedController.get_category_by_id(cat_id).json()
		try :
			user_article_category = models.UserArticleCategory(
			id=helpers.generate_unique_code(),
			category_name=category['data']['name'],
			user_id=user_id,
			category_id=category['data']['id']
			)
			db.session.add(user_article_category)
			db.session.commit()
		except :
			raise DDTException('Something Went Worng')
	return True		

def article_list(user_id):
	user = UserRepository().get_user_by_id(user_id)
	if user is not None:
		return user.transformed_articles()
	raise DDTException('Invalid User', 422)

def archived_article_list(user_id):
	user = UserRepository().get_user_by_id(user_id)
	if user is not None:
		return user.transformed_archived_articles()
	raise DDTException('Invalid User', 422)
	