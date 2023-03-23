import sys
import os
import re
import csv
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def main():
    if len(sys.argv) != 2:
        print("Usage: python repopulate_playlist.py <csv_file>")
        sys.exit(1)

    csv_file = sys.argv[1]
    playlist_id = os.path.basename(csv_file).split('-')[0]

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
                            scope=scope,
                            username=username)

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

        # Clear playlist
        sp.user_playlist_replace_tracks(username, playlist_id, [])

        # Repopulate playlist
        uris = []
        with open(csv_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                uris.append(row['track_uri'])

        for i in range(0, len(uris), 100):
            sp.user_playlist_add_tracks(username, playlist_id, uris[i:i+100])

        print("Playlist repopulated successfully.")
    else:
        print("Can't get token for", username)

if __name__ == "__main__":
    main()  
