import requests

def if_exist_song_func(song_name, artist_name, notion_api_key, notion_db_id):
    """曲が登録されているかを調べます

    Args:
        song_name (str): 曲名
        artist_name (str): アーティスト名
        notion_api_key (str): インテグレーションの key
        notion_db_id (str): データベース ID

    Returns:
        bool: データが存在するかの真偽値
    """
    # API エンドポイント
    url = f"https://api.notion.com/v1/databases/{notion_db_id}/query"

    # ヘッダーの設定
    headers = {
        "Authorization": f"Bearer {notion_api_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    # リクエストボディの設定
    data = {
        "filter": {
            "and": [
                {
                    "property": "Song",
                    "rich_text": {
                    "contains": song_name
                    }
                }, 
                {
                    "property": "Artist",
                    "select": {
                        "equals": artist_name
                    }
                }
            ]
        }
    }

    # POST リクエストを送信
    response = requests.post(url, headers=headers, json=data)

    # レスポンスを表示
    # print(response.status_code)

    # レスポンスの JSON を取得
    response_data = response.json()

    # "results" 配列の長さを計算
    results_length = len(response_data.get("results", []))

    if results_length > 0:
        return True
    else:
        return False

if __name__ == "__main__":

    import os
    from dotenv import load_dotenv

    # .env ファイルを読み込む
    load_dotenv()

    # 環境変数から API キーを取得
    NOTION_API_KEY = os.getenv("NOTION_KEY")
    NOTION_DB_ID = os.getenv("NOTION_DB_ID")

    res = if_exist_song_func("BBB", "M", NOTION_API_KEY, NOTION_DB_ID)
    print(res)

    res = if_exist_song_func("DDD", "XL", NOTION_API_KEY, NOTION_DB_ID)
    print(res)