import os

folder_path = input('Please enter the root of your sector: ')

text_to_append = '''
PLUGIN:TopSky plugin:HideMapData:GROUND
'''
#上方引号中输入需要添加的内容
# 获取文件夹内所有以.prf为后缀名的文件
file_list = [file for file in os.listdir(folder_path) if file.endswith('_TWR.asr')] #修改后缀名可实现各种类型文件的操作，修改startswith或endwith可实现以某种文件名开头的文件的处理

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    
    try:
        # 在文件末尾追加文本内容
        with open(file_path, 'a', encoding='gbk', errors='ignore') as file: #默认在文本末尾添加内容
            file.write(text_to_append)
        
        print(f"Appended content to file: {file_name}")
    
    except Exception as e:
        print(f"Failed to append content to file: {file_name}. Error: {str(e)}")

print("Mission Complete.")