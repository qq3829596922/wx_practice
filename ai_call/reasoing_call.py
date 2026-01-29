import logging
import json
from openai import OpenAI
from openai.types.shared import reasoning
from dotenv import load_dotenv
import os
load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

def chat_with_thinking(user_message):
    """开启 thinking 的流式对话"""

    response = client.chat.completions.create(
        model="anthropic/claude-sonnet-4.5",  # 支持 thinking 的模型
        messages=[
            {"role": "user", "content": user_message}
        ],
        stream=True,
        extra_body={
            # "thinking": {
            #     "type": "enabled",
            #     "budget_tokens": 500  # thinking 的 token 预算
            # }
            "reasoning":{
                "enabled":True,
                "effort":"high",
                "max_tokens":500
            }
        }
    )

    logger.info("=" * 50)
    logger.info("开始接收 chunks...")
    logger.info("=" * 50)

    for i, chunk in enumerate(response):
        logger.info(f"--- Chunk {i} ---")
        logger.info(json.dumps(chunk.model_dump(), indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    chat_with_thinking("1+1等于几？")
