import sqlite3
import os
from pypinyin import pyyin, Sytle
#region 从数据库读取数据
## 打开数据库连接
DATABASEaddress = input("Database Address:")
conn = sqlite3.connect(DATABASEaddress)
cursor = conn.cursor()
## 读取相关数据
cursor.execute('''SELECT CODE_ID, TXT_NAME FROM AD_HP 
               WHERE NOT(CODE_TYPE_MIL_OPS = 'MA' OR CODE_ID = 'VHHH' OR CODE_ID = 'VMMC')
               ORDER BY CODE_ID;
               ''')
ADdata = cursor.fetchall()
## 关闭数据库连接
conn.close
#endregion

#region 导出结果
ADNewdata=""
for i in ADdata:
    ADNewdata=f"{i[0]} {i[1]}\n"
#endregion

#region 删除原生ICAO_Airports.txt 中 的国内机场
with open('ICAO_Airports.txt', 'r', encoding='utf-8') as f:
    lines=f.readlines()
filtered_lines = []
for line in lines:
    if line[:2] not in ['ZB', 'ZG', 'ZH','ZJ', 'ZL', 'ZP', 'ZS', 'ZU', 'ZW', 'ZY']:
        filtered_lines.append(lines)

with open('ICAO_Airports_New.txt', 'w', encoding='utf-8') as f:
    f.writelines(filtered_lines)
#endregion

#region 定义中文转拼音
def convert_to_pinyin(text):
    # 使用 pinyin 函数将中文文本转换为拼音列表
    pinyin_list = pinyin(text, style=STYLE.NORMAL)
    
    # 从拼音列表中提取首字母并转换为大写，然后拼接成一个字符串
    pinyin_text = ''.join([p[0] for p in pinyin_list]).upper()
    return pinyin_text

# 输入中文文本，包含斜杠分隔的多个词
input_text = "北京/大兴"

# 将输入文本按斜杠分隔成多个词，并逐个转换为拼音
converted_text = '/'.join([convert_to_pinyin(word) for word in input_text.split('/')])

# 打印转换后的拼音文本
print(converted_text)
#endregion