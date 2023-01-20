import spotipy
import requests
import datetime
import base64
import json
from spotipy.oauth2 import SpotifyClientCredentials
from secret import *

# with open("secret.txt") as f:
#     secret_ls = f.readlines()
#     cid = secret_ls[0][:-2]
#     secret = secret_ls[1]

#Authentication to Spotify API without specific user credentials
# client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
# sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

url = "https://accounts.spotify.com/api/token"
headers = {}
data = {}


#Endcode as Base64
message = f"{clientID}:{clientSecret}"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')



token_data = {
    'grant_type' : 'client_credentials'
}

token_header = {
    'Authorization' : "Basic " + base64_message #<base64 encoded cid:secret>
}

#Formal request for an access token from spotify
res = requests.post(url, headers=token_header, data=token_data)

#json object received from Spotify
responseObject = res.json()

# print(json.dumps(responseObject, indent=2))

#Extracting the actual access token from json object received from Spotify
accessToken = responseObject['access_token']


