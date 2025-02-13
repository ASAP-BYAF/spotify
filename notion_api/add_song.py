import requests

def add_song_func(song_name, artist_name, date, notion_api_key, notion_db_id):
    # API エンドポイント
    url = f"https://api.notion.com/v1/pages"

    # ヘッダーの設定
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # リクエストボディの設定
    data = {
	    "parent": { "database_id": f"{notion_db_id}" },
        "properties": {
            "Song": {
                "title": [
                {
                    "type": "text",
                    "text": {
                    "content": song_name
                    }
                }
                ]
            },
            "Artist": {
                "select": {
                    "name": artist_name
            }
            },
            "Check": {
                "checkbox": False
            },
            "Good": {
                "checkbox": False
            },
            "Date": {
                "date": {
                    "start": date
                }
            }
        }
    }

    # POST リクエストを送信
    requests.post(url, headers=headers, json=data)
    # response = requests.post(url, headers=headers, json=data)

    # レスポンスを表示
    # print(response.status_code)

    return


if __name__ == "__main__":

    import os
    from dotenv import load_dotenv

    # .env ファイルを読み込む
    load_dotenv()

    # 環境変数から API キーを取得
    NOTION_API_KEY = os.getenv("NOTION_KEY")
    NOTION_DB_ID = os.getenv("NOTION_DB_ID")

    add_song_func("DDD", "XL", "2021-02-12", NOTION_API_KEY, NOTION_DB_ID)