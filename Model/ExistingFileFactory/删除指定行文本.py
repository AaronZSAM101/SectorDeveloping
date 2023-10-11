import os

# 定义要处理的文件夹路径
folder_path = input('Please enter your Sector Path:')

# 获取文件夹中所有以.prf为后缀的文件
file_list = [f for f in os.listdir(folder_path) if f.endswith('_TWR.prf')]

# 遍历每个文件
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    
    # 打开文件并读取内容
    with open(file_path, 'r', errors='ignore') as file:
        lines = file.readlines()
    
    # 删除第5至第56行内容
    del lines[31:51]  # 注意：这里索引从0开始，即：第一行为0，第二行为1，以此类推
    
    # 再次打开文件并写入修改后的内容
    with open(file_path, 'w', errors='ignore') as file:
        file.writelines(lines)

print("删除操作已完成。")