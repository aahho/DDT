from flask import redirect
import oauth2 as oauth
import urlparse, requests
from app import app
import helpers, json
from Exceptions.ExceptionHandler import DDTException

def facebookDefaults():
	default = {}
	default['token_request_uri'] = "https://www.facebook.com/dialog/oauth"
	default['user_redirect_uri'] = helpers.get_local_server_url()+"/app/auth?provider=facebook"
	default['login_failed_url'] = '/user/login/facebook'
	default['access_token_uri'] = 'https://graph.facebook.com/oauth/access_token?'
	return default

# To Redirect the user for facebook login
def redirectTo():
	url = "{token_request_uri}?client_id={client_id}&redirect_uri={redirect_uri}&scope=email".format(
		token_request_uri = facebookDefaults()['token_request_uri'],
		client_id = app.config['FACEBOOK_CLIENT_ID'],
		redirect_uri = facebookDefaults()['user_redirect_uri']
		)
	return redirect(url)

# To Authorize the user with facebook signin
def authorize(request):
	consumer = oauth.Consumer(key=app.config['FACEBOOK_CLIENT_ID'], secret=app.config['FACEBOOK_CLIENT_SECRET'])
	client = oauth.Client(consumer)
	request_url = facebookDefaults()['access_token_uri'] + \
		'client_id=%s&redirect_uri=%s&client_secret=%s&code=%s' \
		% (app.config['FACEBOOK_CLIENT_ID'], facebookDefaults()['user_redirect_uri'], \
			app.config['FACEBOOK_CLIENT_SECRET'], request.args.get('code')) 
	resp, content = client.request(request_url, 'GET')
	return json.loads(content)['access_token']

def get_user_details(token):
    headers = {
        'Authorization': 'Bearer '+token
    }
    user_info = requests.get('https://graph.facebook.com/me?access_token=%s&scope=email&fields=id,name,email,picture' % token)
    user_info = json.loads(user_info.content)
    if 'email' not in user_info:
        raise DDTException("invalid facebook auth token")
    return create_user_data(user_info)

def create_user_data(user_info):
    return {
        'email' : user_info['email'],
        'display_name' : user_info['email'].split('@')[0],
        'first_name' : user_info['name'].split(' ')[0],
        'last_name' : user_info['name'].split(' ')[1:-1],
    }