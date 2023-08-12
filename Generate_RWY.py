import sqlite3
import re
import csv
import os
# 打开数据库连接
DATABASEadress = input("Database Adress:")
conn = sqlite3.connect(DATABASEadress)
cursor = conn.cursor()

# 读取表AD_HP的AD_HP_ID、CODE_ID、TXT_NAME
cursor.execute('SELECT AD_HP_ID, CODE_ID, TXT_NAME FROM AD_HP')
ad_hp_data = cursor.fetchall()

# 读取表RWY的RWY_ID、AD_HP_ID、CODE_AIRPORT(暂时去除看效果)
cursor.execute('SELECT RWY_ID, AD_HP_ID FROM RWY')
rwy_data = cursor.fetchall()

# 读取表RWY_DIRECTION的RWY_ID、TXT_DESIG、VAL_MAG_BRG、GEO_LAT、GEO_LONG
cursor.execute('SELECT RWY_ID, TXT_DESIG, VAL_MAG_BRG, GEO_LAT, GEO_LONG FROM RWY_DIRECTION')
rwy_direction_data = cursor.fetchall()

# 关闭数据库连接
conn.close()

# 创建字典
dic_ad_hp={}
dic_rwy={}
dic_rwy_direction={}
dic_total={}
for ad_hp in ad_hp_data:
    tmp=ad_hp[0]
    ad_hp=ad_hp[1:]
    dic_ad_hp[tmp]=ad_hp
for rwy in rwy_data:
    if rwy[1] in dic_ad_hp:
        data=dic_ad_hp[rwy[1]]
    else:
        data=()
    tmp=rwy[0]
    rwy=rwy[1:]
    dic_rwy[tmp]=rwy+data
for rwy_direction in rwy_direction_data:
    if rwy_direction[0] in dic_rwy:
        data=dic_rwy[rwy_direction[0]]
    else:
        data=()
    tmp=rwy_direction[0]
    rwy_direction=rwy_direction[0:]
    if tmp in dic_total:
        dic_total[tmp]=dic_total[tmp][:2]+rwy_direction[1:2]+dic_total[tmp][2:3]+rwy_direction[2:3]+dic_total[tmp][3:5]+rwy_direction[3:5]+dic_total[tmp][5:]
    else:
        dic_total[tmp]=rwy_direction+data
# 将输出写入txt文件
with open('output.csv', 'w', encoding='utf-8') as f:
    for key, value in dic_total.items():
        tmpend=value[1:9]+value[10:]
        for dt in tmpend:
            f.write(dt+',')
        f.write('\n')
# 以utf-8字符集打开csv文件
with open('output.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    data = list(csv_reader)
# 根据第九列的内容进行排序
sorted_data = sorted(data, key=lambda row: row[8])
# 将排序后的数据写入txt文件
with open('output.txt', 'w', encoding='utf-8') as txt_file:
    for row in sorted_data:
        txt_file.write(' '.join(row) + '\n')
print("排序完成")
os.remove('output.csv')

def contains_chinese(text):
    # 使用正则表达式检查文本是否包含中文字符
    return bool(re.search('[\u4e00-\u9fff]', text))

# 打开输入文件
with open('output.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

# 过滤不包含 'N'、'E' 的行且包含中文字符的行
filtered_lines = [line for line in lines if ('N' in line or 'E' in line) and contains_chinese(line)]

# 打开输出文件并将过滤后的行写入
with open('output.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(filtered_lines)

print("多余数据删除完成")


with open('output.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()
latdd=int(str[1:3])
latmm=int(str[3:5])
latss=round(float(str[5:]),3)
longdd=int(str[1:3])
longmm=int(str[3:5])
longss=round(float(str[5:]),3)
EuroScopeFormat=f"{str[0]}N{latdd}.{latmm}.{latss} E{longdd}.{longmm}.{longss}"

with open('rwy.txt', 'w', encoding='gbk') as output_file:

        new_coord = f'{EuroScopeFormat}'
        output_file.write(new_coord + '\n')

print("坐标已转换并保存到rwy.txt文件中。")
