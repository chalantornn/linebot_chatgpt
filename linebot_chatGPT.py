from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "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"
model_use = "text-davinci-003"

channel_secret = "a2907ed7d5f0ef3245993dac090e628c"
channel_access_token = "KaQIlNy1mdJ4hIqfgtZiGpsw8WAKJmSpZo2szrCu5JzaluYnL8wZ299RQL9cPCdC3n7BU9C9/UkOKCm4ENWUcwYx88jTDtvGvz65gBAq8DvgTGkeM1iaxYDD9Qsr0ul29G534V0jvReuGemxQeJm4AdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

