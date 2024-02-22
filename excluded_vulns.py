# excluded_vulns.py

excluded_vulns = [
    "无 HTTP 重定向", "TRACE 方法已启用", "Permissions-Policy header not implemented",
    "Cookie 未设置 Secure 标记","Access-Control-Allow-Origin header with wildcard (*) value",
    "Content Security Policy Misconfiguration","Cookie 未设置 HttpOnly 标记3","未指定内容类型",
    "Cookie 具有缺失、不一致或矛盾属性","点击劫持：X-Frame-Options 报头缺失","电子邮件地址","可能找到虚拟主机",
    "未实施内容安全策略 (CSP)","检测到 Javascript 源映射","点击劫持：CSP frame-ancestors 缺失",
    "未实施 HTTP 严格传输安全 (HSTS)","Cookie 未设置 HttpOnly 标记","Cookie 通过不安全的连接设置了 Secure 标记",
    "Clickjacking: X-Frame-Options header","Content Security Policy (CSP) not implemented",
    "No HTTP Redirection","HTTP Strict Transport Security (HSTS) not implemented",
    "Clickjacking: X-Frame-Options header","Insecure HTTP Usage","Clickjacking: CSP frame-ancestors missing",
    "Subresource Integrity (SRI) 未实施""Active Mixed Content over HTTPS ",""
    # ... 其他漏洞名称 ...
]
