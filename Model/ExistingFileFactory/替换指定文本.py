# 修改已存在文件指向
print('Replacing Script')
import os

search_path = input('Please Enter the sector path:')
target_strings = [
' ' #引号中输入要替换的文本
]
replacement_strings = [
' ' # 引号中输入待替换的文本
]

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith('.txt'): #修改后缀名可实现各种类型文件的操作，修改startswith或endwith可实现以某种文件名开头的文件的处理
            file_path = os.path.join(root, file)
            updated_lines = []
            with open(file_path, 'r', encoding='gbk', errors='ignore') as f:
                lines = f.readlines()
                for line in lines:
                    updated_line = line
                    for target_string, replacement_string in zip(target_strings, replacement_strings):
                        if target_string in line:
                            updated_line = line.replace(target_string, replacement_string)
                            break
                    updated_lines.append(updated_line)

            with open(file_path, 'w', encoding='gbk', errors='ignore') as f:
                f.writelines(updated_lines)
print('Mission Complete.')