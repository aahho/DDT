# from google.oauth2 import id_token
# from google.auth.transport import requests as google_requests
from flask import redirect
from Exceptions.ExceptionHandler import DDTException
import requests, json, helpers
from app import app



# (Receive token by HTTPS POST)
# ...

# def authenticate_token(token):
#     return
#     print app
#     try:
#         idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), app.config['GOOGLE_CLIENT_ID'])

#         # Or, if multiple clients access the backend server:
#         # idinfo = id_token.verify_oauth2_token(token, requests.Request())
#         # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#         #     raise ValueError('Could not verify audience.')

#         if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#             raise ValueError('Wrong issuer.')

#         # If auth request is from a G Suite domain:
#         # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#         #     raise ValueError('Wrong hosted domain.')

#         # ID token is valid. Get the user's Google Account ID from the decoded token.
#         userid = idinfo['sub']
#     except ValueError:
#         raise DDTException("invalid google auth token")
def googleDefaults():
    default = {}
    default['token_request_uri'] = "https://accounts.google.com/o/oauth2/auth"
    default['response_type'] = "code"
    default['user_redirect_uri'] = helpers.get_local_server_url()+"/app/auth?provider=google"
    # default['user_activation_redirect_uri'] = "/user/activate/authcallback"
    default['scope'] = "email"
    default['login_failed_url'] = '/'
    default['access_token_uri'] = 'https://accounts.google.com/o/oauth2/token'
    default['grant_type'] = 'authorization_code'
    return default


def redirectTo():
    url = "{token_request_uri}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}".format(
        token_request_uri = googleDefaults()['token_request_uri'],
        response_type = googleDefaults()['response_type'],
        client_id = app.config['GOOGLE_CLIENT_ID'],
        redirect_uri = googleDefaults()['user_redirect_uri'],
        scope = googleDefaults()['scope']
        )
    return redirect(url)

# To Authorize the user with google signin
def authorize(request):
    print request.args.get('code')
    # parser = Http()
    params = {
        'code':request.args.get('code'),
        'redirect_uri': googleDefaults()['user_redirect_uri'],
        'client_id': app.config['GOOGLE_CLIENT_ID'],
        'client_secret': app.config['GOOGLE_CLIENT_SECRET'],
        'grant_type': googleDefaults()['grant_type']
    }
    # print params
    # headers={'content-type':'application/x-www-form-urlencoded'}
    # print googleDefaults()
    resp = requests.post(googleDefaults()['access_token_uri'], data=params)
    token_data = resp.json()
    return token_data['access_token']
    # resp, content = parser.request("https://www.googleapis.com/oauth2/v1/userinfo?access_token={accessToken}".format(accessToken=))
    # return content

def get_user_details(token):
    headers = {
        'Authorization': 'Bearer '+token
    }
    user_info = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', headers=headers)
    user_info = json.loads(user_info.content)
    if 'email' not in user_info:
        raise DDTException("invalid google auth token")
    return create_user_data(user_info)

def create_user_data(user_info):
    if user_info['verified_email'] is not True:
        raise DDTException('Email is not verified')
    return {
        'email' : user_info['email'],
        'display_name' : user_info['email'].split('@')[0],
        'first_name' : user_info['name'].split(' ')[0],
        'last_name' : user_info['family_name'],
    }