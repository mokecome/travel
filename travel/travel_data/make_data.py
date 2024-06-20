# -*- coding: utf-8 -*-
"""
Created on Fri May  3 01:32:59 2024

@author: User
"""


from openai import AzureOpenAI
import pandas as pd

def context_format(df,Q,A,filename):
    import json
    with open(filename, "w", encoding="utf-8") as f:
        for i,row in df.iterrows():
            question=row[Q].strip()
            answer=row[A].strip()
            context_json={"query":question,"target":answer}
            json.dump(context_json, f, ensure_ascii=False)
            f.write('\n')

def get_llm_qa(input_):
    client = AzureOpenAI(
      azure_endpoint = "https://mokecome-llm-20240429.openai.azure.com/", 
      api_key="e349db7c996d485281ed1e5ed04d6cb1",
      api_version="2024-02-15-preview"
    )
    message_text = [{"role":"user","content":'''{},請根据上述事實對交通方式、景點介紹、天氣環境產生5個問答對,請注意天氣環境的回答中應該包含景點名稱、溫度、降雨機率環境、空氣品質指數,格式如下
                                             Q: 
                                             A:
                                             Q:
                                             A:
                                            '''.format(input_)}]
    completion = client.chat.completions.create(
      model="GTP35-1106-4k", # model = "deployment_name"
      messages = message_text,
      temperature=0.7,
      max_tokens=800,
      top_p=0.90,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    answer=completion.to_dict()['choices'][0]["message"]
    return answer['content']
def qa_format(df,qa_list):#df Q A
    print(qa_list)
    qa_list=[qa.strip() for qa in qa_list.split('\n') if qa.strip()!='']
    print(qa_list)
    # 分割問題和答案
    questions = [qa_list[i][3:] for i in range(0, len(qa_list), 2)]
    answers = [qa_list[i][3:] for i in range(1, len(qa_list), 2)]
    # 建立 DataFrame
    df1 = pd.DataFrame({'Q': questions,'A': answers})
    df=pd.concat([df, df1],axis =0)
    return df()







#context_format(df,'Q','all','tw_data.jsonl')

if __name__ == "__main__":
    # df=pd.read_excel('travel_1.xlsx')
    # df_all=pd.DataFrame([])
    # for i,row in df.iterrows():
    #     #自己加的
    #     df1 = pd.DataFrame({'Q':[row['景點']+'的行程特色介紹?'] ,'A':[row['all']] })
    #     df_all=pd.concat([df_all, df1],axis =0)
    #     #大模型加的 
    #     qa_list=get_llm_qa(row['all'])
    #     df_all=qa_format(df_all,qa_list)
    #     print(df_all)
    # df_all.reset_index(inplace=True,drop=True)
    # df_all.to_excel('travel_qa.xlsx',index=False)
    df=pd.read_excel('travel_qa.xlsx')
    context_format(df,'Q','A','tw_data.jsonl')



    





