# vuln_translator.py
import json

class VulnTranslator:
    def __init__(self):
        self.vuln_translations = {
            "SQL Injection": "SQL注入",
            "Cross Site Scripting": "跨站脚本攻击",
            "Outdated JavaScript libraries": "已过时的 JavaScript 库",
            "Vulnerable JavaScript libraries": "易受攻击的 JavaScript 库",
            "Unencrypted connection": "未加密的连接",
            "Internal IP address disclosure": "内部 IP 地址披露",
            "ASP.NET version disclosure": "ASP.NET 版本泄露",
            "Microsoft IIS version disclosure": "Microsoft IIS 版本披露",
            "TLS 1.1 enabled": "TLS 1.1 已启用",
            "TLS/SSL Sweet32 attack": "TLS/SSL Sweet32 攻击",
            "TLS/SSL Weak Cipher Suites": "TLS/SSL 弱密码套件",
            "Insecure crossdomain.xml policy": "不安全的crossdomain.xml策略",
            "HTTP.sys remote code execution vulnerability": "HTTP.sys远程执行代码漏洞",
            "Sensitive pages could be cached": "敏感页面可能被缓存",
            "Unrestricted access to Prometheus Metrics": "Prometheus Metrics 未授权访问",
            "Unrestricted access to a monitoring system": "monitoring system 未授权访问",
            "Unrestricted access to Prometheus": "Prometheus 未授权访问",
            "Vulnerable package dependencies [high]": "易受攻击的包依赖项[高]",
            "Directory listings": "目录列表",
            "User credentials are sent in clear text": "用户凭据已作为明文发送",
            "[Possible] Internal IP Address Disclosure": "内部 IP 地址披露",
            "[Possible] Internal Path Disclosure (*nix)": "可能出现服务器路径披露 (Unix)",
            "Apache Struts2 Remote Command Execution (S2-052) ": "Apache Struts2 远程命令执行漏洞（S2-052）",
            "Unprotected JSON file leaking secrets": "未加密的 JSON 文件",
            "Spring Boot Actuator v2": "Sping 未授权访问",
            "Golang runtime profiling data": "Golang 运行时分析数据",
            "(Possible) Cross site scripting": "跨站脚本",
            "Open Silverlight Client Access Policy": "打开Silverlight客户端访问策略",
            "Version Disclosure (ASP.NET)": "ASP.NET 版本泄露",
            "SSL Untrusted Root Certificate": "SSL不受信任的根证书",
            "API Security Broken Object Level Authorization": "API对象权限校验不足",
            "Insecure Transportation Security Protocol Supported (TLS 1.1)": "TLS 1.1 已启用",
            "Certificate is Signed Using a Weak Signature Algorithm": "证书使用了弱签名算法进行签名",
            "Version Disclosure (IIS)": "Microsoft IIS 版本披露",
            "SSL/TLS Not Implemented": "未实现 SSL/TLS",
            "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            "URL 重定向": "URL 重定向（Web 服务器）",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",
            # "SSL Certificate Name Hostname Mismatch": "SSL证书名称主机名不匹配",


            # ... 更多映射 ...
        }

    def translate(self, english_name):
        # 如果找不到翻译，则返回原始英文名称
        return self.vuln_translations.get(english_name, english_name)
