from dotenv import load_dotenv
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from scrape.get_songs import scrape_cdtv_ranking
from spotify.add_song import add_song


def main():

    # cdtv のランキングデータを取得
    date, ranking = scrape_cdtv_ranking()

    # .env ファイルを読み込む
    load_dotenv()

    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
    SPOTIFY_PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")

    ## spotifyインスタンスを作成
    scope = "playlist-modify-public"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=scope
    ))

    n_new_song_spotify = 0
    new_songs = []

    for i, entry in enumerate(ranking, 1):
        song = entry["song"]
        artist = entry["artist"]

        # SPOTIFY に対する処理
        if_exist_in_spotify = add_song(sp, song, artist, SPOTIFY_PLAYLIST_ID)
        if if_exist_in_spotify:
            print(f"Added: Rank {i} --- Added to Spotify: {artist} - {song} !!!")
            n_new_song_spotify += 1
            new_songs.append((i, artist, song))

    print(f"{n_new_song_spotify} new songs have been added to spotify !!!")
    for i_song in new_songs:
        print(f"Rank {i_song[0]}: {i_song[1]} - {i_song[2]}")

if __name__ == "__main__":
    main()