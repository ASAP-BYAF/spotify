import os
import sys
from dotenv import load_dotenv

from scrape.get_songs import scrape_cdtv_ranking
from notion_api.add_song import add_song_func
from notion_api.if_exist_song import if_exist_song_func


def main():

    # cdtv のランキングデータを取得
    date, ranking = scrape_cdtv_ranking()

    # .env ファイルを読み込む
    load_dotenv()

    # 環境変数から API キーを取得
    NOTION_API_KEY = os.getenv("NOTION_KEY")
    NOTION_DB_ID = os.getenv("NOTION_DB_ID")

    n_new_song = 0
    # 曲が登録されているかを確認
    for entry in ranking:
        song = entry["song"]
        artist = entry["artist"]
        if_exist_song_flag = if_exist_song_func(song, artist, NOTION_API_KEY, NOTION_DB_ID)
        
        # 曲が存在しない場合は新規登録
        if not if_exist_song_flag:
            add_song_func(song, artist, date, NOTION_API_KEY, NOTION_DB_ID)
            print(f"{artist} - {song} have been added !!!")
            n_new_song += 1
        # else:
        #     print("Data already exists !!!")

    print(f"{n_new_song} new songs have been added.")

if __name__ == "__main__":
    main()