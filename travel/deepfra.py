import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"#conda 和 torch包重複
import numpy as np
import generate_vector
import pickle
import json
import random
from langchain.memory import ChatMessageHistory
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain.memory import ConversationBufferMemory

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
#os.environ["DEEPINFRA_API_TOKEN"] = 'PLGfg2yhCSD6eP9uDTtiUQ7by8sQ2sHt'
#即時活動 即時API
#活動推薦RANDOM
import pdfplumber
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv
import pandas as pd
import time
time.strftime("%H:%M", time.localtime())
load_dotenv()


azure_openai_version = ""
# Azure Chat OpenAI
azure_openai_akp_key = ''
azure_openai_deployment = ""
azure_openai_endpoint = ""

client = AzureOpenAI(
    azure_endpoint=azure_openai_endpoint,
    api_key=azure_openai_akp_key,
    api_version=azure_openai_version,
)
def get_weather(loc):#城市位置名稱 即時天氣查詢 -> 地點查詢
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": loc,               
        "appid": '81c010f56d7fd75640f91cd4b1bffdf7',
        "units": "metric",            # 使用摄氏度而不是华氏度
        "lang":"zh_tw"                # 输出语言为繁體中文
    }
    response = requests.get(url, params=params)
    data = response.json()
    return json.dumps(data)

def generate_summary(text):
    message_text = [
        {"role": "system", "content": '''你是一個擅長總結 去重的助手。請將以下內容總結成30字內的結論。
                                         格式如下:
                                             所在地:
                                             目的地:
                                             '''},
        {"role": "user", "content": text}
    ]
    
    completion = client.chat.completions.create(
        model=azure_openai_deployment,
        messages=message_text,
        temperature=0.7,
        max_tokens=500,
        top_p=0.90,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    
    return completion.choices[0].message.content


def get_ref(user_prompt):
    with open("./travel_data/id_vector","rb") as f:
        index=pickle.load(f)
    with open("./travel_data/id_knowadge",encoding='utf-8') as f:
        id_know=json.load(f)
    vector=generate_vector.get_vector(user_prompt)
    vector=np.array([vector])
    D, I = index.search(vector,3)
    D=D[0]
    I=I[0]
    sentences=[]
    for d,i in zip(D,I):
        #距离过滤
        if d>0.02:
            continue
        sentences.append(id_know[str(i)]['target'])
    ref_prompt="請根据以下事實回答問题{}。問题是：{}".format("。".join(sentences),user_prompt)
    print(ref_prompt)
    #過濾filier
    return ref_prompt

def get_location_destination(response):
    df=pd.read_excel('./travel_data/travel_1.xlsx')['景點']
    df_str = df.to_string()
    system_prompt = """你善長規劃台灣的無障礙旅遊。對各地的交通路線極為熟悉，明確知道無障礙旅遊的客人應該前往那些景點，品嘗那些美食以及如何出行。
                       你的任務是了解用戶的所在地與目的地。
                       若用戶未提供所在地,則默認當前位置(若無法獲取,預設為南京東路3段),並告知用戶。
                       經過一次詢問若用戶未給予目的地,則依開放時間優先推薦地點,並告知用戶。
                       若有多個目的地,則採用最後告知的目的地。
                       當你獲得所在地與目的地後,會告知用戶所在地與目的地。不必解釋其他,格式如下:
                           我的所在地:南京東路3段
                           我的目地的:古亭站 
                    """#.format(df_str)
    messages= [
                {"role": "system", "content":system_prompt},
                {"role":"user","content":response}]
    completion = client.chat.completions.create(
            model="",  # 替換為你的部署名稱
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.90,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
    return completion.choices[0].message.content

def Accessible_travel(desc):
    response=get_ref(desc)
    
    system_prompt='''你善長規劃台灣的無障礙旅遊。你對於各地的交通路線也十分清楚，很清楚無障礙旅遊的客人應該去什麽景點，品嘗什麽美食以及如何出行。
                           當你知道你用戶的所在地與目的地,會給我起點到終點的一份旅遊指南。
                           
                           旅遊指南格式如下： 
                            🌳推薦的景點特色與相關無障礙設施 

                            🏞️即時的天氣環境信息
                                 今天天氣是23°C，降雨機率為10%，環境空氣品質指數AQI為97，屬於普通。

                            🚍交通指南
                              -自行開車：
                              
                              -大眾運輸：
                               1.板橋公車站前搭乘( 953 金山－板橋 )班車，於野柳地質公園站下車。      
                               2.淡水捷運站前搭乘 ( 862皇冠北海岸線 )班車，於野柳地質公園站下車。'''    
    messages= [
                {"role": "system", "content":system_prompt},
                {"role":"user","content":response}]
    completion = client.chat.completions.create(
            model="gpt4o-mokecome-0522",  # 替換為你的部署名稱
            messages=messages,
           temperature=0.7,
           max_tokens=1000,
           top_p=0.90,
           frequency_penalty=0,
           presence_penalty=0,
           stop=None
        )
    return completion.choices[0].message.content


def trip_planning(user_prompt):
    #對天氣更新
    user_prompt=get_ref(user_prompt)#獲取向量資料庫裡的資料  點即

    system='''你是一個十分高級完善的旅遊指南。你把台灣地圖牢記於心，你對於台灣出名的美食了如指掌，你對於各地的交通路線也十分清楚，你很清楚不同需求愛好的客人應該去什麽景點，品嘗什麽美食以及如何出行。
             當我告訴你我所在的地點和需求的時候，你會推薦一個靠近我的地方，並給我一份的旅遊指南。
             當我告訴你想要去的目的地時,你會推薦由{}至目的地的旅遊指南。
              旅遊指南格式如下： 
               🌳推薦的景點特色與相關無障礙設施 

               🏞️即時的天氣環境信息
                    今天天氣是23°C，降雨機率為10%，環境空氣品質指數AQI為97，屬於普通。
                🙅注意事項
                ❌可不必去蝴蝶泉和玫瑰庄园，行動不安便靠量安全
                ✅了解当地民风民俗，避免不必要的误会和麻烦

               🚍交通指南
                 -自行開車：
                 
                 -大眾運輸：
                  1.板橋公車站前搭乘( 953 金山－板橋 )班車，於野柳地質公園站下車。      
                  2.淡水捷運站前搭乘 ( 862皇冠北海岸線 )班車，於野柳地質公園站下車。
                 
            '''.format('台北')
    # completion = client.chat.completions.create(
    #     model=azure_openai_deployment,
    #     messages= [
    #                     {"role": "system", "content":system},
    #                     {"role":"user","content":user_prompt}],
    #     max_tokens=300,
    # )
    # return completion.choices[0].message.content  



#對該地點簡述  路線拆解(google api)
def get_route(result):
    MRT=['動物園站出口1', '動物園站出口2', '木柵站出口', '萬芳社區站出口', '萬芳醫院站出口', '辛亥站出口', '麟光站出口', '六張犁站出口', '科技大樓站出口', '中山國中站出口', '松山機場站出口1', '松山機場站出口2', '松山機場站出口3', '大直站出口1', '大直站出口3', '劍南路站出口1', '劍南路站出口2', '西湖站出口1', '西湖站出口2', '港墘站出口1', '港墘站出口2', '文德站出口1', '文德站出口2', '內湖站出口1', '內湖站出口2', '大湖公園站出口1', '大湖公園站出口2', '葫洲站出口1', '葫洲站出口2', '東湖站出口1', '東湖站出口2', '東湖站出口3', '南港軟體園區站出口1', '南港軟體園區站出口2', '中正紀念堂站出口1', '中正紀念堂站出口5', '台大醫院站出口1', '台大醫院站出口2', '台大醫院站出口3', '台北車站M2', '台北車站M4', '中山站出口4', '中山站出口5', '中山站出口6', '雙連站出口2', '民權西路站出口1', '民權西路站出口10', '圓山站出口1', '圓山站出口2', '劍潭站出口2', '劍潭站出口3', '劍潭站出口1', '士林站出口1', '士林站出口2', '芝山站出口1', '芝山站出口2', '明德站出口1', '明德站出口2', '明德站出口3', '石牌站出口1', '石牌站出口2', '唭哩岸站出口1', '唭哩岸站出口2', '奇岩站出口1', '奇岩站出口2', '奇岩站出口3', '北投站出口1', '北投站出口2', '新北投站出口1', '復興崗站出口1', '復興崗站出口2', '忠義站出口1', '忠義站出口2', '關渡站出口1', '關渡站出口2', '竹圍站出口1', '竹圍站出口2', '紅樹林站出口1', '淡水站出口1', '淡水站出口2', '東門站出口8', '大安森林公園站出口4', '大安森林公園站出口5', '大安森林公園站出口6', '大安站出口4', '大安站出口3', '信義安和站出口5', '信義安和站出口2A', '台北101/世貿站出口3', '台北101/世貿站出口4', '台北101/世貿站出口5', '象山站出口1', '象山站出口2', '小碧潭站出口1', '小碧潭站出口2', '新店站出口', '新店區公所站出口1', '七張站出口1', '大坪林站出口3', '大坪林站出口5', '景美站出口1', '萬隆站出口4', '公館站出口1', '公館站出口2', '台電大樓站出口5', '古亭站出口1', '小南門站出口3', '松山站出口3', '松山站出口5', '南京三民站出口1', '南京三民站出口2', '台北小巨蛋站出口1', '台北小巨蛋站出口2', '台北小巨蛋站出口3', '南京復興站出口1', '南京復興站出口2', '南京復興站出口7', '松江南京站出口1', '松江南京站出口2', '松江南京站出口8', '北門站出口2', '北門站出口3', '迴龍站出口1', '丹鳳站出口2', '輔大站出口1', '輔大站出口2', '新莊站出口1', '新莊站出口2', '頭前庄站出口1', '先嗇宮站出口1', '三重站出口1', '菜寮站出口2', '台北橋站出口', '大橋頭站出口1', '中山國小站出口4', '行天宮站出口2', '頂溪站出口1', '永安市場站出口', '景安站出口', '南勢角站出口3', '蘆洲站出口2', '三民高中站出口1', '徐匯中學站出口2', '三和國中站出口1', '三重國小站出口', '頂埔站出口1', '頂埔站出口3', '頂埔站出口4', '永寧站出口1', '永寧站出口2', '土城站出口1', '海山站出口2', '亞東醫院站出口3', '府中站出口1', '板橋站出口3', '板橋站出口4', '板橋站出口5', '新埔站出口4', '新埔站出口5', '江子翠站出口3', '龍山寺站出口1', '西門站出口4', '西門站出口6', '善導寺站出口3', '忠孝新生站出口2', '忠孝新生站出口3', '忠孝復興站出口2', '忠孝敦化站出口2', '國父紀念館站出口4', '市政府站出口2', '永春站出口5', '後山埤站出口3', '昆陽站出口1', '昆陽站出口4', '南港站出口2', '南港展覽館站出口1', '南港展覽館站出口2A', '南港展覽館站出口5', '十四張站出口', '秀朗橋站出口2', '景平站出口', '中和站出口', '橋和站出口', '中原站出口', '板新站出口', '新埔民生站出口', '幸褔站出口1', '新北產業園區站出口']
    start_time=time.strftime("%H:%M", time.localtime())
    system = f'''你是交通路線專家,你會根據給予的起點和終點,對過程中的路徑改寫或加入其他地點,並計算出各路徑所花費時間。
                過程中的路徑會考慮地點的開放時間,過程中不重複,請一步步思考並得出結論。
                格式如下:
                    起始時間{start_time} 
                    路徑  
                    1.台北車站M2 → 忠孝復興站出口2 |約需10分鐘|  [9:10]
                    2.忠孝復興站出口2 → 東門站出口8 |約需5分鐘|  [9:15]
                    3.東門站出口8  → 新店站出口 |約需10分鐘|  [9:25]
                    總共花費時間:20分鐘
                    整體路徑:台北車站M2,忠孝復興站出口2,東門站出口8,新店站出口
                '''
    prompt='''{},只需擇一路徑(三個)列出到達,一定要有總共花費時間,不必解釋其他
           '''.format(result)
    completion = client.chat.completions.create(
        model=azure_openai_deployment,
        messages= [
                        {"role": "system", "content":system},
                        {"role":"user","content":prompt}],
        max_tokens=600,
    )
    route_bus=completion.choices[0].message.content  
    
    print(route_bus)    
    mrt_system = '''你是交通路線專家,對台灣的捷運站牢記於心,認識"{}"的無障礙設施地點。'''.format(MRT)
    mrt_user_prompt = '''
                     將文本中出現捷運站,就改寫成最近的無障礙設施地點。只需改寫後的文本,不必解釋其他
                     文本:{} 
                   '''.format(route_bus)
    
    completion = client.chat.completions.create(
        model=azure_openai_deployment,
        messages= [
                        {"role": "system", "content":mrt_system},
                        {"role":"user","content":mrt_user_prompt}],
        max_tokens=600,
    )
    return completion.choices[0].message.content 

if __name__ == "__main__":
    #網頁抓取pdf檔
    # df1=pd.DataFrame([])
    # pdf = pdfplumber.open('./travel_data/銀髮健身.pdf')
    # for p in range(1,len(pdf.pages)):
    #     page=pdf.pages[p]
    #     table = page.extract_table()
    #     pdf_table=[]
    #     for i in table:
    #         pdf_table.append(i)
    #     df=pd.DataFrame(pdf_table)
    #     df1=pd.concat([df1,df],axis=0)
    # pdf.close()
    # df1=df1.reset_index(drop=True)
    # df1=df1.drop_duplicates()
    # df1.columns = df1.iloc[0]
    # df1 = df1[1:]
    # df1.drop(columns= df1.columns[0:3],inplace= True)
    # df1 = df1.fillna(method='ffill')
    # print(df1)
    # df1[['執行據點','據點地址','執行單位']]=df1[['執行據點','據點地址','執行單位']].applymap(lambda x:x.replace('\n',''))
    # df1['all']=df1['執行據點']+'\n地址:'+df1['據點地址']+'\n單位:'+df1['執行單位']+'\n開放時段:'+df1['據點開放時段']+'\n聯絡電話:'+df1['據點聯絡電話']
    # df1.to_excel('out.xlsx', index=False)
    
    # print(df1)
    #位置  縣市  比對




        
    #熱門景點  目的地優先考慮  此為銀髮健身活動
    #result=trip_planning("台北市")#選取經度最靠近的XX地點  行程內包含政府旅遊與銀髮健身俱樂部
    #print(result)
    BUS=['0南', '1', '9', '12', '14', '20', '21', '22', '33', '39','39夜', '41', '49', '57', '63', '66', '72', '88', '99', '202', '202區', '203', '204', '205', '206', '207', '208', '208區', '208直', '212直', '214', '214直', '215', '224', '226', '227', '234', '235', '236區', '246', '247', '247區', '253', '260', '262', '262區', '264', '267', '268', '270', '276', '277', '278', '278區', '280', '280直', '281', '282', '284', '287區', '292', '300', '539', '556', '568', '600', '604', '605', '606', '612', '616', '624', '624綠野香坡', '630', '637', '643', '645', '645副', '648', '651', '652', '656', '660', '660區', '662', '667', '668', '671', '676', '679', '680', '681', '682', '685', '688','704', '704區', '705', '706', '711', '756', '788', '788區', '788海科館', '791', '791區', '791繞貢寮', '791經貢寮區衛生', '795往木柵(台灣好行-木柵平溪線)', '795往平溪(台灣好行-木柵平溪線)', '795往十分寮(台灣好行-木柵平溪線)', '813', '819', '849', '849屈尺社區', '857', '860', '862', '880', '902', '905', '912', '949', '950', '957', '981', '982', '綠1', '紅2', '棕2', '紅3區', '紅5', '橘5', '棕6', '紅7', '藍7', '紅7區', '藍7副', '紅10', '藍10', '紅10區', '通勤11', '紅12', '通勤12', '通勤13', '紅15', '藍15', '通勤16', '通勤18', '藍20區', '通勤21', '紅22', '藍22', '通勤22', '通勤24', '通勤25', '通勤26', '通勤27', '通勤28', '紅29', '通勤29', '紅31', '藍36', '藍38', '紅50', '中山幹線', '仁愛幹線', '內湖幹線', '北環幹線', '民生幹線', '民權幹線', '和平幹線', '忠孝幹線', '承德幹線', '松江新生幹線', '信義幹線', '南京幹線', '重慶幹線', '基隆路幹線', '復興幹線', '敦化幹線', '湯泉-大坪林-湯泉', '羅斯福路幹線']
    result=get_route('''我的所在地: 南京東路3段
        我的目的地: 古亭站''')
    print(result)