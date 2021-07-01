from flask import Flask, request, abort, render_template
import random
import requests
import json
from linebot.models import *
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from utli.fireBase import dataBase
import utli.flexBuilder as flexBuilder
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)

db = dataBase()
app = Flask(__name__)


line_bot_api = LineBotApi('pIFhz9UF4l5rT4shGT0TPksC8bHDzKm7yUuqvvf5NqooQ3OIcR9iB6kaZ7/eXm64R/VGi83B717ISN4xeFRgQOwFUx+lNkNz6dgIbkweNlqnaFYts+XKlUy9KNGtPav2eNK9LC7GAqnMduvQTZc6YwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2bd83a025461a18b9b6bd1eb632b95d3')

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

@handler.add(PostbackEvent)
def handle_post_message(event):
    if event.postback.data == 'apple':
        print('OK')

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event)
    text = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)


    if (text == '看看目錄'):
        contents = []
        products = list(db.getProductData().values())
        for product in products:
            contents.append(flexBuilder.productList(product['name'], product['price'], product['img'], product['describe']))
        if len(contents) > 0:
            carouselContents = {
                "type" : "carousel",
                "contents" : contents
            }
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('商品目錄', carouselContents))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('目前沒有商品...'))
    #todo
    elif(text=="想下單"):
        carousel_template_message = TemplateSendMessage(
            alt_text='我想下單',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/DX0hJiE.png',
                        title='我想下單',
                        text='請點選想下單的品項類別',
                        actions=[
                            MessageAction(
                                label = '何奶奶手工辣椒醬',
                                text = '何奶奶手工蠟椒醬'
                            ), 
                            MessageAction(
                                label = '小何私心推薦',
                                text = '小何私心推薦'
                            ),

                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    elif(text=='何奶奶手工辣椒醬'):
        contents = []
        products = list(db.getProductData().values())
        for product in products:
            contents.append(flexBuilder.productList(product['name'], product['price'], product['img'], product['describe']))
        if len(contents) > 0:
            carouselContents = {
                "type" : "carousel",
                "contents" : contents
            }
            line_bot_api.reply_message(event.reply_token, FlexSendMessage('商品目錄', carouselContents))
    elif(text=='小何私心推薦'):
        line_bot_api.reply_message(event.reply_token, TextSendMessage('目前還沒有商品上架'))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage('請點選下方功能選單'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)