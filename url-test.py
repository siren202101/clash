import requests
import time

# 手动输入 URL
url = input("请输入URL: ")

try:
    # 开始计时
    start_time = time.time()
    
    # 发送 GET 请求
    response = requests.get(url)
    
    # 结束计时
    end_time = time.time()
    
    # 计算延迟（毫秒）
    latency = (end_time - start_time) * 1000
    
    # 判断状态码
    if response.status_code == 204:
        print("访问成功")
    else:
        print("访问失败，状态码:", response.status_code)
    
    # 输出延迟
    print(f"延迟: {latency:.2f} 毫秒")
    
except requests.exceptions.RequestException as e:
    print("请求异常:", e)
