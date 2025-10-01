# --*-- coding: utf-8 --*--

"""
@File: update_cookie.py
@Author: Gemini
@Date: 2025-10-01
@Description: 用于从指定API获取Cookie并更新到青龙面板环境变量的脚本。
@Version: 3.0
@Changes: 根据Cookie类型(nodeseek/right)分别更新不同的环境变量(NS_COOKIE/ES_COOKIE)。
"""

import os
import requests
import json
import sys

# --- 全局配置 ---

# 从环境变量中获取 Cookie API 的凭证信息
# 请确保在青龙面板 -> 环境变量中设置了以下变量:
# 1. UCC: 你的 Cookie API 基础地址 (例如: http://192.168.88.251:28088/cookie)
# 2. CC_UUID: 你的 API UUID
# 3. CC_PASSWORD: 你的 API 密码
# 脚本会自动更新名为 NS_COOKIE 和 ES_COOKIE 的变量，请确保它们已存在。
UCC_URL = os.getenv("UCC")
CC_UUID = os.getenv("CC_UUID")
CC_PASSWORD = os.getenv("CC_PASSWORD")

# --- 核心功能函数 ---

def check_configs():
    """检查必要的环境变量是否已设置"""
    print("正在检查环境变量配置...")
    if not all([UCC_URL, CC_UUID, CC_PASSWORD]):
        print("错误：脚本所需的环境变量不完整！")
        print("请确保在青龙面板中正确设置了以下三个环境变量：")
        print("1. UCC: 你的 Cookie API 基础地址 (例如: http://192.168.88.251:28088/cookie)")
        print("2. CC_UUID: 用于 API 认证的 UUID")
        print("3. CC_PASSWORD: 用于 API 认证的密码")
        sys.exit(1)
    print("配置检查通过！")
    print(f"API 地址: {UCC_URL}")

def get_latest_cookies(base_url, uuid, password):
    """
    通过API获取最新的Cookie。
    """
    api_url = f"{base_url}/get/{uuid}"
    headers = {"Content-Type": "application/json"}
    payload = {"password": password if password else ""}
    
    print(f"正在从 {api_url} 获取 Cookies...")
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            print("成功获取 API 响应。")
            return response.json()
        else:
            print(f"错误：API 请求失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"错误：网络请求异常，请检查API地址 '{UCC_URL}' 和网络连接。")
        print(f"异常详情: {e}")
        return None

def format_cookie_string(cookie_list):
    """
    将 JSON 格式的 Cookie 列表转换为原始 Cookie 字符串。
    """
    if not isinstance(cookie_list, list):
        return ""
    
    cookie_parts = [f'{cookie.get("name")}={cookie.get("value")}' for cookie in cookie_list]
    return "; ".join(cookie_parts)

def update_ql_env(env_name, new_value):
    """
    使用青龙内置的 QLAPI 更新环境变量。
    """
    try:
        print(f"\n--- 开始更新变量: {env_name} ---")
        print(f"正在查询青龙环境变量: {env_name}")
        search_result = QLAPI.getEnvs({"searchValue": env_name})

        if search_result.get("code") != 200:
            print(f"查询环境变量失败: {search_result.get('message')}")
            return

        target_env = None
        if search_result.get("data"):
            for env in search_result.get("data"):
                if env.get("name") == env_name:
                    target_env = env
                    break
        
        if not target_env:
            print(f"错误：在青龙面板中未找到名为 '{env_name}' 的环境变量。")
            print(f"请先在环境变量中手动创建 '{env_name}'。")
            return

        env_id = target_env.get("id") or target_env.get("_id")
        print(f"已找到目标变量，ID: {env_id}")
        
        update_payload = {
            "id": env_id,
            "name": env_name,
            "value": new_value,
            "remarks": target_env.get("remarks", "")
        }

        print("正在提交更新请求...")
        update_result = QLAPI.updateEnv(update_payload)
        
        if update_result.get("code") == 200:
            print(f"✅ 环境变量 '{env_name}' 更新成功！")
        else:
            print(f"❌ 环境变量 '{env_name}' 更新失败！")
            print(f"青龙API响应: {update_result.get('message', '无详细信息')}")

    except NameError:
        print("错误: QLAPI 未定义。请确保此脚本在青龙面板的 Python 任务环境中运行。")
    except Exception as e:
        print(f"更新环境变量时发生未知错误: {e}")


# --- 主逻辑 ---

if __name__ == "__main__":
    check_configs()
    
    cookie_data_json = get_latest_cookies(UCC_URL, CC_UUID, CC_PASSWORD)
    
    if not cookie_data_json or "cookie_data" not in cookie_data_json:
        print("未能获取有效的 Cookie 数据，脚本终止。")
        sys.exit(1)
        
    all_cookies = cookie_data_json.get("cookie_data", {})
    updated = False

    # 逻辑1: 检查 'nodeseek' 并更新 'NS_COOKIE'
    if "nodeseek" in all_cookies:
        updated = True
        print("检测到 'nodeseek' 的 Cookie，正在处理...")
        ns_cookie_value = format_cookie_string(all_cookies["nodeseek"])
        if ns_cookie_value:
            print(f"格式化的 NS_COOKIE: {ns_cookie_value[:50]}...")
            update_ql_env("NS_COOKIE", ns_cookie_value)
        else:
            print("'nodeseek' 的 Cookie 数据为空，不执行更新。")

    # 逻辑2: 检查 'right' 并更新 'ES_COOKIE'
    if "right" in all_cookies:
        updated = True
        print("检测到 'right' 的 Cookie，正在处理...")
        es_cookie_value = format_cookie_string(all_cookies["right"])
        if es_cookie_value:
            print(f"格式化的 ES_COOKIE: {es_cookie_value[:50]}...")
            update_ql_env("ES_COOKIE", es_cookie_value)
        else:
            print("'right' 的 Cookie 数据为空，不执行更新。")
    
    # 如果两种cookie都未找到
    if not updated:
        print("\n在返回的数据中未发现 'nodeseek' 或 'right' 相关的Cookie，本次无需更新。")

    print("\n脚本执行完毕。")
