from ast import arguments
import logging
from pickle import FALSE
from pydoc import describe
from typing import Generator, Optional
from openai import OpenAI
import json
from dotenv import load_dotenv
load_dotenv()
import os
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()  # 控制台
    ]
)
logger=logging.getLogger()

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url=os.getenv("OPENAI_BASE_URL"))

def get_weather(city,date):
    """ 获取城市天气 """
    return f"城市{city}的天气是{date}，可以出海打鱼"
def get_tempareture(city,time):
    """获取城市某个时间的气温"""
    return f"城市{city}{time}的气温是60度不要出门不然会被考成人干"

def weather_report(weather,tempareture,ai_conclusion):
    return f"""
    天气获取情况{weather}\n
    温度获取情况:{tempareture}\n
    ai总结:{ai_conclusion}\n
    """


tool_functions={
    "get_weather":get_weather,
    "get_temperature":get_tempareture,
    "weather_report":weather_report
}

tools=[
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description":"获取当前日期的天气情况",
            "parameters":{
                "type":"object",
                "properties":{
                        "city":{
                            "type":"string",
                            "description":"当前的城市"
                        },
                        "date":{
                            "type":"string",
                            "description":"当前的日期"
                        },
                    
                    },
                "required":["city"]
                }

            }
    },
    {
        "type":"function",
        "function":{
            "name":"get_temperature",
            "description":"获取城市某个时间的气温",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"查询的城市"
                    },
                    "time":{
                        "type":"string",
                        "description":"时间"
                    }

                },
                "required":["city"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"weather_report",
            "description":"结合天气和温度工具，以及大模型的总结，出一个天气预报",
            "parameters":{
                "type":"object",
                "properties":{
                    "weather":{
                        "type":"string",
                        "description":"天气工具的结果"
                    },
                    "tempareture":{
                        "type":"string",
                        "description":"温度工具的结果"
                    },
                    "ai_conclusion":{
                        "type":"string",
                        "description":"ai对于天气工具和温度工具总结"
                    }
                },
                "requiered":["weather","tempareture","ai_conclusion"]
            }
        }
    }
]

def execute_tools(tool_call_list):
    tool_calls=[]
    for tc in tool_call_list:
        tool_name=tc["function"]["name"]
        id=tc["id"]
        arguments=json.loads(tc["function"]["arguments"])
        content=tool_functions[tool_name](**arguments)
        tool_calls.append({"role":"tool","tool_call_id":id,"content":content})
    
    return tool_calls

def stream_chat(messages,tools=None):

    stream=client.chat.completions.create(
        model=os.getenv("AI_MODEL"),
        messages=messages,
        tools=tools,
        stream=True,
        extra_body={
            "reasoning":{
                "enabled":True
            }
        }
        
        )
    contents=""
    reasonings=""
    tool_calls_list=[]
    tool_num=0
    start_reasoning=False
    for chunk in stream:
        print(chunk)
        choice=chunk.choices[0]
        delta=choice.delta
        
        content=delta.content

        reasoning_details=getattr(delta,"reasoning_details",None)
        # print(reasoning)

        if reasoning_details:
            for reasoning in reasoning_details:
                if not start_reasoning:
                    print("start thinking\n")
                    start_reasoning=True
                if reasoning.get("text",""):
                    reasonings+=reasoning["text"]
                    print(reasoning["text"],flush=True,end="")
            
                if reasoning.get("signature",""):
                    print("stop thinking\n")
                    start_reasoning=False
        # print(delta)

        if content:
            contents+=content
            print(content,flush=True,end="")
        
        if delta.tool_calls:
            for tool_calls in delta.tool_calls:
                index=tool_calls.index

                while tool_num<=index:
                    tool_calls_list.append({"index":"","id":"","type":"","function":{"name":"","arguments":""}})
                    tool_num+=1
                tool_calls_list[index]["index"]=index
                tool_calls_list[index]["type"]="function"
                # print(tool_calls)
                if tool_calls.function.name:
                    tool_calls_list[index]["function"]["name"]=tool_calls.function.name
                if tool_calls.id:
                    tool_calls_list[index]["id"]=tool_calls.id
                if tool_calls.function.arguments:
                    tool_calls_list[index]["function"]["arguments"]+=tool_calls.function.arguments
                # print(tool_calls_list)
            
        # print(delta)
    # print(chunk)
    return content,tool_calls_list

import time
def chat(user_message):
    messages=[{"role":"user","content":user_message}]
    while True:
        content,tool_calls_list=stream_chat(messages=messages,tools=tools)
        # print(f"\n\ntool_calls_list:{tool_calls_list}\n\n")
        assistant={"role":"assistant"}
        if content:
            assistant["content"]=content
        if tool_calls_list:
            assistant["tool_calls"]=tool_calls_list
            messages.append(assistant)
            tool_calls=execute_tools(tool_calls_list)
            # print(f"\n\ntool_calls:{tool_calls}\n\n")
            messages.extend(tool_calls)
        else:
            if content:
                messages.append(assistant)
            break
        
        print(bool(tool_calls_list))
        # time.sleep(5)


if __name__=="__main__":

    chat("帮我看下北京30号今天的天气和下午2点的温度,然后做出ai总结，再调用weather_report 工具，最后按照weather_report 工具 再总结给我")





# print(f"content:{content} \n\ntool_calls_list:{tool_calls_list}")

# print()
# def chat(messages:list,tools:list)->Generator:

