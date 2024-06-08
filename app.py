from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
import traceback
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


# 監聽所有來自 /callback 的 Post Request
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


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    questions_answers = {
        "日本大阪": "推薦景點：環球影城、心齋橋、黑門市場、天守閣、通天閣",
        "日本東京": "推薦景點：迪士尼樂園、晴空塔、淺草寺、 東京鐵塔、明治神宮",
        "日本北海道": "推薦景點：狸小路、小樽運河、富田農場、北海道神宮",
        "日本沖繩": "推薦景點：瀨長島、美麗海水族館、玉泉洞、美國村",
        "台灣台北": "推薦景點：臺北市立兒童新樂園、國立故宮博物院、華山文創、臺北101",
        "台灣新北": "推薦景點：野柳、金山、淡水老街、鶯歌老街、碧潭",
        "台灣基隆": "推薦景點：潮境公園、正濱漁港、和平島公園、八斗子",
        "台灣桃園": "推薦景點：大溪老街、Xpark、可口可樂世界、埔心牧場",
        "台灣新竹": "推薦景點：新竹都城隍廟、小叮噹科學園區、六福村、綠世界生態農場",
        "台灣苗栗": "推薦景點：龍騰斷橋、飛牛牧場、南庄老街、後龍好望角、白沙屯拱天宮、尚順育樂世界",
        "台灣台中": "推薦景點：高美濕地、國立自然科學博物館、宮原眼科、審計新村、秋紅谷",
        "台灣彰化": "推薦景點：鹿港老街、八卦山大佛風景區、臺灣玻璃館、溪湖糖廠、琉璃仙境休閒農場",
        "台灣雲林": "推薦景點：千巧谷牛樂園牧場、劍湖山、北港朝天宮、北港老街、青埔落羽松秘境",
        "台灣嘉義": "推薦景點：臺灣花磚博物館、阿里山森林鐵路車庫園區、森林之歌、愛木村地方文化館",
        "台灣南投": "推薦景點：台一生態休閒農場、清境農場、杉林溪、日月潭、日月老茶廠、忘憂森林",
        "台灣台南": "推薦景點：奇美博物館、藍晒圖文創園區、十鼓文創園區、神農街、安平老街",
        "台灣高雄": "推薦景點：駁二藝術特區、義大遊樂世界、高雄草衙、旗山老街、旗津星空隧道",
        "台灣屏東": "推薦景點：國立海洋生物博物館、六堆客家文化園區、大鵬灣國際休閒特區、小琉球",
        "台灣台東": "推薦景點：臺東海濱公園、初鹿牧場、紅葉谷綠能溫泉園區、知本國家森林遊樂區",
        "台灣花蓮": "推薦景點：遠雄海洋公園、海崖古、大石鼻山步道、月崖灣親子農場、九曲洞隧道",
        "台灣宜蘭": "推薦景點：斑比山丘、冬山河親水公園、清水地熱公園、積木博物館、湯圍溝溫泉公園",
        "韓國首爾": "推薦景點：樂天世界、星空圖書館、梨花女子大學、弘大街、明洞、東大門",
        "韓國釜山": "推薦景點：釜山水族館、BIFF廣場、松島天空步道、西面地下街、松島海上纜車",
        "韓國濟州島": "推薦景點：ECOLAND森林小火車、濟州東門市場、Mazeland迷宮公園、神話世界主題樂園",
    }
    
    if msg in questions_answers:
        #print(f"{english_word} 的中文翻譯是：{words_dict[english_word]}")
    
        line_bot_api.reply_message(event.reply_token, TextSendMessage(questions_answers[msg]))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))
       
         

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
