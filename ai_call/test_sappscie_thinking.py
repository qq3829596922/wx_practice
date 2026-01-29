"""
Sappscie API Thinking 测试脚本 (OpenRouter 格式)

=== 启用 Thinking (两种方式都支持) ===
方式1: extra_body={"reasoning": {"enabled": True}}
方式2: extra_body={"reasoning_effort": "medium"}  # low / medium / high

=== 返回格式 ===
字段: reasoning_details (列表)
结构: [{"type": "reasoning.text", "text": "...", "signature": "...", "format": "anthropic-claude-v1", "index": 0}]

=== 流式响应阶段 ===
阶段1: Thinking
    - reasoning_details 有值，包含 text
    - content = None 或 ''

阶段2: Thinking 结束
    - reasoning_details 包含 signature 字段

阶段3: Response
    - reasoning_details = [] (空列表)
    - content 有值

阶段4: 结束
    - finish_reason = 'stop'

=== 判断 Thinking 结束 ===
方式1: reasoning_details 中出现 signature 字段
方式2: content 开始有值
"""

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
    messages=[{"role": "user", "content": "1+1等于几？简短回答"}],
    stream=True,
    extra_body={
        "reasoning": {"enabled": True}  # OpenRouter 格式
    }
)

reasoning = ""
content = ""
in_thinking = False
thinking_ended = False

print("\n[Thinking]")
for chunk in stream:
    if not chunk.choices:
        if chunk.usage:
            print(f"\n[Usage] tokens: {chunk.usage.total_tokens}")
        continue

    delta = chunk.choices[0].delta
    finish_reason = chunk.choices[0].finish_reason

    # OpenRouter 格式: reasoning_details (列表)
    reasoning_details = getattr(delta, "reasoning_details", None)

    if reasoning_details:
        for r in reasoning_details:
            # 检查是否有 text
            text = r.get("text", "")
            if text:
                if not in_thinking:
                    in_thinking = True
                reasoning += text
                print(text, end="", flush=True)

            # 检查是否有 signature (thinking 结束标志)
            if r.get("signature"):
                if in_thinking:
                    print("\n\n[Response]")
                    in_thinking = False
                    thinking_ended = True

    # Response 内容
    if delta.content:
        # 如果还没检测到 thinking 结束，但 content 有值了
        if in_thinking and not thinking_ended:
            print("\n\n[Response]")
            in_thinking = False
            thinking_ended = True
        content += delta.content
        print(delta.content, end="", flush=True)

    if finish_reason == "stop":
        print("\n")

print("=" * 50)
print(f"Reasoning ({len(reasoning)} chars): {reasoning[:100]}..." if len(reasoning) > 100 else f"Reasoning: {reasoning}")
print(f"Content: {content}")
