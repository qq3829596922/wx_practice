"""精简版 reasoning 测试脚本"""
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

print(f"base_url: {os.getenv('OPENAI_BASE_URL')}")
print(f"model: {os.getenv('AI_MODEL')}")
print("-" * 50)

stream = client.chat.completions.create(
    model=os.getenv("AI_MODEL"),
    messages=[{"role": "user", "content": "1+1等于几？说100字的回答"}],
    stream=True,
    extra_body={
        "reasoning": {
            "enabled": True
        }
    }
)

print("\n=== 原始 chunk 输出 ===\n")
for i, chunk in enumerate(stream):
    print(f"[{i}] {chunk}")
    print(f"    type: {type(chunk)}")
    if chunk.choices:
        delta = chunk.choices[0].delta
        print(f"    delta attrs: {dir(delta)}")
        print(f"    delta.__dict__: {getattr(delta, '__dict__', 'N/A')}")
        # 尝试不同的 reasoning 字段名
        for attr in ['reasoning', 'reasoning_content', 'reasoning_details', 'thinking']:
            val = getattr(delta, attr, None)
            if val is not None:
                print(f"    >>> Found {attr}: {val}")
    print()
