import sys
import uuid
import tkinter as tk
from tkinter import messagebox

class MACAddressChecker:
    def __init__(self, allowed_mac_addresses):
        self.allowed_mac_addresses = [addr.lower().replace('-', ':') for addr in allowed_mac_addresses]

    def get_physical_mac_addresses(self):
        mac_addresses = []
        mac = uuid.getnode()
        mac_address = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2)).lower()
        mac_addresses.append(mac_address)
        return mac_addresses

    def check_mac_address(self):
        physical_macs = self.get_physical_mac_addresses()
        print("物理 MAC 地址列表:", physical_macs)
        if not any(mac in self.allowed_mac_addresses for mac in physical_macs):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("错误", "此设备不在允许的列表中，程序将退出。")
            root.destroy()
            sys.exit()

# 示例使用
allowed_macs = [
    "MAC",  # 示例MAC地址，请替换为实际允许的MAC地址
]
checker = MACAddressChecker(allowed_macs)
checker.check_mac_address()
