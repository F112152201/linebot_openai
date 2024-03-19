from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

app = Flask(__name__)


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
        "occupation": "professor",
        "ability": "Research"
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
