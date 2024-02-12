# generate_merged_report.py
import json
import os
import docx
import time
from tkinter import messagebox
from your_existing_module import add_vuln_details_to_doc, generate_word_report  # 替换为实际模块名

def load_vuln_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def merge_vulns(all_vulns):
    merged_vulns = {}
    for vuln_id, vuln_data in all_vulns.items():
        vt_name = vuln_data["vt_name"]
        if vt_name not in merged_vulns:
            merged_vulns[vt_name] = vuln_data.copy()
            merged_vulns[vt_name]["combined_urls"] = [vuln_data.get("combined_url", vuln_data["affects_url"])]
        else:
            merged_vulns[vt_name]["combined_urls"].append(vuln_data.get("combined_url", vuln_data["affects_url"]))
    return merged_vulns

def generate_merged_word_report(merged_vulns, report_name):
    print("开始创建合并的 Word 文档")
    doc = docx.Document()
    for vt_name, vuln in merged_vulns.items():
        vuln["combined_url"] = "\n".join(set(vuln["combined_urls"]))  # 去重并合并 URL
        add_vuln_details_to_doc(doc, vuln)  # 使用你现有的函数
    file_name = f"{report_name}_{time.strftime('%Y-%m-%d %H-%M-%S')}.docx"
    doc.save(file_name)
    print("已保存合并的 Word 文档")
    messagebox.showinfo("操作完成", f"合并报告已生成: {file_name}")

if __name__ == "__main__":
    vulns_file = "vulns.json"  # 漏洞数据文件
    all_vulns = load_vuln_data(vulns_file)
    merged_vulns = merge_vulns(all_vulns)
    generate_merged_word_report(merged_vulns, "Merged_Vulnerability_Report")