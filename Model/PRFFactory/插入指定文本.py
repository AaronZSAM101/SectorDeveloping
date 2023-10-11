# 批量写入（在行中操作）
print('Writing Script')
import os

search_path = input('Please enter the root of your sector: ')
target_string = [' '] #引号中输入要在哪行后添加
new_line = [' '] #引号中输入要添加的内容

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith('.prf'): #修改后缀名可实现各种类型文件的操作，修改startswith或endwith可实现以某种文件名开头的文件的处理
            file_path = os.path.join(root, file)
            updated_lines = []
            with open(file_path, 'r', errors='ignore') as f:
                lines = f.readlines()
                for line in lines:
                    updated_lines.append(line)
                    if all(item in line for item in target_string):
                        updated_lines.append(''.join(new_line) + '\n')

            with open(file_path, 'w', errors='ignore') as f:
                f.writelines(updated_lines)
print('Mission Complete.')