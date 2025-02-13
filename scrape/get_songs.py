import requests
from bs4 import BeautifulSoup


def scrape_cdtv_ranking():
    # スクレイピング対象のURL
    URL = "https://www.tbs.co.jp/cdtv_livelive/database/"

    # User-Agentを設定
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    # ページのHTMLを取得
    response = requests.get(URL, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    # エンコーディングを自動検出して適用
    response.encoding = response.apparent_encoding  # 文字化け防止

    # BeautifulSoup で HTML を解析
    soup = BeautifulSoup(response.text, "html.parser")

    # 日付を取得
    date_span = soup.select_one(".weekof .big")
    if date_span:
        date = date_span.text.strip().replace("/", "-")
    
    # ランキングデータを取得
    rankings = []
    for row in soup.select(".rank-tbl tr"):
        song_td = row.select_one(".rank-song a")
        artist_td = row.select_one(".rank-artist a")

        if song_td and artist_td:
            song = song_td.text.strip()
            artist = artist_td.text.strip()
            rankings.append({"song": song, "artist": artist})

    return date, rankings

if __name__ == "__main__":
    ranking_list = scrape_cdtv_ranking()
    if ranking_list:
        for rank, entry in enumerate(ranking_list, 1):
            print(f"{rank}. {entry['artist']} - {entry['song']}")
