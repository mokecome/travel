from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.models import  FlexSendMessage
from linebot import LineBotApi
from deepfra import get_route,get_location_destination,Accessible_travel,generate_summary
from extra import get_one_json,travel_json
from linebot.models import  TextSendMessage
import json
from PIL import Image
import random
import parsel
import sys
import configparser
#Config Parser
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)

channel_access_token = config['Line']['CHANNEL_ACCESS_TOKEN']
channel_secret = config['Line']['CHANNEL_SECRET']
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

handler = WebhookHandler(channel_secret)

configuration = Configuration(
    access_token=channel_access_token
)

import re
import os
import requests
def get_img_files(dec):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    img_url='https://travel.yam.com/find/{}'.format(dec)
    response1 = requests.get(url=img_url, headers=headers)
    html_data1 = response1.text
    selector1 = parsel.Selector(html_data1)
    title= selector1.css('div.article_list_box_info h3 a::text').get()
    title_url= selector1.css('div.article_list_box a::attr(href)').get()
    img_url= selector1.css('div.article_list_box a img::attr(src)').get()
    
    
    # url='https://www.taiwan.net.tw/m1.aspx?sNo=0000064&keyString={}'.format(dec)
    # response = requests.get(url=url, headers=headers)
    # html_data = response.text
    # selector = parsel.Selector(html_data)
    # lis = selector.css('ul.grid div.card-wrap')
    # titles=[]
    #img_urls=[]
    # tag1_urls=[]
    # for li in lis:
    #   tag1_url ='https://www.taiwan.net.tw/'+li.css('a::attr(href)').get()
    #   title =li.css('a::attr(title)').get()
    #   #img_url =li.css('a div.graphic img::attr(data-src)').get()
    #   titles.append(title)
    #   #img_urls.append(img_url)
    #   tag1_urls.append(tag1_url)
    return title,img_url,'https://travel.yam.com/'+title_url
def extract_time(text):
    pattern = r'\[(.*?)\]'
    result = re.findall(pattern, text)
    if result:
        for match in result:
            print(match)
    else:
        print("No matches found.")
    return result
def extract_spend(text):
    pattern = r'\|(.*?)\|'
    result = re.findall(pattern, text)
    if result:
        return [time.strip() for time in result]
    else:
        return []

def all_spend(text):
    pattern = r'總共花費時間:(.*?)\n'
    result = re.findall(pattern, text)
    if result:
        return [route.strip() for route in result]
    else:
        return []
def add_json(data):
    flex_message = {
        "type": "carousel",
        "contents": data
    }
    return flex_message

# 保存消息到文件
def save_message(user_id, message):
    with open(f'./travel_data/{user_id}_message_records.txt', 'a+') as f:
        f.write(f"{message}\n")
# 读取消息记录
def get_recent_messages(user_id):
    try:
        with open(f'./travel_data/{user_id}_message_records.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) >= 5 :
              lines=lines[-5:]
            line_data=','.join(lines).replace('\n','').replace(',,',',').replace('?,',',')
            return line_data
    except FileNotFoundError:
        return []
app = Flask(__name__)
line_bot_api=LineBotApi('8ihzltg+k6o4M2scisl9FO12/+uLGy4rTt0AKE+IJEopWcyd+W99gGHguYradgaBDsjJtFCs75P4EC7C7pQiWyph9w6Dyto03UMBYv+tLXLUAkWAs4jJ11quHcSMCA7fqP5158+pmLgifcWfL523ygdB04t89/1O/w1cDnyilFU=')

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    line_bot_api=LineBotApi('8ihzltg+k6o4M2scisl9FO12/+uLGy4rTt0AKE+IJEopWcyd+W99gGHguYradgaBDsjJtFCs75P4EC7C7pQiWyph9w6Dyto03UMBYv+tLXLUAkWAs4jJ11quHcSMCA7fqP5158+pmLgifcWfL523ygdB04t89/1O/w1cDnyilFU=')
    line_bot_api.push_message('Ufd1b922dbd4129f78b659d3aefbc88fd', TextSendMessage(text='你好,我是無障礙旅遊小助手,請問有想去的地方嗎?'))
    user_id = event.source.user_id
    messages=get_recent_messages(user_id)
    messages=generate_summary(messages)
    print(messages)
    if event.message.text=='#景點直達#':
        text=get_location_destination(messages)
        route_info = get_route(text)
        flex_message = get_one_json(extract_time(route_info), route_info.split('整體路徑:')[1].split(','), extract_spend(route_info), all_spend(route_info)) 
        #flex_message=json.dumps(flex_message)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="景點直達", contents=flex_message))
        with open(f'./travel_data/{user_id}_message_records.txt', 'w') as f:
            f.write('')
    elif event.message.text=='#行程規劃#':
          text=get_location_destination(messages)
          save_message(user_id, text)
          if ('所在地' in text) and ('目的地' in text):
              answer=Accessible_travel(text)
              print(text.split('目的地:')[1])
              flex_travel=travel_json(text.split('目的地:')[1],answer)
              #flex_travel = add_json(flex_travel)
              line_bot_api.reply_message(event.reply_token,FlexSendMessage(alt_text="行程規劃",contents=flex_travel))
    elif event.message.text=='#地圖導航#':
        text=''
    else:   
            text=get_location_destination(messages)
            save_message(user_id, text)
            if ('所在地:' in text) and ('目的地:' in text):
               answer=Accessible_travel(text)
               print(answer)
               line_bot_api.reply_message(event.reply_token, TextSendMessage(text=answer))
            # Clear the message records file
               #with open(f'./travel_data/{user_id}_message_records.txt', 'w') as f:
               #    f.write('')
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
if __name__ == "__main__":
    app.run()
    '''
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
    '''
    





