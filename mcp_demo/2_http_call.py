"""
HTTP 方式调用 Demo

特点：
- 你需要知道接口地址
- 你需要知道参数格式
- 你需要自己写调用代码
- 你决定什么时候调用什么接口
"""

import httpx

BASE_URL = "http://localhost:9999"

def add(a: float, b: float) -> dict:
    """调用加法接口"""
    resp = httpx.post(f"{BASE_URL}/add", json={"a": a, "b": b})
    return resp.json()

def multiply(a: float, b: float) -> dict:
    """调用乘法接口"""
    resp = httpx.post(f"{BASE_URL}/multiply", json={"a": a, "b": b})
    return resp.json()

if __name__ == "__main__":
    print("=" * 50)
    print("HTTP 方式调用")
    print("=" * 50)

    # 你需要自己决定调用什么
    print("\n调用加法: 3 + 5")
    result = add(3, 5)
    print(f"结果: {result}")

    print("\n调用乘法: 4 × 6")
    result = multiply(4, 6)
    print(f"结果: {result}")

    print("\n" + "=" * 50)
    print("HTTP 方式的特点:")
    print("1. 你需要知道有哪些接口")
    print("2. 你需要知道参数格式")
    print("3. 你写代码决定调用哪个接口")
    print("4. AI 不参与调用决策")
    print("=" * 50)
