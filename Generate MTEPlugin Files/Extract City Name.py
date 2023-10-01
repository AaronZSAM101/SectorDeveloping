# 打开输入文件和输出文件
with open('input.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    # 创建一个集合来存储唯一的文本
    unique_text = set()

    # 逐行读取输入文件
    for line in input_file:
        # 去除行末尾的换行符
        line = line.strip()
        
        # 将文本添加到集合中
        unique_text.add(line)

    # 将唯一的文本写入输出文件
    for text in unique_text:
        output_file.write(f'{text}\n')

input('done.')