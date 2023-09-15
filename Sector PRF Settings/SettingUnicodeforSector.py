# 修改扇区编码集
# 无法确保你之前写了中文之后再用该脚本转换时所有的中文字符是否能够保留
# 所以，请时刻谨记，编辑任何扇区文件时，均使用GBK编码集进行编辑。
import os

folder_path = input('Please enter the root of your sector: ')

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.prf'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                with open(file_path, 'w', encoding='gbk') as f:
                    f.write(content)

                print(f"Modified encoding for file: {file_path}")
            except Exception as e:
                print(f"Error occurred while modifying encoding for file: {file_path}")
                print(str(e))
input('Mission Completed.')