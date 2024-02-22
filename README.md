[英文][English](README_EN.md)

# AWVS自动化批量扫描和报告工具

AWVS自动化批量扫描和报告工具是一个基于Python的应用，旨在为使用AWVS（Acunetix Web Vulnerability Scanner）的安全研究人员提供自动化的扫描和报告生成能力。该工具特别适用于需要对多个目标进行安全评估的场景，通过自动化流程显著提高工作效率。

## 项目介绍

本项目是一个探索性的尝试，旨在实验深度学习模型在自动化生成可用代码方面的潜力。通过这个项目，我们希望能够展示人工智能在软件开发领域的应用前景，特别是在提高开发效率和促进创新思维方面的可能性。

目前，项目中的代码已经经过了人工微调，以确保其实用性和有效性。我们鼓励社区成员参与进来，提出建议，共同推动项目的发展。

## 项目背景

本项目的开发背景颇具戏剧性，起源于甲方和我们公司之间的一系列冷嘲热讽。在这个过程中，双方都表现出了对人工智能和自动化程序的抵制态度。然而，正是这种看似不利的环境激发了我们探索AI在软件开发中应用的决心。

我们认为，通过实践和探索，可以更好地理解AI技术的潜力和限制，进而引导技术的健康发展。因此，尽管遭遇了外界的质疑和反对，我们仍然坚持开展这个项目，希望能够为科技和社会带来积极的影响。

## 安装步骤

确保您的系统满足以下前提条件：

* Windows操作系统
* Python 3.6或更高版本
执行以下步骤来安装和配置工具：

1. 克隆仓库到本地或下载源代码压缩包。
```plain
git clone https://github.com/tiger652814/AWVS_fished.git
```
2. 打开命令行界面，切换到项目目录。
3. 运行`pip install -r requirements.txt`来安装所需的Python依赖包。
```plain
pip install -r requirements.txt
```
4. **更新本机MAC地址**：根据代码中的说明更新您的MAC地址信息，以确保程序能正常运行。请在`gui.py`和`mac_checker.py`中找到`allowed_macs`列表并添加您的MAC地址。
```plain
# 白名单MAC地址列表
allowed_macs = [
    "MAC",
]
```
5. 在main_program.py中找到中找到
```plain
generate_tjdx_report(filtered_vulns, f"{safe_task_description}【想修改的名称】渗透报告+表格")
print("【想修改的名称】版漏洞报告生成完毕。")
```
便可以修改成想要的名称。
6. 运行`python gui.py`来启动图形用户界面。

## window运行程序打包教程

1. 上述操作全部进行完毕后，使用pyinstaller工具进行打包。
2. 执行命令安装pyinstaller工具
```plain
pip install pyinstaller
```
3. 安装完毕后在项目的目录中执行命令：
```plain
pyinstaller --onefile --windowed --icon=logo.ico --add-data "word_TJDX.py;." gui.py
```
4. 在项目目录中dist文件中找到生产后的gui.exe文件，

## 使用说明

1. 在图形界面中，选择包含目标URL的txt文件目录。
2. 确认您的扫描参数和报告选项。
3. 点击“开始扫描”按钮以启动扫描过程。
4. 扫描完成后，您可以在指定的输出目录中找到生成的报告。

## 许可

本项目采用[自定义许可证](LICENSE)。使用本工具前，请确保您的使用目的和方式符合许可证条款以及相关法律法规。

## 贡献

我们欢迎并鼓励社区成员对项目进行贡献，无论是通过提交bug报告、请求新功能，还是创建拉取请求来改进代码。

