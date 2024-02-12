# gui.py
import json
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import main_program
import os
import threading
from tkinter import scrolledtext
from mac_checker import MACAddressChecker  # 从 mac_checker.py 中导入 MACAddressChecker

def load_config():
    global api_prefix, api_key
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            api_prefix = config.get("api_prefix", "")
            api_key = config.get("api_key", "")
    except FileNotFoundError:
        api_prefix = ""
        api_key = ""

def start_scan():
    url_file = url_file_entry.get()
    task_description = description_entry.get()

    if not url_file:
        messagebox.showerror("错误", "请选择需要扫描的URL文件")
        return

    if not task_description:
        messagebox.showerror("错误", "请输入任务名称")
        return
    print(f"API Key: {api_key}")  # 输出 API Key 以进行调试

    # 创建一个新线程来运行 main_program.run_main_program
    scan_thread = threading.Thread(target=main_program.run_main_program, args=(url_file, task_description, api_prefix, api_key))
    scan_thread.start()

    #main_program.run_main_program(url_file, task_description, api_prefix, api_key)

# 调用 load_config() 函数以在程序启动时加载配置信息
load_config()

def save_config():
    global api_prefix, api_key
    api_prefix = api_prefix_entry.get()
    api_key = api_key_entry.get()

    config = {"api_prefix": api_prefix, "api_key": api_key}
    with open("config.json", "w") as f:
        json.dump(config, f)

    config_window.withdraw()

try:
    with open("config.json", "r") as f:
        config = json.load(f)
        api_prefix = config.get("api_prefix", "")
except FileNotFoundError:
    config = {}
    api_prefix = ""

def print_to_output_display(text):
    output_display.insert(tk.END, text + '\n')
    output_display.see(tk.END)

class RedirectText:
    def write(self, string):
        print_to_output_display(string)

    def flush(self):
        pass

sys.stdout = RedirectText()

# 白名单MAC地址列表
allowed_macs = [
    "MAC",

]

root = tk.Tk()
root.geometry("740x440")
root.minsize(740, 440)
root.maxsize(740, 440)
root.title("AWVS 批量扫描_安服摸鱼工具 V2.1.5.4.9")
#root.iconbitmap("logo.ico")

# 定义自定义字体
custom_font = ("Helvetica", 12)

# 创建主菜单栏
menubar = tk.Menu(root)

# 创建配置菜单
config_menu = tk.Menu(menubar, tearoff=0)
config_menu.add_command(label="配置 API 地址", command=lambda: config_window.deiconify())

# 将配置菜单添加到主菜单栏中
menubar.add_cascade(label="配置", menu=config_menu)

# 设置主窗口的菜单栏
root.config(menu=menubar)

# 创建主窗口中的 Frame
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# 以下是主窗口中的内容
# 创建选择文件输入框
url_frame = ttk.Frame(main_frame, padding=10)
url_frame.pack(fill=tk.X, pady=(20, 10))  # 增加上边距，减少下边距

url_label = ttk.Label(url_frame, text="选择需要扫描的 URL 文件：", font=custom_font)
url_label.pack(side=tk.LEFT)

url_file_entry = ttk.Entry(url_frame, width=40, font=custom_font)
url_file_entry.pack(side=tk.LEFT, padx=10)


def browse_urls_file():
    filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
    filepath = filedialog.askopenfilename(title="选择需要扫描的 URL 文件", filetypes=filetypes)
    if filepath:
        # 将文件路径转换为绝对路径
        abs_filepath = os.path.abspath(filepath)
        url_file_entry.delete(0, tk.END)
        url_file_entry.insert(0, abs_filepath)


browse_button = ttk.Button(url_frame, text="选择文件", command=browse_urls_file)
browse_button.pack(side=tk.RIGHT)

# 创建任务名称输入框
description_frame = ttk.Frame(main_frame, padding=10)
description_frame.pack(fill=tk.X, pady=(10, 20))  # 减少上边距，增加下边距

description_label = ttk.Label(description_frame, text="输入任务名称：                     ", font=custom_font)
description_label.pack(side=tk.LEFT, anchor=tk.N)  # 添加 anchor=tk.N 参数使标签向上对齐

description_entry = ttk.Entry(description_frame, width=40, font=custom_font)
description_entry.pack(side=tk.LEFT, padx=10, anchor=tk.N)  # 添加 anchor=tk.N 参数使输入框向上对齐

output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
output_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 创建并使用检查器
checker = MACAddressChecker(allowed_macs)

# 进行MAC地址检查
checker.check_mac_address()

# progress_frame = ttk.Frame(main_frame, padding=10)
# progress_frame.pack(fill=tk.X, pady=10)
#
# progress_label = ttk.Label(progress_frame, text="进度：", font=custom_font)
# progress_label.pack(side=tk.LEFT)
#进度条短期不进行调试增加。
# progress_var = tk.DoubleVar()
# progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
# progress_bar.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
#
# percent_label = ttk.Label(progress_frame, text="", font=custom_font)
# percent_label.pack(side=tk.LEFT, padx=10)

# 创建开始扫描按钮
start_button = ttk.Button(main_frame, text="开始扫描", command=start_scan)
start_button.pack(pady=20)

# 以下是配置窗口的内容
config_window = tk.Toplevel()
config_window.geometry("650x280")
config_window.minsize(650, 280)
config_window.maxsize(650, 280)
config_window.title("配置")

config.setdefault("api_key", "")  # 添加默认值

api_frame = ttk.Frame(config_window, padding=20)
api_frame.pack(fill=tk.X, pady=10)

api_prefix_label = ttk.Label(api_frame, text="API 地址：", font=custom_font)
api_prefix_label.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

api_prefix = config.get("api_prefix", "https://example.com/api/v1")

api_prefix_entry = ttk.Entry(api_frame, width=50, font=custom_font)
api_prefix_entry.insert(0, api_prefix)
api_prefix_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

api_prefix_desc = ttk.Label(api_frame, text="API地址格式：https://example.com/api/v1", font=custom_font)
api_prefix_desc.grid(row=1, column=1, padx=(0, 10), pady=0, sticky="w")

api_key_label = ttk.Label(api_frame, text="API 密钥：", font=custom_font)
api_key_label.grid(row=2, column=0, padx=(0, 10), pady=10, sticky="w")

api_prefix_desc = ttk.Label(api_frame, text="API密钥寻找方法：用户名-用户资料-生成API密钥-复制到对话框",
                            font=custom_font)
api_prefix_desc.grid(row=3, column=1, padx=(0, 10), pady=0, sticky="w")

api_key_entry = ttk.Entry(api_frame, width=50, font=custom_font)
api_key_entry.insert(0, config["api_key"])
api_key_entry.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")

save_button = ttk.Button(config_window, text="保存", command=save_config)
save_button.pack(pady=20)

# 隐藏配置窗口
config_window.withdraw()

root.mainloop()