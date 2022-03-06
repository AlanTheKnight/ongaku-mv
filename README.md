# Ongaku-MV

Script that helps to move playlists from Spotify to YT Music

## Usage

Install Python & Poetry. Install requirements using Poetry.

Create new application in Spotify Developer Dashboard. Copy
client credentials and paste them to `config.toml`.

Open YT Music homepage in browser. Open dev panel using `Ctrl+Shift+I`. Go to network tab. Find HTTP request that starts with `browse?`. Copy request headers and paste them to `config.toml`.

```toml
[spotify]
client_id = ""
client_secret = ""
scope = "playlist-read-private"

[ytmusic]
headers = """

"""
```

First of all, retrieve your spotify playlists using

```poetry run python spotify.py```

To transfer music, run

```poetry run python yt.py```

If you don't want to see videos in your playlists, run

```poetry run python yt.py --songs```

If you want to select songs, run

```poetry run python yt.py --interactive```
