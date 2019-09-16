"""LINE Push"""
import json
import requests

# HTTPヘッダを設定
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + 'yjwadTK19ssEogEdXIeZeA9uDNwevf26nSNp+RCCzNbhReTfxHwwv2SFfvGZUm9s9N7QLIAQpvsm9Og6WiEBt2j0eMS0hrF7aWVkrm4kdkWeEf/vVwozldqiSSRVPx4u3W7NfHDW9Oh2ollWA3NdpQdB04t89/1O/w1cDnyilFU=',
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
