# 🎵 Billboard to Spotify Bot  

A simple Python script that allows you to search for tracks on Spotify and add them to your playlists using the **Spotify Web API**.  
This project is built with [Spotipy](https://spotipy.readthedocs.io/) — a lightweight Python library for Spotify.  

---

## 🚀 Features  
- Authenticate with your Spotify account  
- Fetch your current playlists  
- Search for tracks by song title / artist  
- Add tracks to an existing playlist  
- Cache search results locally (so you don’t keep hitting Spotify’s API unnecessarily)(yet to be added  

---

## 🛠 Requirements  

- Python 3.8+  
- Spotify Developer Account (to create an app and get credentials)  
- A virtual environment is recommended  

---

## 📦 Installation  

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Create Env Variables in ".env"**
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://localhost:8888/callback

