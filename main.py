#-*- coding: utf-8 -*-

from flask import Flask, request, abort
from elasticsearch import Elasticsearch
import os
import datetime
import time

# connect to the Elasticsearch cluster
elastic = Elasticsearch([{'host': '34.97.218.155', 'port': 9200}])

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, PostbackAction, TextMessage, TextSendMessage, TemplateSendMessage, 
    ButtonsTemplate, ConfirmTemplate, MessageTemplateAction
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

category = ""
am_pm = ""

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    if event.reply_token == "00000000000000000000000000000000":
        return

    if event.message.text == 'daily':
        button_template = TemplateSendMessage(
            alt_text='Button alt text',
            template=ButtonsTemplate(
                text="please select a category",
                title="daily input start",
                image_size="cover",
                thumbnail_image_url="https://www.actioned.com/wp-content/uploads/2018/03/daily-action-list.png",
                actions=[
                    PostbackAction(label='reading', data='1'),
                    PostbackAction(label='exercise', data='2'),
                    PostbackAction(label='coding', data='3'),
                    PostbackAction(label='english', data='4')
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token, button_template)
    elif (event.message.text.isdigit()):
        category_time = event.message.text
        dt_now = datetime.datetime.now()
        source_to_update = {
            "date" : dt_now.strftime('%Y-%m-%d'),
            "category" : int(category),
            "time" : int(category_time),
            "am_pm" : am_pm
        }

        index_id = dt_now.strftime('%Y%m%d') + category + am_pm
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

        time.sleep(1)
        result = elastic.search(
            index='daily',
            body={'query': {'match': {'date': dt_now.strftime('%Y-%m-%d')}}})
        hits = result['hits']['total']['value']
        result_hits = dt_now.strftime('%Y-%m-%d') + 'に登録した\r\n習慣数 : ' + str(hits)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=result_hits))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))

@handler.add(PostbackEvent)
def handle_button(event):
    print(event)
    global category
    global am_pm
    if event.postback.data in ["1","2","3","4"]:
        category = event.postback.data
        confirm_template = TemplateSendMessage(
            alt_text='Confirm alt text',
            template = ConfirmTemplate(
                text='please select am or pm?',
                actions=[
                    PostbackAction(label='AM', data='am'),
                    PostbackAction(label='PM', data='pm'),
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token, confirm_template)

    elif event.postback.data in ["am","pm"]:
        am_pm = event.postback.data
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='please input time'))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
