from __init__ import app
import sys, requests, helpers
from app import app

server_url = helpers.get_local_server_url()+'/notify'
headers = {
    "app-token" : app.config['APP_TOKEN']
}
requests.get(server_url, headers=headers)