#########################
# Imports
#########################

import requests, json, base64
from secrets import *

#########################
# Headers
#########################

headers = {
    'Authorization': "Basic " + str(base64.urlsafe_b64encode((CLIENT_ID + ':' + CLIENT_SECRET).encode())).decode()
}

data = [
  ('grant_type', 'authorization_code'),
  ('code', AUTHORIZATION_CODE),
  ('redirect_uri', REDIRECT_URI),
]

#########################
# Requests
#########################

response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
json = json.loads(response.text)

#########################
# Populating
#########################

f = open("secrets.py", 'r')
i = f.readlines()
o = ""
f.close()

for line in i:
    if line == "ACCESS_TOKEN = \"ACCESS_TOKEN\"\n":
        line = "ACCESS_TOKEN = \"%s\"\n" % json["access_token"]
    elif line == "REFRESH_TOKEN = \"REFRESH_TOKEN\"\n":
        line = "REFRESH_TOKEN = \"%s\"\n" % json["refresh_token"]
    o += line

f = open("secrets.py", 'w')
f.write(o)
f.close()
