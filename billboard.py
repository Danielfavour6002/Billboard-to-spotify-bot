import requests
from bs4 import BeautifulSoup
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

#SCRAPE BILLBOARD HOT 100
date = input("What year do you want to create playlist for ? Enter date in this format YYYY-MM-D: ")
URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL).text

soup = BeautifulSoup(response, "html.parser")

# Find all chart items
chart_items = soup.select("li.o-chart-results-list__item")

songs = []
for item in chart_items:
    # Get song title
    title_elem = item.select_one("h3.c-title")
    title = title_elem.get_text(strip=True) if title_elem else None

    # Get artist (could be span or a)
    artist_elem = item.select_one("span.c-label, a")
    artist = artist_elem.get_text(strip=True) if artist_elem else None

    if title and artist:
        songs.append({"title": title, "artist": artist})


#SPOTIFY HANDLING
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

#spotify auth
spot = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, state=None, scope="playlist-modify-public playlist-modify-private"
,
    cache_path=".spotipy_cache"  , username=None, proxies=None, show_dialog=False, requests_session=True, requests_timeout=None, open_browser=True ))

#grab user id 
user_id = spot.me()["id"] 


#perform spotify search for song and artist
tracks = []
if not songs:
    print("couldn't find any result for the date you provided")
for song in songs:
    print(f"searching: {song["title"]} - {song["artist"]}")
    query = f"track:{song['title']} artist:{song['artist']}"
    results = spot.search(q=query, type='track' )
    if results["tracks"]["items"]:  # check if Spotify returned a match
        track = results["tracks"]["items"][0]["uri"]  # take the first match's URI
        tracks.append(track)
        print("track added")
        print(song["title"], "-", song["artist"])
    else:
        print("couldn't find any result")
print("search complete")

#get all user playlists
option = input("Do you want to add in existing playlist or new one. Type 'current' or 'new': ")
if option == "current":
    playlists = spot.current_user_playlists(limit=50)
    if not playlists:
        print("no playlist found")
    playlist_items = playlists["items"]
    playlist_id =  playlist_items[0]["id"]#change zero to the index of playlist you want to select
    added_tracks = spot.playlist_add_items(playlist_id=playlist_id, items=tracks)
    print(f"tracks added successfully")
else:
    #create new spotify playlist
    print("creating new playlist\ngenerating playlist id")
    playlist = spot.user_playlist_create(
        user=user_id,
        name=f"{date} Billboard Top 100",
        public=True,  
        description=  "playlist with top 100 songs!"
    )
    new_playlist_id = playlist["id"]
    added_tracks = spot.playlist_add_items(playlist_id=new_playlist_id, items=tracks)
    print(f"tracks added successfully")

