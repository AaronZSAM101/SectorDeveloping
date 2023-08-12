import sqlite3
import re
import csv
import os
# 读取数据库
## 打开数据库连接
DATABASEadress = input("Database Adress:")
conn = sqlite3.connect(DATABASEadress)
cursor = conn.cursor()
## 读取表AD_HP的AD_HP_ID、CODE_ID、TXT_NAME
cursor.execute('SELECT AD_HP_ID, CODE_ID, TXT_NAME FROM AD_HP')
ad_hp_data = cursor.fetchall()
## 读取表RWY的RWY_ID、AD_HP_ID、CODE_AIRPORT
cursor.execute('SELECT RWY_ID, AD_HP_ID FROM RWY')
rwy_data = cursor.fetchall()
## 读取表RWY_DIRECTION的RWY_ID、TXT_DESIG、VAL_MAG_BRG、GEO_LAT、GEO_LONG
cursor.execute('SELECT RWY_ID, TXT_DESIG, VAL_MAG_BRG, GEO_LAT, GEO_LONG FROM RWY_DIRECTION')
rwy_direction_data = cursor.fetchall()
## 关闭数据库连接
conn.close()

# 创建字典、拼合数据库数据
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
# 将输出写入csv文件
with open('output.csv', 'w', encoding='utf-8') as f:
    for key, value in dic_total.items():
        tmpend=value[1:9]+value[10:]
        for dt in tmpend:
            f.write(dt+',')
        f.write('\n')

# 坐标转换
## 以utf-8字符集打开csv文件
with open('output.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    data = list(csv_reader)
## 根据机场ICAO进行排序
sorted_data = sorted(data, key=lambda row: row[8])
## 将排序后的数据写入rwy.txt文件
with open('output.txt', 'w', encoding='utf-8') as txt_file:
    for row in sorted_data:
        txt_file.write(' '.join(row) + '\n')
print("第一次排序完成")

# 数据整理
## 删除军用机场
def contains_chinese(text):
    # 使用正则表达式检查文本是否包含中文字符
    return bool(re.search('[\u4e00-\u9fff]', text))
## 删除无外键匹配机场
with open('output.txt', 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()
filtered_lines = [line for line in lines if ('N' in line or 'E' in line) and contains_chinese(line)]
## 打开输出文件并将过滤后的行写入
with open('output.txt', 'w', encoding='utf-8') as output_file:
    output_file.writelines(filtered_lines)
print("多余数据删除完成")

# 转换坐标
## 定义ES格式切片
def convert_coordinates(coord_str, format):
    if format == "lat":
        degree = int(coord_str[:2])
        minute = int(coord_str[2:4])
        seconds = float(coord_str[4:])
    else:
        degree = int(coord_str[:3])
        minute = int(coord_str[3:5])
        seconds = float(coord_str[5:])
    return f"{degree:03d}.{minute:02d}.{seconds:06.3f}"
## 切片后数据拼合
input_filename = "output.txt"
output_filename = "rwy.txt"
with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []

        for part in parts:
            if part.startswith("N"):
                converted_part = convert_coordinates(part[1:], "lat")
                converted_parts.append(part[0] + converted_part)
            elif part.startswith("E"):
                converted_part = convert_coordinates(part[1:], "lon")
                converted_parts.append(part[0] + converted_part)
            else:
                converted_parts.append(part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")

## 多跑道机场排序
outputtxt = open('rwy.txt', 'r', encoding='utf-8')
data = outputtxt

def custom_sort_key(line):
    parts = line.split()
    return (parts[8], int(parts[0][:2]), parts[0][-1])

sorted_data = sorted(data, key=custom_sort_key)
print('第二次排序完成')
## 删除不必要的文件
os.remove('output.txt')
os.remove('output.csv')

# 添加澳门跑道
VMMC_Runway = '''[RUNWAY]\n;NOT IN DATABASE\n16 34 164 344 N022.09.38.311 E113.35.14.139 N022.08.17.458 E113.35.43.911 VMMC 澳门\n01 19 014 194 N023.04.16.054 E113.04.06.233 N023.05.45.236 E113.04.26.242 ZGFS 佛山\n;IN DATABASE\n'''
with open('rwy.txt', 'r+', encoding='utf-8') as file:
    DATABASEcontent = "".join(sorted_data)
    file.seek(0,0)
    file.write(VMMC_Runway + DATABASEcontent)
input("跑道文件生成成功！按任意键退出")