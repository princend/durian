import random
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import tempfile, os
from config import client_id, client_secret, fgoAlbum_id, access_token, refresh_token, line_channel_access_token, \
    line_channel_secret, gmAlbum_id, clientDrawList, clientEatList, clientDoList, clientGmList, entertainmentList, \
    foodAlbum_id

app = Flask(__name__)

line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


@handler.add(MessageEvent, message=(ImageMessage, TextMessage))
def handle_message(event):
    """if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            config = {
                'album': album_id,
                'name': 'Catastrophe!',
                'title': 'Catastrophe!',
                'description': 'Cute kitten being cute on '
            }
            path = os.path.join('static', 'tmp', dist_name)
            client.upload_from_path(path, config=config, anon=False)
            os.remove(path)
            print(path)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳成功'))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
        return 0

    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    el"""
    if isinstance(event.message, TextMessage):
        clientText = event.message.text

        #Draw
        for i in clientDrawList:
            if clientText == i:
                client = ImgurClient(client_id, client_secret)
                images = client.get_album_images(fgoAlbum_id)
                index = random.randint(0, len(images) - 1)
                url = images[index].link
                image_message = ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
                line_bot_api.reply_message(
                    event.reply_token, image_message)
                return 0

        #What to eat
        for i in clientEatList:
            if clientText == i:
                client = ImgurClient(client_id, client_secret)
                images = client.get_album_images(foodAlbum_id)
                index = random.randint(0, len(images) - 1)
                url = images[index].link
                image_message = ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
                line_bot_api.reply_message(
                    event.reply_token, image_message)
                return 0

        #What to do
        for i in clientDoList:
            if clientText == i:
                index = random.randint(0, len(entertainmentList) - 1)
                text = entertainmentList[index]
                line_bot_api.reply_message(event.reply_token, [TextSendMessage(text = text)])
                return 0

        #Good morning
        for i in clientGmList:
            if clientText == i:
                client = ImgurClient(client_id, client_secret)
                images = client.get_album_images(gmAlbum_id)
                index = random.randint(0, len(images) - 1)
                url = images[index].link
                image_message = ImageSendMessage(
                    original_content_url=url,
                    preview_image_url=url
                )
                line_bot_api.reply_message(
                    event.reply_token, image_message)
                return 0

                #upload 
                        ext = 'jpg'
        message_content = line_bot_api.get_message_content(event.message.id)
        with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
            for chunk in message_content.iter_content():
                tf.write(chunk)
            tempfile_path = tf.name

        dist_path = tempfile_path + '.' + ext
        dist_name = os.path.basename(dist_path)
        os.rename(tempfile_path, dist_path)
        try:
            client = ImgurClient(client_id, client_secret, access_token, refresh_token)
            config = {
                'album': album_id,
                'name': 'Catastrophe!',
                'title': 'Catastrophe!',
                'description': 'Cute kitten being cute on '
            }
            path = os.path.join('static', 'tmp', dist_name)
            client.upload_from_path(path, config=config, anon=False)
            os.remove(path)
            print(path)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳成功'))
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='上傳失敗'))
        return 0

    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'

        return 0

        """if event.message.text == "抽卡" or event.message.text == "抽":
            client = ImgurClient(client_id, client_secret)
            images = client.get_album_images(album_id)
            index = random.randint(0, len(images) - 1)
            url = images[index].link
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )
            line_bot_api.reply_message(
                event.reply_token, image_message)
            return 0
        elif event.message.text == "吃什麼":
            index = random.randint(0, len(foodList) - 1)
            text = foodList[index]
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text = text)
                ])
            return 0
        elif event.message.text == "要乾麻":
            index = random.randint(0, len(entertainmentList) - 1)
            text = entertainmentList[index]
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text = text)
                ])
            return 0
        else:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=' yoyo'),
                    TextSendMessage(text='請傳一張圖片給我')
                ])
            return 0"""


if __name__ == '__main__':
    app.run()
