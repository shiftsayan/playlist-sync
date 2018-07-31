#########################
# Imports
#########################

import webbrowser, requests
from secrets import *

#########################
# Headers
#########################

params = (
    ('client_id', CLIENT_ID),
    ('response_type', 'code'),
    ('redirect_uri', REDIRECT_URI),
    ('scope', 'user-read-private playlist-modify-private playlist-read-private playlist-read-collaborative playlist-modify-public'),
)

#########################
# Requests
#########################

response = requests.get('https://accounts.spotify.com/authorize/', params=params)
webbrowser.open_new_tab(response.url)
