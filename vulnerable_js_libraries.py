import re
import json

def extract_js_library_vulnerabilities(vuln_data):
    """从漏洞数据中提取易受攻击的 JavaScript 库信息"""
    vuln_details = []
    for vuln_id, data in vuln_data.items():
        if data.get('vt_name') == '易受攻击的 JavaScript 库':
            # 提取漏洞的详细信息
            details = data.get('details', '')
            library_name, library_version = extract_library_name_and_version(details)
            vuln_details.append({
                'library_name': library_name,
                'library_version': library_version,
                'details': details
            })
    return vuln_details

def extract_library_name_and_version(details):
    """从详细信息中提取库名称和版本"""
    match = re.search(r'([a-zA-Z]+)\s*(\d+\.\d+\.?\d*)', details)
    if match:
        return match.group(1), match.group(2)
    return 'Unknown', '0.0.0'

def format_vulnerabilities(vuln_details):
    """格式化输出易受攻击的 JavaScript 库的漏洞信息"""
    formatted_output = []
    for detail in vuln_details:
        formatted_info = f"库名称: {detail['library_name']}\n"
        formatted_info += f"版本: {detail['library_version']}\n"
        formatted_info += f"详细信息: {detail['details']}\n"
        formatted_output.append(formatted_info)
    return formatted_output

def main(vuln_dict_list):
    """主函数，处理易受攻击的 JavaScript 库的漏洞信息"""
    js_library_vulns = extract_js_library_vulnerabilities(vuln_dict_list)
    formatted_vulns = format_vulnerabilities(js_library_vulns)
    return formatted_vulns
