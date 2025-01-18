import time
import pandas as pd
import os
import pdfplumber
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


from configparser import ConfigParser
 
# 创建解析器对象
m_config = ConfigParser()

# 含税金额
patterns = [
    r'（小写）¥(\d+\.\d{2})',
    r'（小写）￥(\d+\.\d{2})',
    r'\(小写\) ¥(\d+\.\d{2})',
    r'\(小写\) ￥(\d+\.\d{2})',
    
    r'（小写）¥ (\d+\.\d{2})',
    r'（小写）￥ (\d+\.\d{2})',
    r'\(小写\) ¥ (\d+\.\d{2})',
    r'\(小写\) ￥ (\d+\.\d{2})'
]
# 获取发票号和金额
def extract_invoice_data(pdf_path):
    # 定义正则表达式模式
    amount_pattern = r'¥\s*(\d+\.\d{2})' # 非税金额

    with pdfplumber.open(pdf_path) as pdf:
        # 通常情况下，这些信息都在第一页，但可以遍历所有页面以确保正确提取
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # 匹配发票号码
                invoice_number_pattern = re.compile(r'发票号码\s*[:：]\s*(\d+)')
                invoice_number_match = invoice_number_pattern.search(text)
                invoice_code_match = invoice_number_match.group(1) if invoice_number_match else None
                # 如果找不到发票号码，尝试匹配一串20位或12位的数字
                if not invoice_code_match:
                    backup_invoice_number_pattern = re.compile(r'\b\d{20}\b')
                    backup_invoice_number_match = backup_invoice_number_pattern.search(text)
                    invoice_code_match = backup_invoice_number_match.group(0) if backup_invoice_number_match else None
                if not invoice_code_match:
                    backup_invoice_number_pattern = re.compile(r'\b\d{12}\b')
                    backup_invoice_number_match = backup_invoice_number_pattern.search(text)
                    invoice_code_match = backup_invoice_number_match.group(0) if backup_invoice_number_match else None

                if invoice_code_match is None:
                    print(pdf_path + '::发票代码未找到')
                    continue

                # 匹配金额
                amount_match = None
                for p in  patterns :
                    amount_match = re.search(p, text)
                    if amount_match is not None:
                        break

                # 不统计非税金额
                # if amount_match is None:
                    # amount_match = re.search(amount_pattern, text)
                if amount_match is None:
                    print(pdf_path + '::金额未找到')
                    continue

                invoice_code = invoice_code_match
                amount = amount_match.group(1)
                return invoice_code, float(amount)  # 注意这里将金额转换为浮点数

    return None, None


def process_pdf_files(directory_path):
    # 获取目录中的所有文件
    files = [f for f in os.listdir(directory_path) if f.endswith('.pdf')]

    data = []

    # 更新进度条的最大值
    # progress_bar["maximum"] = len(files)

    # 遍历文件列表
    for i, file_name in enumerate(files):
        pdf_path = os.path.join(directory_path, file_name)
        invoice_code, amount = extract_invoice_data(pdf_path)
        # if invoice_code and amount:
        data.append({
                '文件名': file_name,
                '发票号码': invoice_code,
                '金额合计': amount
            })
        # else:
            # print(f"未从文件 {file_name} 中找到有效的发票号码或金额")

        # 更新进度条
        # progress_bar["value"] = i + 1
        # root.update_idletasks()

    # 将数据转换为DataFrame
    df = pd.DataFrame(data)

    # 计算金额合计的总和
    total_amount = df['金额合计'].sum()

    # 创建一个包含总计行的新DataFrame
    summary_row = pd.DataFrame({
        '文件名': ['总计'],
        '发票号码': [''],
        '金额合计': [total_amount]
    })

    # 使用concat函数合并原始DataFrame和总计行
    df = pd.concat([df, summary_row], ignore_index=True)

    # 写入Excel文件
    current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
    out_directory = m_config.get('dir', 'out')
    output_file = os.path.join(out_directory, 'output_'+current_time+'.xlsx')
    df.to_excel(output_file, index=False, engine='openpyxl')

    # 提示完成
    # messagebox.showinfo("完成", f"处理完成！文件已保存为: {output_file}")

def on_button_click():
    select_directory()

def select_directory():
    dir_path = filedialog.askdirectory()
    print("Selected Directory:", dir_path)
    
    entry.delete(0, tk.END)  # 清除输入框中的内容
    entry.insert(0, dir_path)
    
    m_config.set('dir', 'src', dir_path)
    save_config()
    
def on_button_click1():
    select_directory1()

def select_directory1():
    dir_path = filedialog.askdirectory()
    print("Selected Directory:", dir_path)
    
    entry1.delete(0, tk.END)  # 清除输入框中的内容
    entry1.insert(0, dir_path)
    
    m_config.set('dir', 'out', dir_path)
    save_config()

    
def on_button_click2():
    src_dir=entry.get()
    if check_dir(src_dir) == False :
        return
    
    out_dir=entry1.get()
    if check_dir(out_dir) == False :
        return
    
    process_pdf_files(src_dir)
    response = messagebox.askyesno("完成", f"Excel已保存，是否打开文件所在目录？")
    if response == True:
        os.startfile(out_dir)
        
def initWindows():
    entry.insert(0, m_config.get('dir','src'))
    entry1.insert(0, m_config.get('dir','out'))
    
def check_dir(dir_path):
    isOK = False
    # 检查目录是否存在
    if os.path.exists(dir_path):
        # 检查目录是否为一个目录
        if os.path.isdir(dir_path):
            isOK = True

    if isOK == False :
        messagebox.showerror("错误", f"请输入正确的目录")
    
    return isOK

# 读取配置文件
def load_config():
    m_config.read('config.ini')

 # 保存修改后的配置文件
def save_config():
    with open('config.ini', 'w') as config_file:
        m_config.write(config_file)

 # 创建主窗口
root = tk.Tk()
root.title("输入发票PDF文件地址")
#禁止用户调整窗口大小
root.resizable(False,False)

label = tk.Label(root, text="输入PDF目录：")
label.grid(row=0, column=0, padx=10, pady=5)
# 创建目录输入框
entry = tk.Entry(root, width=100, exportselection=False)
entry.grid(row=0, column=1, padx=10, pady=5)

# 创建按钮并放置在输入框后面
button = tk.Button(root, text="...", command=on_button_click)
button.grid(row=0, column=2, padx=10, pady=5)

label1 = tk.Label(root, text="Excel保存的位置：")
label1.grid(row=1, column=0, padx=10, pady=5)
# 创建目录输入框
entry1 = tk.Entry(root, width=100, exportselection=False)
entry1.grid(row=1, column=1, padx=10, pady=5)

# 创建按钮并放置在输入框后面
button1 = tk.Button(root, text="...", command=on_button_click1)
button1.grid(row=1, column=2, padx=10, pady=5)

# 创建按钮并放置在窗口上
button2 = tk.Button(root, text="开始统计", command=on_button_click2)
button2.grid(row=2, column=1, padx=10, pady=5)

def main():
    current_path = os.getcwd()
    print(f"当前工作目录是: {current_path}")
    load_config()
    initWindows()
    # 运行主事件循环
    root.mainloop()

if __name__ == "__main__":
    main()       
