import re
import os
import csv
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

# Read credentials from credentials.json
with open("credentials.json", "r") as file:
    credentials = json.load(file)
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    redirect_uri = credentials['redirect_uri']
    username = credentials['username']

# Set up Spotify API authentication
scope = 'playlist-modify-private playlist-read-private'
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope)

# Check if token.json exists and load token from it
if os.path.exists("token.json"):
    with open("token.json", "r") as file:
        token_info = json.load(file)
else:
    auth_url = sp_oauth.get_authorize_url()
    print("Please visit this URL for authorization:")
    print(auth_url)

    response = input("Enter the URL you were redirected to: ")

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    # Save token to token.json
    with open("token.json", "w") as file:
        json.dump(token_info, file)

if token_info:
    sp = spotipy.Spotify(auth=token_info['access_token'], oauth_manager=sp_oauth)
    playlists = sp.user_playlists(username)

    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print(f'Exporting {playlist["name"]}')
            playlist_name = playlist['name']
            playlist_id = playlist['id']
            playlist_tracks = sp.playlist_tracks(playlist_id)

            # Filter out non-alphanumeric characters and dashes
            filtered_playlist_name = re.sub(r'[^a-zA-Z0-9-]', '', playlist_name)

            # Create the filename with the playlist ID and filtered playlist name
            filename = f'playlists/{playlist_id}-{filtered_playlist_name}.csv'

            # Create a CSV file for the playlist
            with open(filename, mode='w', encoding='utf-8', newline='') as csvfile:
                fieldnames = ['track_name', 'artist', 'album', 'track_uri', 'track_url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for item in playlist_tracks['items']:
                    track = item['track']
                    track_name = track['name']
                    artist = track['artists'][0]['name']
                    album = track['album']['name']
                    track_uri = track['uri']
                    track_url = track['external_urls']['spotify']

                    # Write track details to the CSV file
                    writer.writerow({'track_name': track_name, 'artist': artist, 'album': album, 'track_uri': track_uri, 'track_url': track_url})
else:
    print("Can't get token for", username)
