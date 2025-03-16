from dotenv import load_dotenv
import os
import sys
import unicodedata

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def to_hankaku(text):
    return unicodedata.normalize('NFKC', text)

# 楽曲検索関数
def search_track(sp, song, artist):
    track_name = f"{song} {artist}"
    results = sp.search(q=track_name, limit=3, type="track")
    tracks = results.get("tracks", {}).get("items", [])
    
    if not tracks:
        print(f"No found: {track_name}: 検索結果が０件でした。")
        return None
    else:
        for track in tracks:
            search_song_hankaku = to_hankaku(song)
            found_song_hankaku = to_hankaku(track["name"])
            print(f"    検索条件: {search_song_hankaku}")
            print(f"    検索結果: {found_song_hankaku}")
            if search_song_hankaku.lower() in found_song_hankaku.lower():
                track_uri = track["uri"]  # Spotify URI
                return track_uri
            else:
                print(f"    {track_name}: 曲名が一致しませんでした。")

        print(f"No correspond: {track_name}: 該当する曲が見つかりませんでした。")
        return None


# プレイリスト内の曲を取得
def get_tracks_from_playlist(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    
    while results:
        tracks.extend(results['items'])
        # 次のページがあれば取得
        if results['next']:
            results = sp.next(results)
        else:
            break
    return tracks


# プレイリスト内で曲を検索
def search_in_playlist(sp, playlist_id, search_uri):
    tracks = get_tracks_from_playlist(sp, playlist_id)
    matching_tracks = []

    for item in tracks:
        track = item['track']
        uri = track['uri']

        if uri == search_uri:
            print(f"Already exist: {track['name']} は既にプレイリストに存在します。")
            return True
    return False

def add_song(sp, song, artist, playlist_id):

    # 楽曲検索
    track_uri = search_track(sp, song, artist)

    # プレイリスト内で検索を実行
    exist_in_playlist = search_in_playlist(sp, playlist_id, track_uri)

    # 取得した曲をプレイリストに追加
    if track_uri and not exist_in_playlist:
        # プレイリスト ID（Spotify の URL から取得）
        sp.playlist_add_items(playlist_id, [track_uri])

        return True
    else:
        return False


if __name__ == "__main__":
    song = "Daft Punk"
    artist = "Get Lucky"
    playlist_id = "3v1cYX1lIYQ8kHouZ2g3Z0"
    add_song(song, artist, playlist_id)