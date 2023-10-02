import re

# 打开文件以读取内容
with open('China_Callsign.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# 使用正则表达式删除英文逗号前的多个空格
modified_content = re.sub(r'\s*,', ',', content)

# 将修改后的内容写回文件
with open('China_Callsign.txt', 'w', encoding='utf-8') as file:
    file.write(modified_content)
print('done.')