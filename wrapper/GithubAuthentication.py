from flask import redirect
import urlparse, requests
from app import app
import helpers, json
from Exceptions.ExceptionHandler import DDTException

def githubDefaults():
	default = {}
	default['token_request_uri'] = "https://github.com/login/oauth/authorize"
	default['user_redirect_uri'] = helpers.get_local_server_url()+"/app/auth?provider=github"
	default['login_failed_url'] = '/app/login'
	default['access_token_uri'] = 'https://github.com/login/oauth/access_token'
	return default

# To Redirect the user for facebook login
def redirectTo():
	url = "{token_request_uri}?client_id={client_id}&redirect_uri={redirect_uri}&scope=user:email".format(
		token_request_uri = githubDefaults()['token_request_uri'],
		client_id = app.config['GITHUB_CLIENT_ID'],
		redirect_uri = githubDefaults()['user_redirect_uri']
		)
	return redirect(url)

# To Authorize the user with facebook signin
def authorize(request):
	# code = request.args
	headers = {
		'accept' : 'application/json'
	}
	response = requests.post(githubDefaults()['access_token_uri'],
							data = {'client_id' : app.config['GITHUB_CLIENT_ID'],
                           'client_secret' : app.config['GITHUB_CLIENT_SECRET'],
                           'code' : request.args.get('code')},
                           headers=headers)
	print response.content
	return json.loads(response.content)['access_token']

def get_user_details(token):
	headers = {
		'accept' : 'application/json'
	}
	user_info = requests.get('https://api.github.com/user/emails?access_token='+token, headers=headers)
	print user_info
	user_info = json.loads(user_info.content)
	print user_info
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