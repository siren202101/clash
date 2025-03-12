import requests
from bs4 import BeautifulSoup
import time
import os

# 每次执行时删除旧的日志文件
if os.path.exists("refresh_log.txt"):
    os.remove("refresh_log.txt")
if os.path.exists("no_keyword_pages_log.txt"):
    os.remove("no_keyword_pages_log.txt")

print("\033[34m***神棍局***天威DNS雷达系统\033[0m")

# 检查关键词函数
def check_keyword(content):
    keywords = ["正确","河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海","内蒙古","广西","西藏","宁夏","新疆","北京","天津","上海","重庆"]
    for keyword in keywords:
        if keyword in content:
            return True
    return False

# 记录日志到文件
def write_log_to_file(total_checks, keyword_detected_count, keyword_not_detected_count, log_details):
    with open("refresh_log.txt", "w", encoding="utf-8") as log_file:
        log_file.write("====== 检测结果统计 ======\n")
        log_file.write(f"总共检测次数: {total_checks}\n")
        log_file.write(f"DNS正确的次数: {keyword_detected_count}\n")
        log_file.write(f"DNS异常的次数: {keyword_not_detected_count}\n")
        log_file.write("\n====== 详细日志 ======\n")
        for detail in log_details:
            log_file.write(detail + "\n")

# 记录嵌入页面内容到另一个文件，当DNS异常时
def save_page_content(content, index):
    with open("no_keyword_pages_log.txt", "a", encoding="utf-8") as page_file:
        page_file.write(f"\n\n====== 第 {index+1} 次刷新DNS异常的嵌入页面内容 ======\n")
        page_file.write(content)

# 主程序
def main(refresh_count=99):   #检测次数
    url = "http://nstool.netease.com/"
    total_checks = 0
    keyword_detected_count = 0
    keyword_not_detected_count = 0
    log_details = []

    for i in range(refresh_count):
        try:
            total_checks += 1
            print(f"第 {i+1} 次刷新:")

            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.encoding = 'gbk'  # 设置编码
            soup = BeautifulSoup(response.text, 'html.parser')

            # 查找iframe标签并获取src属性
            iframe = soup.find('iframe')
            iframe_src = iframe['src']

            # 获取嵌入页面内容
            iframe_response = requests.get(iframe_src, headers={'User-Agent': 'Mozilla/5.0'})
            iframe_response.encoding = 'gbk'  # 设置编码
            iframe_content = iframe_response.text

            # 检查关键词
            if check_keyword(iframe_content):
                keyword_detected_count += 1
                print("DNS正确，继续查询...")
                log_details.append(f"第 {i+1} 次：DNS正确")
            else:
                keyword_not_detected_count += 1
                print("DNS异常，继续查询...")
                log_details.append(f"第 {i+1} 次：DNS异常")
                
                # 保存没有关键词的嵌入页面内容到日志文件
                save_page_content(iframe_content, i)

            time.sleep(2)  # 等待5秒后再刷新

        except Exception as e:
            print("发生错误：", e)
            log_details.append(f"第 {i+1} 次：发生错误，{e}")
            break

    # 统计日志
    print("\n====== 检测结果统计 ======")
    print(f"总共检测次数: {total_checks}")
    print(f"DNS正确的次数: {keyword_detected_count}")
    print(f"DNS异常的次数: {keyword_not_detected_count}")
    
    # 写入日志到文件
    write_log_to_file(total_checks, keyword_detected_count, keyword_not_detected_count, log_details)
    print("日志已写入 refresh_log.txt 文件。")

if __name__ == '__main__':
    main()  # 默认刷新99次
