import os
import requests
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    if '我要' in get_message :
        line_bot_api.reply_message(event.reply_token,TextSendMessage("才不告訴你勒~~")    
    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
    
    url = 'https://notify-api.line.me/api/notify'
    token = 'xqH30BaWlOVwIj8JYd2uT6deJlp8FMJgHMkBMyOgA9j'
    headers = {
        'Authorization': 'Bearer ' + token    # 設定權杖
    }
    data = {
        'message':'測試一下！'     # 設定要發送的訊息
    }
    data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法
    
