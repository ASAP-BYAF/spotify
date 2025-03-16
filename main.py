from dotenv import load_dotenv
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from scrape.get_songs import scrape_cdtv_ranking
from notion_api.add_song import add_song_func
from notion_api.if_exist_song import if_exist_song_func
from spotify.add_song import add_song


def main():

    # cdtv のランキングデータを取得
    date, ranking = scrape_cdtv_ranking()

    # .env ファイルを読み込む
    load_dotenv()

    # 環境変数から API キーを取得
    NOTION_API_KEY = os.getenv("NOTION_KEY")
    NOTION_DB_ID = os.getenv("NOTION_DB_ID")

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

    # n_new_song_notion = 0
    n_new_song_spotify = 0

    # 曲が登録されているかを確認
    # for i, entry in enumerate(ranking[9:11], 1):
    for i, entry in enumerate(ranking, 1):
        song = entry["song"]
        artist = entry["artist"]

        # # NOTION DB に対する処理
        # if_exist_in_notion = if_exist_song_func(song, artist, NOTION_API_KEY, NOTION_DB_ID)
        
        # # 曲が存在しない場合は新規登録
        # if not if_exist_in_notion:
        #     add_song_func(song, artist, date, NOTION_API_KEY, NOTION_DB_ID)
        #     print(f"Added to Notion: {artist} - {song} !!!")
        #     n_new_song_notion += 1

        # SPOTIFY に対する処理
        if_exist_in_spotify = add_song(sp, song, artist, SPOTIFY_PLAYLIST_ID)
        if if_exist_in_spotify:
            print(f"Added: Rank {i} --- Added to Spotify: {artist} - {song} !!!")
            n_new_song_spotify += 1
        # else:
            # print(f"Rank {i} --- Already in Spotify: {artist} - {song} !!!")

    # print(f"{n_new_song_notion} new songs have been added to notion DB !!!")
    print(f"{n_new_song_spotify} new songs have been added to spotify !!!")

if __name__ == "__main__":
    main()