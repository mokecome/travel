# -*- coding: utf-8 -*-
"""
Created on Sun May 26 00:17:33 2024

@author: User
"""
from langchain_openai import AzureChatOpenAI
from openai import AzureOpenAI
import json
import requests
client = AzureChatOpenAI(
  azure_endpoint = "https://mokecome-openai-20240501.openai.azure.com/", 
  api_key="a34657118e1e4ca3b7e62c3ecfd1cb80",
  api_version="2024-02-01",
  azure_deployment="gpt4o-mokecome-0522",
  temperature=0,
)





image_client = AzureOpenAI(
    api_version="2024-02-01",
    azure_endpoint="https://dall-e3-0522.openai.azure.com/",
    api_key='369d428f2a8a4ca182d5651b522daec6',
)

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.tools import tool,BaseTool
from typing import Optional,Union

from langchain_openai import AzureOpenAI
from langchain.agents import (AgentExecutor,create_react_agent)
from langchain_core.prompts import (PromptTemplate,ChatPromptTemplate,MessagesPlaceholder)

@tool
def generator_image(prompt) -> str:
    """生成圖片時,使用這個工具"""
    result = image_client.images.generate(
        model="Dalle3", # the name of your DALL-E 3 deployment
        prompt=prompt,
        n=1
    )
    image_url = json.loads(result.model_dump_json())['data'][0]['url']
    response = requests.get(image_url)
    with open('generated_image.jpg', 'wb') as f:
        f.write(response.content)
    return f'已使用{image_url}生成圖片'
@tool
def search_run(query:str) -> str:
    """使用網路搜尋你不知道的事物"""
    search = DuckDuckGoSearchAPIWrapper()
    answer = ''
    result = search.results(query, 3)
    for item in result:
        print(item['title'], item['snippet'])  # 標題   摘要   網址
        answer = answer + ',' + item['title']
    return answer

tools=[generator_image,search_run]

prompt = PromptTemplate.from_template("""Answer the following questions as best you can. You have access to the following tools:
                                      {tools}
                                       Use the following format:
                                       Question: the input question you must answer
                                       Thought: you should always think about what to do
                                       Action: the action to take, should be one of [{tool_names}]
                                       Action Input: the input to the action
                                       Observation: the result of the action
                                       ... (this Thought/Action/Action Input/Observation can repeat N times)
                                       Thought: I now know the final answer 
                                       Final Answer: the final answer to the original input question
                                       
                                       Begin!
                                       
                                       Question: {input}
                                       Thought : {agent_scratchpad}
                                       """)
#產生一個agent
agent_executor = AgentExecutor(agent=create_react_agent(llm=client,prompt=prompt,tools=tools),tools=tools,verbose=True)
result = agent_executor.invoke({'input': '2024AI趨勢大師', 'chat_history': []})
print(result['output'])

import time
import requests
start_time=time.strftime("%H:%M", time.localtime())