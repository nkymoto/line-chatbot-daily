"""LINE Push"""
import json
import requests

# HTTPヘッダを設定
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + 'GWH6fPLvGZ1heaQHZA6bS2v9Zpd2P0UL1RNM8zzEJKITucnXIak3m0S78dKcqflt29c8SJxTegKZkC/LHFhkmjAaCyOy70OumT9a+VXqniAX1aOtEIHHVz8PhVwMVjYrH5WRWBYMDD/Km4oaWv4f7AdB04t89/1O/w1cDnyilFU=',
}

# POSTデータを設定
POST = {
    'to': 'U475654098fd61a584d6ad5b4e052ef9a',
    'messages': [
        {
            'type': 'text',
            'text': 'hello world'
        }
    ]
}

# 実行
CH = 'https://api.line.me/v2/bot/message/push'
REQ = requests.post(CH, headers=HEADERS, data=json.dumps(POST))

# HTTPステータスが 200 だったら OK
print(REQ.status_code)
if REQ.status_code != 200:
    print(REQ.text)
