[中文][Chinese](README.md)

# AWVS Automated Batch Scanning and Reporting Tool

The AWVS Automated Batch Scanning and Reporting Tool is a Python-based application designed to provide security researchers using AWVS (Acunetix Web Vulnerability Scanner) with automated scanning and report generation capabilities. This tool is particularly suitable for scenarios that require security assessments of multiple targets, significantly improving work efficiency through automation.

## Project Introduction

This project is an exploratory attempt to experiment with the potential of deep learning models in automating code generation. Through this project, we aim to showcase the application prospects of artificial intelligence in software development, especially in enhancing development efficiency and promoting innovative thinking.

Currently, the code in the project has been manually fine-tuned to ensure its practicality and effectiveness. We encourage community members to get involved, make suggestions, and jointly push the development of the project.

## Project Background

The development background of this project is quite dramatic, originating from a series of sarcasms between a client and our company. In this process, both parties exhibited resistance to artificial intelligence and automated programs. However, it was this seemingly unfavorable environment that inspired our determination to explore the application of AI in software development.

We believe that through practice and exploration, we can better understand the potential and limitations of AI technology, thereby guiding its healthy development. Therefore, despite facing skepticism and resistance from the outside world, we are committed to advancing our exploration.

## Installation Steps

Ensure your system meets the following prerequisites:

- Windows operating system
- Python 3.6 or higher version

Follow these steps to install and configure the tool:

1. Clone the repository to your local machine or download the source code zip package.
```plain
git clone https://github.com/tiger652814/AWVS_fished.git
```
2. Open the command line interface and switch to the project directory.
3. Run `pip install -r requirements.txt` to install the required Python dependencies.
```plain
pip install -r requirements.txt
```
4. **Update Local MAC Address**: Update your MAC address information according to the instructions in the code to ensure the program runs correctly. Find the `allowed_macs` list in `gui.py` and `mac_checker.py` and add your MAC address.
```plain
# Whitelist of MAC addresses
allowed_macs = [
    "MAC",
]
```
5. In `main_program.py`, you can find and modify
```plain
generate_tjdx_report(filtered_vulns, f"{safe_task_description}【desired name】Penetration Report+Table")
print("【desired name】version vulnerability report generated.")
```
to change it to the desired name.
6. Run `python gui.py` to launch the graphical user interface.

## Windows Program Packaging Tutorial

1. After completing all the above operations, use the pyinstaller tool for packaging.
2. Execute the command to install the pyinstaller tool
```plain
pip install pyinstaller
```
3. After installation, execute the command in the project directory:
```plain
pyinstaller --onefile --windowed --icon=logo.ico --add-data "word_TJDX.py;." gui.py
```
4. Find the produced `gui.exe` file in the dist folder within the project directory.

## Usage Instructions

1. In the graphical interface, select the directory of the txt file containing the target URLs.
2. Confirm your scan parameters and report options.
3. Click the "Start Scan" button to initiate the scanning process.
4. After the scan is completed, you can find the generated report in the designated output directory.

## License

This project is licensed under the [MIT License](LICENSE). Before using this tool, ensure your use complies with the license terms as well as applicable laws and regulations.

## Contributions

We welcome and encourage community members to contribute to the project, whether by submitting bug reports, requesting new features, or creating pull requests to improve the code.
