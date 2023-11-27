import os

# 定义要处理的文件夹路径
folder_path = input('Please enter your Sector Path:')

# 遍历文件夹中的文件
for filename in os.listdir(folder_path):
    if filename.endswith('_TWR.asr'): #修改后缀名可实现各种类型文件的操作，修改startswith或endwith可实现以某种文件名开头的文件的处理
        file_path = os.path.join(folder_path, filename)
        
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='gbk', errors='ignore') as file:
            lines = file.readlines()

        # 过滤掉空行
        non_empty_lines = [line for line in lines if line.strip() != '']

        # 打开文件并写入非空行内容
        with open(file_path, 'w', encoding='gbk', errors='ignore') as file:
            file.writelines(non_empty_lines)
print('Mission Complete.')