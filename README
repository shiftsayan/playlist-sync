# Playlist Sync

These Python scripts and accompanying Spotify application sync my latest Apple Music playlists with my Spotify playlists so my weeb friends can enjoy my 🔥 music taste.

### Dependancies
* `webbrowser`
* `requests`
* `json`
* `base64`
* `bs4`
* `fuzzywuzzy`

### Use
1. Creating the Spotify App
  * Go to [the Spotify developer dashboard](https://developer.spotify.com/dashboard/) and log into your Spotify account
  * Use a meaningful name and description for the app
  * Click on *Edit Settings* and add `http://localhost:8000` to *Redirect URIs*
  * Copy your username and client credentials into `secrets.py`
2. Getting the Authorization Code
  * Spin up a local server using `python -m SimpleHTTPServer`
  * Run `python auth.py` from a separate Terminal window, which will open a new tab in your default browser
  * Copy the authorization code from the URL (`http://localhost:8000/?code=AUTHORIZATION_CODE`) of the new tab into `secrets.py`
3. Getting the Access and Refresh Tokens
  * Run `python access.py`, which automatically fetches the access and refresh codes and copies them into `secrets.py`
4. Manually Refreshing the Access and Refresh Tokens
  * Run `python refresh.py`, which automatically updates the access code and copies it into `secrets.py`
5. Syncing the Playlists
  * Copy the share URLs for all playlists you want to sync to `playlists.txt`
  * Run `python sync.py`, which automatically syncs your Apple Music and Spotify playlist to the best of a machine's ability

*NOTE:* You only need to generate the authorization code and access token once. On all subsequent calls to `sync.py`, the access token is automatically updated.

### Limitations

* Currently Spotify's API only supports getting a maximum of 100 tracks from a playlist. This will lead to sync issues with longer playlists.
* Spotify's search doesn't work with some song names (like `:) by LIL PHAG, MOD SUN & Dr. Woke`).
