import json
from warnings import filters
from ytmusicapi import YTMusic
from colprint import print_success, print_error
from os.path import isfile
import toml
import sys

if isfile("config.toml"):
    with open('config.toml') as f:
        config = toml.load(f)
else:
    print_error("❌ No config.toml file found.")
    exit(0)


YTMusic.setup(filepath="headers_auth.json",
              headers_raw=config["ytmusic"]["headers"])
ytmusic = YTMusic("headers_auth.json")
print_success("✅ YT Music auth.")


if not isfile("my-songs.json"):
    print_error(
        "❌ No music file was found. Run spotify.py script to generate it first.")
    exit(0)

print_success("✅ Music file found.")
with open("my-songs.json", "r") as f:
    playlists = json.load(f)

interactive = "--interactive" in sys.argv

mode_music = "--songs" in sys.argv

print("-" * 50)
for playlist in playlists:
    p_id = ytmusic.create_playlist(
        title=playlist["name"], description=playlist["description"])
    print_success(f"✅ Created playlist {playlist['name']}")

    count = 0
    for song in playlist["songs"]:
        query = f"{song['title']} {song['artist']}"
        print(f"🔍 Searching for {query} songs...")
        search_results = ytmusic.search(query, filter=("songs" if mode_music else "videos"))
        if interactive:
            print(f"Are you looking for {search_results[0]['title']}?")
            if input().lower() not in ("", "y", "yes", "\n"):
                print_error(
                    f"❌ Song {song['title']} not found in YT Music. Skipping.")
                continue
        ytmusic.add_playlist_items(p_id, [search_results[0]["videoId"]])
        count += 1

    print_success(
        f"👍 Added {count} songs to playlist {playlist['name']}")
