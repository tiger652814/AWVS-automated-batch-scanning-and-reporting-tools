#main_program.py
import json
import os
import re
import threading
import time
import warnings
from tkinter import messagebox
import docx
import requests
import urllib3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from word_report_generator import generate_word_report as generate_standard_report
from word_SB import generate_word_report as generate_tjdx_report
from vuln_translator import VulnTranslator
from excluded_vulns import excluded_vulns

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 添加此行在全局范围内
vuln_dict_list = {}

def log_exception_to_file(message, file_path):
    with open(file_path, "a") as file:
        file.write(message + "\n")

def clean_string(input_string):
    # 替换或删除控制字符和其他非法字符
    cleaned_string = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_string)
    return cleaned_string

def combine_url_and_request(base_url, request):
    # 提取请求的第一行，例如 "GET /actuator/health HTTP/1.1"
    request_line = request.split('\n')[0]

    # 分割第一行以获取路径部分
    parts = request_line.split(' ')
    if len(parts) >= 2:
        path = parts[1]  # 获取路径，例如 "/actuator/health"
        # 组合基础 URL 和路径
        combined_url = base_url.rstrip('/') + path
        return combined_url
    else:
        return base_url  # 如果请求行格式不正确，只返回基础 URL

def run_main_program(url_file, task_description, api_url, api_key):
    # 初始化翻译器
    translator = VulnTranslator()
    warnings.filterwarnings("ignore")
    headers = {
        "Content-Type": "application/json",
        "X-Auth": api_key,  # AWVS API 密钥
    }

    # 读取 URL 列表
    url_list = []
    with open(url_file, 'r') as f:
        url_list = f.read().splitlines()

    threads = []
    target_id_list = []
    scan_id_list = []
    scan_session_id_list = []

    global vuln_dict_list
    vuln_dict_list = {}  # 重置为一个空字典

    for url in url_list:
        t = threading.Thread(target=process_url, args=(
            url, api_url, api_key, task_description, headers, target_id_list, scan_id_list, scan_session_id_list))
        t.daemon = True  # 将线程设置为守护线程
        t.start()
        threads.append(t)
        time.sleep(0.5)

    # 等待所有线程完成执行
    for thread in threads:
        thread.join()


    # 初始化一个空字典来存储所有漏洞信息
    all_vulns = {}

    # 合并每个URL的漏洞信息到一个大字典
    for url, vuln_dict in vuln_dict_list.items():
        for vuln_id, vuln_data in vuln_dict.items():
            # 翻译漏洞名称
            vuln_data['chinese_vt_name'] = translator.translate(vuln_data['vt_name'])

            # 如果存在中文标题则使用中文标题，否则使用英文标题
            display_vt_name = vuln_data['chinese_vt_name'] if vuln_data['chinese_vt_name'] else vuln_data['vt_name']
            vuln_data['display_vt_name'] = display_vt_name

            all_vulns[vuln_id] = vuln_data

    # for url, vulns in vuln_dict_list.items():
    #     for vuln_id, vuln_data in vulns.items():
    #         # 翻译漏洞名称
    #         vuln_data['chinese_vt_name'] = translator.translate(vuln_data['vt_name'])
    #         all_vulns[vuln_id] = vuln_data
    #
    # # 合并每个URL的漏洞信息到一个大字典
    # for url, vuln_dict in vuln_dict_list.items():
    #     all_vulns.update(vuln_dict)

    # 清理任务描述以用作文件名
    safe_task_description = clean_filename(task_description)

    # 输出到word中
    try:
        # 过滤掉不需要的漏洞
        filtered_vulns = {k: v for k, v in all_vulns.items() if v['vt_name'] not in excluded_vulns}

        # 使用过滤后的漏洞列表生成标准版和过滤版漏洞报告
        print("正在生成标准版漏洞报告...")
        generate_standard_report(all_vulns, f"{safe_task_description}完整版渗透报告+表格")
        print("标准版漏洞报告生成完毕。")

        print("正在生成过滤版漏洞报告...")
        generate_standard_report(filtered_vulns, f"{safe_task_description}过滤版渗透报告+表格")
        print("过滤版漏洞报告生成完毕。")

        # 为SB生成的报告使用同样的过滤逻辑
        print("正在生成SB版漏洞报告...")
        generate_tjdx_report(filtered_vulns, f"{safe_task_description}SB渗透报告+表格")
        print("SB版漏洞报告生成完毕。")

    except Exception as e:
        print(f"生成报告时出现错误: {e}")

    # 输出合并后的大字典
    print(f"vuln_dict_list:{vuln_dict_list}")
    print(f"vuln_dict:{vuln_dict}")
    print(f"all_vulns:{all_vulns}")

def process_url(url, api_url, api_key, task_description, headers, target_id_list, scan_id_list, scan_session_id_list):
    global vuln_dict_list

    lock = threading.Lock()

    # 设置超时时间和重试策略
    timeout = 10  # 增加超时时间
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)

    session = requests.Session()
    # 为 HTTP 和 HTTPS 安装相同的适配器
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        data = {
            "description": task_description,
            "criticality": "10",
            "address": url
        }

        response = session.post(f"{api_url}/targets?c=2&l=1000", headers=headers, data=json.dumps(data), verify=False, timeout=5)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        target_id = response.json()["target_id"]
        target_id_list.append(target_id)

        print(f"Processing URL: {url}, target_id: {target_id}")

        # 修改，为每个URL创建一个任务。
        data = {
            "target_id": target_id,
            "profile_id": "11111111-1111-1111-1111-111111111111",
            "schedule": {
                "disable": False,
                "start_date": None,
                "time_sensitive": False
            }
        }
        response = session.post(f"{api_url}/scans?c=2&l=1000", headers=headers, data=json.dumps(data), verify=False, timeout=5)
        scan_id = response.json()["scan_id"]

    except requests.exceptions.RequestException as e:
        task_description = "task_description_here"  # 定义或获取任务描述
        timestamp = time.strftime('%Y-%m-%d %H-%M-%S')
        error_message = f"处理URL {url} 时出现网络请求错误: {e}\n"
        print(error_message)
        # 将异常信息写入根目录下的文本文件
        log_file_name = f"{task_description}_error_log_{timestamp}.txt"
        log_file_path = os.path.join(os.getcwd(), log_file_name)
        log_exception_to_file(error_message, log_file_path)

    # 校对scan_id
    if scan_id and scan_id not in scan_id_list:
        scan_id_list.append(scan_id)
        # 继续处理扫描任务
    else:
        # 处理无效或重复的scan_id
        print(f"Invalid or duplicate scan_id: {scan_id}")
        # 跳过当前扫描任务
        return  # 使用 return，因为我们处于函数中。

    while True:
        try:
            response = session.get(f"{api_url}/scans/{scan_id}", headers=headers, verify=False, timeout=5)
            response.raise_for_status()  # 检查请求是否成功
            response_json = response.json()

            if "current_session" in response_json:
                status = response_json["current_session"]["status"]
                # 检查状态是否是排队中、已完成、失败等
                if status in ["queued","starting"]:
                    print(f"扫描任务 {scan_id} 正在排队中...")
                elif status in ["completed", "Failed", "aborting", "Stopped", "aborting", "Completed", "failed","Aborting"]:
                    # "aborting","completed","failed","processing","queued"."scheduled","starting"
                    # "Aborting","Completed","Failed","Processing","Queued","Scheduled","Starting"
                    print(response_json)
                    scan_session_id = response_json["current_session"]["scan_session_id"]
                    scan_session_id_list.append(scan_session_id)
                    break
            else:
                print("current_session not found in the response")
                break  # 或者处理这种情况
        except requests.RequestException as e:
            task_description = "task_description_here"  # 定义或获取任务描述
            timestamp = time.strftime('%Y-%m-%d %H-%M-%S')
            error_message = f"处理URL {url} 时出现网络请求错误: {e}\n"
            print(error_message)
            log_file_name = f"{task_description}_error_log_{timestamp}.txt"
            log_file_path = os.path.join(os.getcwd(), log_file_name)
            log_exception_to_file(error_message, log_file_path)
            break  # 重试请求

        time.sleep(5)  # 添加延迟以减少请求频率

    # 扫描完成后，处理漏洞信息
    vuln_dict = {}
    response = session.get(f"{api_url}/scans/{scan_id}/results/{scan_session_id}/vulnerabilities",
                            headers=headers,
                            verify=False, timeout=5)
    vuln_id_list = [vuln["vuln_id"] for vuln in response.json()["vulnerabilities"]]
    for vuln_id in vuln_id_list:
        try:
            print(
                f"Processing vulnerabilities for URL: {url}, scan_id: {scan_id}, scan_session_id: {scan_session_id}, vuln_id: {vuln_id}")
            response = requests.get(
                f"{api_url}/scans/{scan_id}/results/{scan_session_id}/vulnerabilities/{vuln_id}?c=2&l=1000",
                headers=headers,
                verify=False, timeout=5)
            response.raise_for_status()  # 检查响应状态码是否指示错误
            vuln_dict[vuln_id] = response.json()  # 直接提取数据，因为如果出错，上一行代码会抛出异常



            # 获取基础 URL 和请求
            base_url = url  # 从循环或其他地方获取
            request = vuln_dict[vuln_id]["request"]  # 从响应中获取请求
            vuln_dict[vuln_id]["combined_url"] = combine_url_and_request(base_url, request)

        except requests.exceptions.RequestException as e:
            task_description = "task_description_here"  # 定义或获取任务描述
            timestamp = time.strftime('%Y-%m-%d %H-%M-%S')
            error_message = f"处理漏洞ID {vuln_id} 时出现网络请求错误: {e}\n"
            print(error_message)
            # 将异常信息写入根目录下的文本文件
            log_file_name = f"{task_description}_error_log_{timestamp}.txt"
            log_file_path = os.path.join(os.getcwd(), log_file_name)
            log_exception_to_file(error_message, log_file_path)

    with lock:
        vuln_dict_list[url] = vuln_dict.copy()



# 六、多线程扫描
threads = []
lock = threading.Lock()
url_list = []
vuln_scanner = []

# 初始化一个空字典来存储所有漏洞信息
all_vulns = {}

def clean_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename