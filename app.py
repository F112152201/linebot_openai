
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

    # 检查用户消息中是否包含关键词 "教师" 或 "老师"
    if "教师" in text1 or "老师" in text1 or "教学" in text1:
        # 将 LineBot 的身份设置为教师
        user_profile = {
            "role": "user",
            "content": "teach"
        }
    else:
        # 用户未指明身份或不是教师
        user_profile = {
            "role": "user",
            "content": "unknown"
        }

    # 发送消息到 OpenAI 进行处理
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", "content": text1},  # 用户的文本消息
            user_profile  # 用户角色信息
        ],
        temperature=0.5,
    )

    try:
        ret = response['choices'][0]['message']['content'].strip()
    except:
        ret = '发生错误！'

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ret))

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)

