from flask import Flask 
from App.Repository import store
from models import User, UserDetail
import helpers  
import datetime

def user_seeder():
    user_data = {
        'id': '1b3b4f40-2e7c-4a66-b1f1-0f19ff113369', 
        'display_name':'AahhoDev',
        'email' : 'aahhodev@aahho.com',
        'password' : helpers.hash_password('feedr123'),
        'created_at': datetime.datetime.now(),
        'is_god' : True,
        'is_active' : True,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
    }
    user_details = {
        'id' : helpers.generate_unique_code(),
        'user_id': '1b3b4f40-2e7c-4a66-b1f1-0f19ff113369', 
        'first_name':'AahhoDev',
        'last_name' : None,
        'created_at': datetime.datetime.now(),
        'updated_at': datetime.datetime.now(),
    }
    store(User, user_data)
    store(UserDetail, user_details)

