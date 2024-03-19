from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os


@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def handle_message(event):
    text1 = event.message.text
    user_profile = {
        "occupation": "professor",  # 將用戶的職業設定為 "教授"，可以根據需要修改這個值
        "ability": "Research"   # 將用戶的能力設定為 "研究"，可以根據需要修改這個值
    }
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": text1},
            {"role": "system", "content": user_profile}  # 將用戶資料添加到請求中
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
