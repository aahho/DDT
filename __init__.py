from flask import Flask, Blueprint, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from Exceptions.ExceptionHandler import DDTException
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('env.py')
db = SQLAlchemy(app)

from Http.routes import base
from Auth.routes import auth
from feedAction.routes import feed_action

app.register_blueprint(base)
app.register_blueprint(feed_action)
app.register_blueprint(auth)

# custome handler
@app.errorhandler(DDTException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response