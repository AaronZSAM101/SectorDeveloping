# 打开文本文件以读取内容
with open('your_file.txt', 'r') as file:
    lines = file.readlines()

# 提取每行的前两个字符并存储在一个列表中
prefixes = [line[:2] for line in lines]

# 使用集合(set)来去重复并保留唯一的前两个字符
unique_prefixes = list(set(prefixes))

# 在唯一的前两个字符周围加上引号，并每行排列10个
result = ''
for i, prefix in enumerate(unique_prefixes, start=1):
    result += f'"{prefix}",'
    if i % 10 == 0:
        result += '\n'
    else:
        result += ' '

# 打印结果
print(result)