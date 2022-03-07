import json
import sys
import yandex_music
from yandex_music.utils.difference import Difference
from colprint import print_success, print_error
from os.path import isfile
import toml
import requests
import getpass


if isfile("config.toml"):
    with open("config.toml") as f:
        config = toml.load(f)
else:
    print_error("❌ No config.toml file found.")
    exit(0)


def generate_token():
    username = input("Login: ")
    password = getpass.getpass("Password: ")
    url = "https://oauth.yandex.com/token"
    client_id = "23cabbbdc6cd418abb4b39c32c41195d"
    client_secret = "53bc75238f0c4d08a118e51fe9203300"

    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password
    }

    response = requests.post(url, data=data)
    return response.json()["access_token"]


if __name__ == "__main__":
    if "yandex" not in config or "token" not in config["yandex"]:
        token = generate_token()
        if not token:
            print_error("❌ Failed to generate token.")
            exit(0)
        config["yandex"] = {"token": token}
        with open("config.toml", "w") as f:
            toml.dump(config, f)
        print_success("✅ Token generated and saved to config.toml")
    token = config["yandex"]["token"]
    client = yandex_music.Client(token).init()
    print_success(
        f"✅ Logged in to Yandex.Music as {client.me.account.display_name}")

    if not isfile("my-songs.json"):
        print_error(
            "❌ No music file was found. Run spotify.py script to generate it first.")
        exit(0)

    print_success("✅ Music file found.")
    with open("my-songs.json", "r") as f:
        playlists = json.load(f)

    uid = client.me.account.uid

    for playlist in playlists:
        p = client.users_playlists_create(
            playlist["name"],
            visibility=("public" if "--public" in sys.argv else "private"),
            user_id=uid
        )
        print_success(f"✅ Created playlist {playlist['name']}")

        diff = Difference()
        songs = []

        count = 0
        for song in playlist["songs"]:
            query = f"{song['title']} {song['artist']}"
            print(f"🔍 Searching for {query} songs...")
            search_results = client.search(query, type_="track")
            if not search_results['tracks'] or not search_results['tracks']['results']:
                print_error(
                    f"❌ Song {song['title']} not found in YT Music. Skipping.")
                continue
            song_id = str(search_results['tracks']['results'][0]['id'])
            album_id = str(search_results['tracks']
                           ['results'][0]['albums'][0]['id'])
            print_success(
                f"✅ Found https://music.yandex.ru/album/{album_id}/track/{song_id}")
            songs.append({'id': song_id, 'album_id': album_id})
            count += 1

        diff.add_insert(0, tracks=songs)
        client.users_playlists_change(p['uid'], diff.to_json(), 0)

        print_success(
            f"👍 Added {count} songs to playlist {playlist['name']}")
