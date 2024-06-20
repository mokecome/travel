# -*- coding: utf-8 -*-
"""
Created on Wed May  1 15:58:32 2024

@author: User
"""
import pandas as pd
import datetime
import requests
import parsel
import os
import sys
sys.path.append(sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../data_clean"))))
from text_process import sentence_to_qa
if not os.path.exists('./travel_data'):#判斷資料夾
    os.makedirs('./travel_data')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

contry_url='https://travel.yam.com/info/%E5%8F%B0%E4%B8%AD%E6%99%AF%E9%BB%9E/'
contry_response = requests.get(url=contry_url, headers=headers)
contry_html_data = contry_response.text
selector = parsel.Selector(contry_html_data)
contrys  = selector.css('ul#main-menu ul li a::text').getall()
contrys_place=[c for c in contrys if c.endswith('景點')]
print(contrys_place)

df1=pd.DataFrame([])
df3=pd.DataFrame([])
now = datetime.datetime.now()
base_url='https://travel.yam.com'
for contry in contrys_place:
    p=1
    while p<=8:
        url='https://travel.yam.com/info/{}/?p={}'.format(contry,p)
        response = requests.get(url=url, headers=headers)
        html_data = response.text
        selector = parsel.Selector(html_data)
        p=p+1  
        lis = selector.css('div.article_list_tab_content div.article_list_box_info')
        if lis==[]:
            break
        for li in lis:
            url1=base_url+li.css('h2 a::attr(href)').get()
            title=li.css('h2 a::text').get()
            date_str = li.css('p span::text').get()
            date_obj = datetime.datetime.strptime(date_str, '%b %d, %Y')
            if (now - date_obj) <= datetime.timedelta(days=62):#半年前
                response1 = requests.get(url=url1, headers=headers)
                html_data1 = response1.text
                selector1 = parsel.Selector(html_data1)
                ss = selector1.css('div.article_box p::text').getall()
                ss = [s for s in ss if not any(substring in s for substring in ['圖片來源', '圖/'])]
                context=[s.replace('\r\n','').replace('\u3000','').replace('\xa0','') for s in ss]
                before=[] 
                after=[]
                for i,s in enumerate(context):
                    if '地址：' in s:
                        after=context[i:]
                        before=context[:i]
                        break
                for i,s in enumerate(after):
                      if '詳細內容以官方資訊為主' in s:
                          after=after[:i]
                          break
                df2=pd.DataFrame({'time':[date_obj],
                                  'title':[title],
                                  'context':[before],
                                  'text_combine':[sentence_to_qa(after)]
                                  },index=[0])
                df1=pd.concat([df1,df2],axis =0)
    df3=pd.concat([df3,df1],axis =0)


df3.reset_index(inplace=True,drop=True)
df3.to_excel('輕旅行.xlsx',index=False)

    
    



