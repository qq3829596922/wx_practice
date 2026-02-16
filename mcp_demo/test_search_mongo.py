"""测试 /search_mongo 接口"""

import httpx
import json

# 配方服务地址
BASE_URL = "http://localhost:8460"

def test_search_mongo():
    """测试 ES + MongoDB 搜索"""
    url = f"{BASE_URL}/search_mongo"

    # 搜索参数
    payload = {
        "query": "保湿面霜",
        "top_k": 3,
        "from_offset": 0,
        "efficacy_tags": ["保湿"],
        "formulation_type_detail": ["霜"],
    }

    print(f"请求: POST {url}")
    print(f"参数: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    print("=" * 60)

    try:
        response = httpx.post(url, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"返回 {result.get('count', 0)} 条结果，共 {result.get('total', 0)} 条")
        print("=" * 60)

        # 打印配方列表
        for doc in result.get("documents", []):
            print(f"\n配方: {doc.get('formula_name', '未知')}")
            print(f"  编码: {doc.get('formula_code', '未知')}")
            print(f"  公司: {doc.get('company', '未知')}")
            print(f"  功效: {doc.get('efficacy_tags', [])}")

    except httpx.ConnectError:
        print(f"❌ 连接失败，服务是否在 {BASE_URL} 运行？")
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP 错误: {e.response.status_code}")
        print(e.response.text)
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    test_search_mongo()
