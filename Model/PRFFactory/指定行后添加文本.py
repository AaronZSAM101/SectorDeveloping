import os

# 定义要处理的文件夹路径
folder_path = input('File Path:')

# 获取要添加的内容
with open((os.path.join(folder_path, 'append.txt')), 'r', encoding='utf-8', errors='ignore') as append_file:
    append_content = append_file.read()

# 获取文件夹中所有以.prf为后缀的文件
file_list = [f for f in os.listdir(folder_path) if f.endswith('.prf')]

# 遍历每个文件
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    
    # 打开文件并读取内容
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # 在第四行之后插入要添加的内容
    lines.insert(3, append_content)  # 注意：这里索引从0开始
    
    # 再次打开文件并写入修改后的内容
    with open(file_path, 'w') as file:
        file.writelines(lines)

print("添加操作已完成。")