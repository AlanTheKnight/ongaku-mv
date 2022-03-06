from functools import reduce
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import toml
from colprint import print_error, print_success
from os.path import isfile


if isfile("config.toml"):
    with open('config.toml') as f:
        config = toml.load(f)
else:
    print_error("No config.toml file found")
    exit(0)

auth = SpotifyOAuth(client_id=config['spotify']['client_id'],
                    client_secret=config['spotify']['client_secret'],
                    redirect_uri='http://localhost:8888/callback',
                    scope=config['spotify']['scope'])

spotify = spotipy.Spotify(auth_manager=auth)
print_success("✅ Spotify auth")


def get_playlists():
    results = spotify.current_user_playlists(limit=50)
    playlists = results['items']
    while results['next']:
        results = spotify.next(results)
        playlists.extend(results['items'])
    return playlists


def get_playlist_songs(uid: str):
    results = spotify.playlist_items(uid)
    songs = list(map(get_song_info, results["items"]))
    while results["next"]:
        results = spotify.next(results)
        songs.extend(list(map(get_song_info, results["items"])))
    return songs


def get_song_info(record: dict):
    song = record["track"]
    return {
        "artist": reduce(lambda a, b: a + " " + b, (i["name"] for i in song["artists"])),
        "title": song["name"]
    }


if __name__ == '__main__':
    playlists = get_playlists()
    for i, playlist in enumerate(playlists):
        print(f"{i+1})", playlist['name'])

    selected = input("Select playlist(s): ")
    to_transfer = playlists if selected == "all" else list(
        map(lambda x: playlists[int(x) - 1], selected.split()))

    result = []

    for sp in to_transfer:
        cur = {
            "name": sp["name"],
            "description": sp["description"],
            "songs": get_playlist_songs(sp["id"]),
        }
        print_success(
            f"👍 Retrieved {len(cur['songs'])} song(s) from \"{cur['name']}\"")
        result.append(cur)

    with open("my-songs.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
