#########################
# Imports
#########################

from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import bs4, requests, json
from secrets import *

#########################
# Headers
#########################

headers = {
    'Authorization': 'Bearer ' + ACCESS_TOKEN,
}

#########################
# Helper Functions
#########################

def get_tracks(url):
    # Parse Webpage
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    data = json.loads(soup.find(id="shoebox-ember-data-store").get_text())

    name = data['data']['attributes']['name']
    playlist = data['included']

    # Get Track Names and Artists from Playlist
    tracks = []

    for track in playlist:
        try:
            tracks.append({
                            'name': track['attributes']['name'],
                            'artist': track['attributes']['artistName']
                         })
        except:
            continue

    return name, tracks

def get_spotify_playlist(target_name):
    # Get All Playlists
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    playlists = json.loads(response.text)['items']

    target_id = None

    # Search for Playlist in Existing Playlists
    for playlist in playlists:
        if str(playlist['name']) == target_name:
            target_id = str(playlist['id'])

    # Create Playlist if it DNE
    if target_id == None:
        response = requests.post('https://api.spotify.com/v1/users/%s/playlists' % USER_ID, headers=headers, data='{"name":"%s","public":false}' % target_name)
        target_id = str(json.loads(response.text)['id'])

    return target_id

def get_spotify_playlist_tracks(target_id):
    # Get All Teacks in Playlist
    response = requests.get("https://api.spotify.com/v1/users/%s/playlists/%s/tracks" % (USER_ID, target_id), headers=headers)
    playlist = json.loads(response.text)['items']

    # Get Track Names, Artists, and URIs from Playlist
    tracks = []

    for track in playlist:
        tracks.append({
                        'name': track['track']['name'],
                        'artist': track['track']['artists'][0]['name'],
                        'uri': track['track']['uri']
                     })

    return tracks

def get_spotify_track_uri(target_name, target_artist):
    # Parse Apple Music Song Name
    if "(feat." in target_name:
        index = target_name.find("(feat.")
        target_artist += target_name[index + len("(feat."):-1]
        target_name = target_name[:index]

    # Get Search Results
    params = (
        ('q', target_name),
        ('type', 'track'),
    )
    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    results = json.loads(response.text)['tracks']['items']

    # Return Best Fuzzy Match
    scores = []
    factor = 1

    for track in results:
        result = ""
        for artist in track['artists']:
            result += artist['name'] + " "
        scores.append(fuzz.ratio(result.strip(), target_artist) * factor)
        factor -= 0.02

    return results[scores.index(max(scores))]['uri']

def delete_spotify_playlist_tracks(tracks, target_id):
    # Generate Data String
    uris = ""
    for track in tracks:
        uris += '{"uri":"' + str(track['uri']) + '"},'
    data = '{"tracks":[' + uris[:-1] + "]}"

    response = requests.delete('https://api.spotify.com/v1/users/%s/playlists/%s/tracks' % (USER_ID, target_id), headers=headers, data=data)

def add_spotify_playlist_tracks(tracks, target_id):
    # Support 100 Track Limit
    if len(tracks) > 100:
        add_spotify_playlist_tracks(tracks[:100], target_id)
        add_spotify_playlist_tracks(tracks[100:], target_id)

    # Search for Tracks on Spotify
    uris = ""
    for track in tracks:
        try:
            uris += get_spotify_track_uri(track['name'], track['artist']) + ","
        except:
            print("Couldn't add " + track['name'] + " by " + track['artist'])

    params = (
        ('uris', uris[:-1]),
    )

    response = requests.post('https://api.spotify.com/v1/users/%s/playlists/%s/tracks' % (USER_ID, target_id), headers=headers, params=params)


#########################
# Main Function
#########################

def ams(url):
    name, cur_tracks = get_tracks(url)
    target_id  = get_spotify_playlist(name)
    old_tracks = get_spotify_playlist_tracks(target_id)

    add_tracks = [ track for track in cur_tracks if track not in old_tracks ]
    del_tracks = [ track for track in old_tracks if track not in cur_tracks ]

    print("Syncing " + name + "...")
    delete_spotify_playlist_tracks(del_tracks, target_id)
    add_spotify_playlist_tracks(add_tracks, target_id)
