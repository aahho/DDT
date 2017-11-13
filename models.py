from flask import Flask, json, jsonify
from datetime import datetime, timedelta
from __init__ import db
from sqlalchemy import text, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import ARRAY, array
from helpers import datetime_to_epoch
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(100), primary_key=True)
    display_name = db.Column(db.String(70))
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(60))
    reset_pin = db.Column(db.SmallInteger, nullable=False, server_default=text("(0)::smallint"))
    is_banned = db.Column(db.Boolean, nullable=False, server_default=text("false"))
    is_god = db.Column(db.Boolean, nullable=False, server_default=text("false"))
    is_active = db.Column(db.Boolean, nullable=False, server_default=text("false"))
    confirmation_code = db.Column(db.String(255))
    last_login_location = db.Column(db.JSON)
    is_password_change_required = db.Column(db.Boolean, server_default=text("false"))
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    slack_id = db.Column(db.String(30))
    logo = db.Column(db.Text)
    is_premium_user = db.Column(db.Boolean, server_default=text("false"))

    articles = relationship(u'UserArticle')
    categories = relationship(u'UserArticleCategory')
    user_detail = relationship(u'UserDetail', uselist=False)

    def transformed_articles(self):
        user_articles = []
        for article in self.articles:
            if article.deleted_at is None:
                user_articles.append(article.transform())
        return user_articles

    def transformed_archived_articles(self):
        user_articles = []
        for article in self.articles:
            if article.deleted_at is not None:
                user_articles.append(article.transform())
        return user_articles
    
    def category_list(self):
        cat_list = []
        for cat in self.categories:
            cat_list.append(cat.transform())
        return cat_list

    def transform(self):
        return {
            'id' : self.id,
            'displayName' : self.display_name,
            'firstName' : self.user_detail.first_name,
            'lastName' : self.user_detail.last_name,
            'email' : self.email,
            'isGod' : self.is_god,
            'isBanned' : self.is_banned,
            'imageUrl' : self.logo,
            'isPremiumUser' : bool(self.is_premium_user),
            # 'articles' : self.transformed_articles(),
            # 'lastLoginLocation' : self.last_login_location
        }


class UserDetail(db.Model):
    __tablename__ = 'user_details'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.ForeignKey(u'users.id', ondelete=u'CASCADE'), nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    country = db.Column(db.String(40))
    state = db.Column(db.String(40))
    city = db.Column(db.String(40))
    mobile_number = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())
    location = db.Column(db.JSON)

    user = relationship(u'User')

def expires_at():
    return datetime.utcnow() + timedelta(days=7)

class UserToken(db.Model):
    __tablename__ = 'user_tokens'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.ForeignKey(u'users.id', ondelete=u'CASCADE'), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False,  default=expires_at)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=func.now(), onupdate=func.now())

    user = relationship(u'User')

    def transform(self):
        return {
            'id' : self.id,
            'token' : self.token,
            'expiresAt' : datetime_to_epoch(self.expires_at),
            'user' : self.user.transform()
        }

class UserArticle(db.Model):
    """docstring for UserArticle"""
    __tablename__ = 'user_articles'
    
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(u'users.id'))
    feed_article_id = db.Column(db.String)
    feed_article_title = db.Column(db.Text)
    saved_at = db.Column(db.DateTime, nullable=False, default=func.now())
    deleted_at = db.Column(db.DateTime)

    user = relationship("User", back_populates="articles")
    __table_args__ = (
        UniqueConstraint("user_id", "feed_article_id"),
    )

    def transform(self):
        return {
            'id' : self.id,
            'articleId' : self.feed_article_id,
            'title' : self.feed_article_title,
            'savedAt' : datetime_to_epoch(self.saved_at),
            'deletedAt' : datetime_to_epoch(self.deleted_at) if self.deleted_at is not None else None
        }

class UserArticleCategory(db.Model):
    """docstring for UserArticleCategory"""
    __tablename__ = 'user_article_categories'

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey(u'users.id'))
    category_id = db.Column(db.Integer)
    category_name = db.Column(db.String)
    saved_at = db.Column(db.DateTime, nullable=False, default=func.now())
    deleted_at = db.Column(db.DateTime)

    user = relationship("User", back_populates="categories")
    __table_args__ = (
        UniqueConstraint("user_id", "category_id"),
    )

    def transform(self):
        return {
            'id' : self.category_id,
            'name' : self.category_name,
            'savedAt' : datetime_to_epoch(self.saved_at),
            'deletedAt' : datetime_to_epoch(self.deleted_at) if self.deleted_at is not None else None
        } 
