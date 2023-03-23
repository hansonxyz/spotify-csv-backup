# Spotify Playlist Backup and Restore

This repository contains two Python scripts, `spotify-get.py` and `spotify-set.py`, which allow you to back up and restore your Spotify playlists using CSV files.

## Prerequisites

- Python 3.x
- `spotipy` library

## Installation

1. Clone this repository:

`git clone https://github.com/hansonxyz/spotify-csv-editor.git`
`cd spotify-csv-editor`

2. Install the `spotipy` library:

`pip install spotipy`

3. Setup a API project in the Spotify developer console, and add `http://localhost/"` as a redirect uri in the app.

4. Create a `credentials.json` file in the repository's root directory with your Spotify API credentials.  Replace the placeholders with your actual credentials:

`
{
  "client_id": "your_client_id",
  "client_secret": "your_client_secret",
  "redirect_uri": "http://localhost/",
  "username": "your_spotify_username"
}
`

## Usage

Run spotify-get.py to export your Spotify playlists as CSV files:

`python spotify-get.py`

This will create a CSV file for each playlist in the playlists directory.

To restore a playlist from a CSV file, run spotify-set.py with the path to the CSV file as an argument:

`python spotify-set.py /path/to/your/csv_file.csv`

Replace /path/to/your/csv_file.csv with the actual path to the CSV file.

## Notes

Make sure to follow the Spotify API guidelines and comply with their terms of service when using these scripts.  If you encounter any issues or have suggestions, feel free to open an issue on this repository.
