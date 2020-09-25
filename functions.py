from flask import request
import random
import string
import base64
import requests
import time
def get_logins_spotify():
    CLIENT_ID = 'b45b68c4c7a0421589605adf1e1a7626'
    REDIRECT_URI="http://localhost:8080/s"
    scopes="user-library-read user-read-private"
    if request.method=="GET":
        return render_template('login.html')
    if request.method=="POST":
        url = "https://accounts.spotify.com/authorize?client_id={{spotify_client_id}}&response_type=code&redirect_uri=google.com"

        return redirect(f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&redirect_uri="+urllib.parse.quote(REDIRECT_URI.encode('utf-8'))+"&scope="+urllib.parse.quote(scopes.encode('utf-8'))+"&response_type=token")


"""
Creates a state key for the authorization request. State keys are used to make sure that
a response comes from the same place where the initial request was sent. This prevents attacks,
such as forgery. 
Returns: A state key (str) with a parameter specified size.
"""
def createStateKey(size):
	#https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))

"""
Requests an access token from the Spotify API. Only called if no refresh token for the
current user exists.
Returns: either [access token, refresh token, expiration time] or None if request failed
"""
def getToken(code):
    token_url = 'https://accounts.spotify.com/api/token'
    redirect_uri = "http://localhost:8080/callback"
    client_id = "b45b68c4c7a0421589605adf1e1a7626"
    client_secret = "9f629374960a45aa8268eab3a9dbe18b"
    encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    authorization = f"Basic {encodedData}"
    headers = {'Authorization': authorization, 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'code': code, 'redirect_uri': redirect_uri, 'grant_type': 'authorization_code'}
    post_response = requests.post(token_url, headers=headers, data=body)

    # 200 code indicates access token was properly granted
    if post_response.status_code == 200:
        json = post_response.json()
        return json['access_token'], json['refresh_token'], json['expires_in']
    else:
        logging.error('getToken:' + str(post_response.status_code))
        return None
"""
Requests an access token from the Spotify API with a refresh token. Only called if an access
token and refresh token were previously acquired.
Returns: either [access token, expiration time] or None if request failed
"""
def refreshToken(refresh_token):
    token_url = 'https://accounts.spotify.com/api/token'
    client_id = "b45b68c4c7a0421589605adf1e1a7626"
    client_secret = "9f629374960a45aa8268eab3a9dbe18b"
    encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    authorization = f"Basic {encodedData}"

    headers = {'Authorization': authorization, 'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
    post_response = requests.post(token_url, headers=headers, data=body)

    # 200 code indicates access token was properly granted
    if post_response.status_code == 200:
        return post_response.json()['access_token'], post_response.json()['expires_in']
    else:
        logging.error('refreshToken:' + str(post_response.status_code))
        return None


"""
Determines whether new access token has to be requested because time has expired on the 
old token. If the access token has expired, the token refresh function is called. 
Returns: None if error occured or 'Success' string if access token is okay
"""
def checkTokenStatus(session):
	if time.time() > session['token_expiration']:
		payload = refreshToken(session['refresh_token'])

		if payload != None:
			session['token'] = payload[0]
			session['token_expiration'] = time.time() + payload[1]
		else:
			logging.error('checkTokenStatus')
			return None

	return "Success"


"""
Makes a GET request with the proper headers. If the request succeeds, the json parsed
response is returned. If the request fails because the access token has expired, the
check token function is called to update the access token.
Returns: Parsed json response if request succeeds or None if request fails
"""
def makeGetRequest(session, url, params={}):
	headers = {"Authorization": "Bearer {}".format(session['token'])}
	response = requests.get(url, headers=headers, params=params)

	# 200 code indicates request was successful
	if response.status_code == 200:
		return response.json()

	# if a 401 error occurs, update the access token
	elif response.status_code == 401 and checkTokenStatus(session) != None:
		return makeGetRequest(session, url, params)
	else:
		logging.error('makeGetRequest:' + str(response.status_code))
		return None

"""
Gets user information such as username, user ID, and user location.
Returns: Json response of user information
"""
def getUserInformation(session):
	url = 'https://api.spotify.com/v1/me'
	payload = makeGetRequest(session, url)

	if payload == None:
		return None

	return payload

"""
Gets user saved albums
Returns: Json response of user information
"""
def getUserSavedAlbums(session):
	url = 'https://api.spotify.com/v1/me/albums'
	payload = makeGetRequest(session, url)
	if payload == None:
		return None
	return payload

def getBackGroundColors():
    url = "http://localhost:5000/colors?url=https://i.scdn.co/image/ab67616d0000b273e4057e4cece32c02e0f04883"
    response = requests.request("GET", url)
    return response.text
