#-*- coding: utf-8 -*-

from flask import Flask, request, abort
from elasticsearch import Elasticsearch
import os
import datetime

# connect to the Elasticsearch cluster
elastic = Elasticsearch([{'host': '34.97.218.155', 'port': 9200}])

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.reply_token == "00000000000000000000000000000000":
        return

    req_message = event.message.text
    daily_data = req_message.rstrip().split()

    dt_now = datetime.datetime.now()
    source_to_update = {
        "date" : dt_now.strftime('%Y-%m-%d'),
        "category" : int(daily_data[0]),
        "time" : int(daily_data[1]),
        "am_pm" : daily_data[2] 
    } 

    index_id = dt_now.strftime('%Y%m%d') + daily_data[0] + daily_data[2]
    # catch API errors
    try:
        # call the Update method
        response = elastic.index(
            index='daily',
            id=index_id,
            body=source_to_update
        )

        # print the response to screen
        print (response, '\n\n')
        if response['result'] == "updated":
            print ("result:", response['result'])
            print ("Update was a success for ID:", response['_id'])
            print ("New data:", source_to_update)
        else:
            print ("result:", response['result'])
            print ("Response failed:", response['_shards']['failed'])
    except Exception as err:
        print ('Elasticsearch API error:', err)


    result = elastic.search(
             index='daily',
             body={'query': {'match': {'date': dt_now.strftime('%Y-%m-%d')}}})
    hits = result['hits']['total']['value']
    print('ヒット数 : %s' % hits)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=hits))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
