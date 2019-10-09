from flask import Flask, request, abort
import os

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

    req_message = event.message.text　#受け取ったメッセージを変数に入れようとしています。
    yoyaku = req_message.rstrip().split()

    #yoyakuリストに格納した情報をそれぞれの変数に代入しようとしています。
    yyk_name = yoyaku[0]
    yyk_date = yoyaku[1]
    yyk_num = yoyaku[2]
    yyk_var = yoyaku[3]　　#券種によって値段を算出しようとしています。
    if yyk_var == "一般":
        yyk_pay = 3000
    elif yyk_var == "高校生":
        yyk_pay = 1500
    elif yyk_var == "U25":
        yyk_pay = 2000
    yyk_payment = yyk_pay * int(yyk_num)

    txt_yoyaku = yyk_name + " 様  ご予約ありがとうございます。\n下記の内容でご予約を承りました。" \
                 + "お名前： " + yyk_name + "  " + yyk_date \
                 + " の回\n" + yyk_num + "名様  " + "合計 " + str(yyk_payment) + "円"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt_yoyaku))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
