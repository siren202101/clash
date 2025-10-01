# --*-- coding: utf-8 --*--

"""
@File: update_cookie.py
@Author: Gemini
@Date: 2025-10-01
@Description: 用于从指定API获取Cookie并更新到青龙面板环境变量的脚本。
"""

import os
import requests
import json
import sys

# --- 全局配置 ---

# 从环境变量中获取 Cookie API 的凭证信息
# 请确保在青龙面板 -> 环境变量中设置了以下变量:
# 1. CC_UUID: 你的 API UUID
# 2. CC_PASSWORD: 你的 API 密码
# 3. updated_cookie: 你想要在青龙面板中更新的Cookie变量名，例如 NS_COOKIE
CC_UUID = os.getenv("CC_UUID")
CC_PASSWORD = os.getenv("CC_PASSWORD")
TARGET_ENV_NAME = os.getenv("updated_cookie") 

# 你的 Cookie API 地址，根据你的实际情况修改
# 注意：脚本中的 IP 地址是根据你提供的 curl 示例设置的
API_BASE_URL = "http://192.168.88.251:28088"

# --- 核心功能函数 ---

def check_configs():
    """检查必要的环境变量是否已设置"""
    print("正在检查环境变量配置...")
    if not all([CC_UUID, CC_PASSWORD, TARGET_ENV_NAME]):
        print("错误：脚本所需的环境变量不完整！")
        print("请确保在青龙面板中正确设置了以下三个环境变量：")
        print("1. CC_UUID: 用于 API 认证的 UUID")
        print("2. CC_PASSWORD: 用于 API 认证的密码")
        print("3. updated_cookie: 需要更新的目标环境变量名称 (例如: NS_COOKIE)")
        sys.exit(1)
    print(f"配置检查通过，将要更新的目标变量是: {TARGET_ENV_NAME}")

def get_latest_cookies(uuid, password):
    """
    通过API获取最新的Cookie。
    """
    api_url = f"{API_BASE_URL}/cookie/get/{uuid}"
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
        print(f"错误：网络请求异常，请检查API地址和网络连接。")
        print(f"异常详情: {e}")
        return None

def format_cookie_string(cookie_list):
    """
    将 JSON 格式的 Cookie 列表转换为原始 Cookie 字符串。
    例如: [{"name": "a", "value": "1"}, {"name": "b", "value": "2"}] -> "a=1; b=2;"
    """
    if not isinstance(cookie_list, list):
        return ""
    
    cookie_parts = [f'{cookie.get("name")}={cookie.get("value")}' for cookie in cookie_list]
    # 使用 "; " 分隔，更符合标准
    return "; ".join(cookie_parts)

def update_ql_env(env_name, new_value):
    """
    使用青龙内置的 QLAPI 更新环境变量。
    """
    # QLAPI 是青龙 Python 任务的内置对象，无需手动导入
    try:
        # 1. 查询环境变量，获取其 ID
        print(f"正在查询青龙环境变量: {env_name}")
        # 使用 searchValue 进行模糊搜索
        search_result = QLAPI.getEnvs({"searchValue": env_name})

        if search_result.get("code") != 200:
            print(f"查询环境变量失败: {search_result.get('message')}")
            return

        target_env = None
        if search_result.get("data"):
            for env in search_result.get("data"):
                # 精确匹配变量名
                if env.get("name") == env_name:
                    target_env = env
                    break
        
        if not target_env:
            print(f"错误：在青龙面板中未找到名为 '{env_name}' 的环境变量。")
            print("请先在环境变量中手动创建一个同名变量。")
            return

        env_id = target_env.get("id") or target_env.get("_id") # 兼容新旧版本
        print(f"已找到目标变量，ID: {env_id}")

        # 2. 准备更新请求的数据
        # 更新时需要提供 id, name, value 和 remarks
        update_payload = {
            "id": env_id,
            "name": env_name,
            "value": new_value,
            "remarks": target_env.get("remarks", "") # 保持原有的备注不变
        }

        # 3. 调用更新接口
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
    
    # 获取原始Cookie数据
    cookie_data_json = get_latest_cookies(CC_UUID, CC_PASSWORD)
    
    if not cookie_data_json or "cookie_data" not in cookie_data_json:
        print("未能获取有效的 Cookie 数据，脚本终止。")
        sys.exit(1)
        
    all_cookies = cookie_data_json.get("cookie_data", {})
    new_cookie_value = None
    
    # 根据要求，检查 'nodeseek' 或 'right' 是否存在于Cookie数据中
    # 找到任何一个匹配项，就格式化并准备更新
    if "nodeseek" in all_cookies:
        print("检测到 'nodeseek' 的 Cookie，正在进行格式化...")
        new_cookie_value = format_cookie_string(all_cookies["nodeseek"])
    elif "right" in all_cookies:
        print("检测到 'right' 的 Cookie，正在进行格式化...")
        new_cookie_value = format_cookie_string(all_cookies["right"])
    else:
        print("在返回的数据中未发现 'nodeseek' 或 'right' 相关的Cookie，本次无需更新。")

    # 如果成功获取并格式化了新的Cookie值，则执行更新操作
    if new_cookie_value:
        print("格式化后的 Cookie 值为:")
        # 为保护隐私，只显示部分内容
        print(f"{new_cookie_value[:50]}...") 
        update_ql_env(TARGET_ENV_NAME, new_cookie_value)
    
    print("\n脚本执行完毕。")
