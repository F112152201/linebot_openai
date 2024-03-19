from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

app = Flask(__name__)
line_bot_api = LineBotApi('ohPtukAyth3Ezhj9G+Wf9r4WLN9Rz5/eMy81wLAaFLal6AjsNYL9pnLnNTf1Gw+L3A/dBMsBker1Pr7EiUljmO71nFezzwOcCBKZaxsl2on6xAk6aM6GpRWOU/ebYyG21vNafTmRQK0+aeWY5QTpfQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c6904e9e43fdf904980c6ba5ac4a3155')

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text1 = event.message.text
    user_profile = {
        "occupation": "teacher",
        "ability": "teach"
    }
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": text1},
            {"role": "system", "content": user_profile}
        ],
        model="gpt-3.5-turbo-0125",
        temperature=0.5,
    )
    try:
        ret = response['choices'][0]['message']['content'].strip()
    except:
        ret = '發生錯誤！'
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ret))

if __name__ == '__main__':
    app.run()
