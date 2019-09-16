from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import random
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

def get_time():
    return str(datetime.now()).split(".")[0]

scheduler = BlockingScheduler()

random1 = random.randint(1,19)
random2 = random.randint(20,39)
random3 = random.randint(40,59)

def line_push():
    REQ = requests.post(CH, headers=HEADERS, data=json.dumps(POST))
    # HTTPステータスが 200 だったら OK
    print(REQ.status_code)
    if REQ.status_code != 200:
        print(REQ.text)

def random_1():
    print(get_time(), '|', '毎時{}分になると実行'.format(random1))
    line_push() 
scheduler.add_job(random_1, 'cron', minute=random1)

def random_2():
    print(get_time(), '|', '毎時{}分になると実行'.format(random2))
    line_push() 
scheduler.add_job(random_2, 'cron', minute=random2)

def random_3():
    print(get_time(), '|', '毎時{}分になると実行'.format(random3))
    line_push() 
scheduler.add_job(random_3, 'cron', minute=random3)

def main():
    try:
        scheduler.start()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
