from secret_codes import CLIENT_ID, CLIENT_SECRET
import os, json, requests

CLIENT_ID = os.environ['CLIENT_ID'] or CLIENT_ID
CLIENT_SECRET = os.environ['CLIENT_SECRET'] or CLIENT_SECRET

CALLBACK_URL = 'http://localhost:5000/'
SCOPE = ""
TOKEN_DATA = []

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''

def get_auth(client_id, redirect_uri, scope):
  """Generate Spotify Auth URL"""
  url = f"{SPOTIFY_URL_AUTH}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
  return url

def get_token(code, client_id, client_secret, redirect_uri):
  """"""
  body = {
    "grant_type": 'authorization_code',
    "code": code,
    "redirect_uri": redirect_uri,
    "client_id": client_id,
    "client_secret": client_secret
  }

  header = {"Content-Type": HEADER}

  post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=header)
  return handle_token(json.loads(post.text))

def handle_token(response):
  access_token = response['access_token']
  auth_head = {"Authorization": f"Bearer {access_token}"}
  REFRESH_TOKEN = response['refresh_token']
  return [access_token, auth_head, response['expires_in'], REFRESH_TOKEN]

def get_user_token(code):
  global TOKEN_DATA
  TOKEN_DATA = get_token(code, CLIENT_ID, CLIENT_SECRET, f"{CALLBACK_URL}/callback/")