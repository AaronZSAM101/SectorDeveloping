import sqlite3
import re
import csv
import os
import time

AIRAC_CYCLE=input('请输入当前期号，（例：2308）:')
#region 读取数据库
## 打开数据库连接
DATABASEaddress = input("Database Address:")
#FOR TEST: 开始计算代码执行时间
start_time = time.time()
conn = sqlite3.connect(DATABASEaddress)
cursor = conn.cursor()
## 读取相关数据
### 读取NDB数据
cursor.execute('SELECT CODE_ID, VAL_FREQ, GEO_LAT_ACCURACY, GEO_LONG_ACCURACY FROM NDB ORDER BY CODE_ID')
NDBdata = cursor.fetchall()
### 读取VOR数据
cursor.execute('SELECT CODE_ID, VAL_FREQ, GEO_LAT_ACCURACY, GEO_LONG_ACCURACY FROM VOR ORDER BY CODE_ID')
VORdata = cursor.fetchall()
### 读取机场数据
cursor.execute('''SELECT CODE_ID,GEO_LAT_ACCURACY,GEO_LONG_ACCURACY,round(VAL_ELEV*3.281, 3) AS 'VAL_ELEV_FEET' 
               FROM AD_HP 
               WHERE 
               not (CODE_ID = '' OR CODE_ID = 'VHHH' OR CODE_ID = 'VMMC' )
               ORDER BY CODE_ID;
               ''')
ADdata = cursor.fetchall()
### 读取跑道数据
#### 读取表AD_HP的AD_HP_ID、CODE_ID、TXT_NAME
cursor.execute('''SELECT AD_HP_ID, CODE_ID, TXT_NAME FROM AD_HP 
               WHERE not (CODE_ID = 'ZULS')''')
AD_HP_data = cursor.fetchall()
#### 读取表RWY的RWY_ID、AD_HP_ID、CODE_AIRPORT
cursor.execute('''SELECT RWY_ID, AD_HP_ID FROM RWY
               WHERE not (RWY_ID = '5b26e8f1-a3fb-45d5-80fc-5ea5ae44bac1')''')
RWY_data = cursor.fetchall()
#### 读取表RWY_DIRECTION的RWY_ID、TXT_DESIG、VAL_MAG_BRG、GEO_LAT、GEO_LONG
cursor.execute('''SELECT RWY_ID, TXT_DESIG, VAL_MAG_BRG, GEO_LAT, GEO_LONG FROM RWY_DIRECTION
               WHERE not (RWY_ID = '5b26e8f1-a3fb-45d5-80fc-5ea5ae44bac1')''')
RWY_DIRECTION_data = cursor.fetchall()
### 读取点坐标数据
cursor.execute('''SELECT CODE_ID, GEO_LAT_ACCURACY, GEO_LONG_ACCURACY FROM DESIGNATED_POINT WHERE CODE_TYPE = '五字代码点' OR CODE_TYPE = 'P字点' ORDER BY CODE_ID;
               ''')
FIXdata = cursor.fetchall()
### 读取航路数据
cursor.execute('''SELECT GEO_LAT_START_ACCURACY, GEO_LONG_START_ACCURACY, GEO_LAT_END_ACCURACY, GEO_LONG_END_ACCURACY, TXT_DESIG 
               FROM RTE_SEG 
               WHERE
               ( TXT_DESIG NOT LIKE '%XX%' AND TXT_DESIG NOT LIKE '%FANS%' ) 
               ORDER BY TXT_DESIG;
               ''')
RTEdata = cursor.fetchall()
## 关闭数据库连接
conn.close()
#endregion 读取数据库

#region 定义坐标转换
# 定义ES格式切片
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
#endregion

#region 生成NDB文件
# 写入原生文件
#（将读取后的结果转换为string类型）
NDBnewdata = ""
for i in NDBdata:
    NDBnewdata += f"{i[0]} {i[1]} {i[2]} {i[3]}\n"
## 将读取后的结果写入NDB.txt文件
with open('NDB.txt', 'w', encoding='utf-8') as f:
    f.write('[NDB]\n' + NDBnewdata)
## 切片后数据拼合
input_filename = "NDB.txt"
output_filename = "NDBoutput.txt"
with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []
        for part in parts:
            try:
                if part.startswith("N") and len(part) > 3:
                    converted_part = convert_coordinates(part[1:], "lat")
                    converted_parts.append(part[0] + converted_part)
                elif part.startswith("E") and len(part) > 3:
                    converted_part = convert_coordinates(part[1:], "lon")
                    converted_parts.append(part[0] + converted_part)
                else:
                    converted_parts.append(part)
            except Exception as e:
                print(e, part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")
# 整理文件
os.remove('NDB.txt')
os.rename('NDBoutput.txt', 'NDB.txt')
print('NDB文件生成完毕')
#endregion

#region 生成VOR文件
# 写入原生文件
#（将读取后的结果转换为string类型）
VORnewdata = ""
for i in VORdata:
    VORnewdata += f"{i[0]} {i[1]} {i[2]} {i[3]}\n"
## 将读取后的结果写入VOR.txt文件
with open('VOR.txt', 'w', encoding='utf-8') as f:
    f.write('[VOR]\n' + VORnewdata)
## 切片后数据拼合
input_filename = "VOR.txt"
output_filename = "VORoutput.txt"
with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []
        for part in parts:
            try:
                if part.startswith("N") and len(part) > 3:
                    converted_part = convert_coordinates(part[1:], "lat")
                    converted_parts.append(part[0] + converted_part)
                elif part.startswith("E") and len(part) > 3:
                    converted_part = convert_coordinates(part[1:], "lon")
                    converted_parts.append(part[0] + converted_part)
                else:
                    converted_parts.append(part)
            except Exception as e:
                print(e, part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")
# 整理文件
os.remove('VOR.txt')
os.rename('VORoutput.txt', 'VOR.txt')
print('VOR文件生成完毕')
#endregion

#region 生成机场坐标文件
# 写入原生文件
## 将读取后的结果转换为string类型
ADnewdata = ""
for i in ADdata:
    ADnewdata += f"{i[0]} {i[3]} {i[1]} {i[2]} D\n"
## 将读取后的结果写入VOR.txt文件
with open('AD.txt', 'w', encoding='utf-8') as f:
    f.write('[AIRPORT]\n' + ADnewdata)

# 坐标转换
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
input_filename = "AD.txt"
output_filename = "ADoutput.txt"
with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []
        for part in parts:
            try:
                if part.startswith("N"):
                    converted_part = convert_coordinates(part[1:], "lat")
                    converted_parts.append(part[0] + converted_part)
                elif part.startswith("E"):
                    converted_part = convert_coordinates(part[1:], "lon")
                    converted_parts.append(part[0] + converted_part)
                else:
                    converted_parts.append(part)
            except Exception as e:
                print(e, part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")

# 整理文件
os.remove('AD.txt')
os.rename('ADoutput.txt', 'AD.txt')
print('机场坐标文件生成完毕')
#endregion

#region 生成跑道文件
# 创建字典、拼合数据库数据
dic_ad_hp={}
dic_rwy={}
dic_rwy_direction={}
dic_total={}
for AD_HP in AD_HP_data:
    tmp=AD_HP[0]
    AD_HP=AD_HP[1:]
    dic_ad_hp[tmp]=AD_HP
for rwy in RWY_data:
    if rwy[1] in dic_ad_hp:
        data=dic_ad_hp[rwy[1]]
    else:
        data=()
    tmp=rwy[0]
    rwy=rwy[1:]
    dic_rwy[tmp]=rwy+data
for rwy_direction in RWY_DIRECTION_data:
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
## 将排序后的数据写入RWY.txt文件
with open('output.txt', 'w', encoding='utf-8') as txt_file:
    for row in sorted_data:
        txt_file.write(' '.join(row) + '\n')

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
output_filename = "RWY.txt"
input_file = open(input_filename, "r", encoding='utf-8')
output_file = open(output_filename, "w", encoding='utf-8')
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
output_file.close()
input_file.close()

## 多跑道机场排序
outputtxt = open('RWY.txt', 'r', encoding='utf-8')
data = outputtxt

def custom_sort_key(line):
    parts = line.split()
    return (parts[8], int(parts[0][:2]), parts[0][-1])

sorted_data = sorted(data, key=custom_sort_key)
## 删除不必要的文件
os.remove('output.txt')
os.remove('output.csv')

# 手动添加一些跑道
Append_Runway = '''[RUNWAY]\n;NOT IN DATABASE\n16 34 164 344 N022.09.38.311 E113.35.14.139 N022.08.17.458 E113.35.43.911 VMMC 澳门\n01 19 014 194 N023.04.16.054 E113.04.06.233 N023.05.45.236 E113.04.26.242 ZGFS 佛山\n;DATABASE DATA WRONG\n09L 27R 089 269 N029.17.51.940 E090.53.30.000 N029.17.54.130 E090.55.58.110 ZULS 拉萨/贡嘎\n;IN DATABASE\n'''
file = open('RWY.txt', 'w', encoding='gbk')
DATABASEcontent = "".join(sorted_data)
file.write(Append_Runway + DATABASEcontent)
file.close()
print("跑道文件生成完毕")
#endregion

#region 生成点坐标文件
# 写入原生文件
## 将读取后的结果转换为string类型
FIXnewdata = ""
for i in FIXdata:
    FIXnewdata += f"{i[0]} {i[1]} {i[2]}\n"
## 将读取后的结果写入FIX.txt文件
with open('FIX.txt', 'w', encoding='utf-8') as f:
    f.write('[FIX]\n' + FIXnewdata)
    ## 切片后数据拼合
input_filename = "FIX.txt"
output_filename = "FIXoutput.txt"
with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []
        for part in parts:
            try:
                if part.startswith("N") and len(part) > 5:
                    converted_part = convert_coordinates(part[1:], "lat")
                    converted_parts.append(part[0] + converted_part)
                elif part.startswith("E") and len(part) > 5:
                    converted_part = convert_coordinates(part[1:], "lon")
                    converted_parts.append(part[0] + converted_part)
                else:
                    converted_parts.append(part)
            except Exception as e:
                print(e, part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")

# 整理文件
os.remove('FIX.txt')
os.rename('FIXoutput.txt', 'FIX.txt')
print('航路点坐标（不含地名点、航路PBN点）文件生成完毕')
#endregion

#region 生成航路文件
# 写入原生文件
## 将读取后的结果转换为string类型
RTEnewdata = ""
for i in RTEdata:
    RTEnewdata += f"{i[4]} {i[0]} {i[1]} {i[2]} {i[3]}\n"
## 将读取后的结果写入FIX.txt文件
with open('RTE.txt', 'w', encoding='utf-8') as f:
    f.write('[HIGH WAY]\n' + RTEnewdata)
## 切片后数据拼合
input_filename = "RTE.txt"
output_filename = "RTEoutput.txt"
with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []
        for part in parts:
            try:
                if part.startswith("N") and len(part) > 4:
                    # len(part) > 4 的原因是N892
                    converted_part = convert_coordinates(part[1:], "lat")
                    converted_parts.append(part[0] + converted_part)
                elif part.startswith("E"):
                    converted_part = convert_coordinates(part[1:], "lon")
                    converted_parts.append(part[0] + converted_part)
                else:
                    converted_parts.append(part)
            except Exception as e:
                print(e, part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")

# 整理文件
os.remove('RTE.txt')
os.rename('RTEoutput.txt', 'RTE.txt')
print('航路文件生成完毕')
#endregion

#region 合并所有文件
file_names = ["NDB.txt", "VOR.txt",  "AD.txt", "FIX.txt", "RTE.txt", "RWY.txt"]
output_file_name = f"{AIRAC_CYCLE} ES.txt"

output_file = open(output_file_name, "w", encoding='gbk')
for file_name in file_names:
    f = open(file_name, "r", encoding='gbk')
    output_file.write(f.read())
    f.close()
    # os.remove(file_name)
output_file.close()
#endregion

#FOR TEST: 结束计算代码执行时间
end_time = time.time()
execution_time = end_time - start_time

input(f'{AIRAC_CYCLE}期扇区数据生成完毕，总用时{execution_time:.2f}秒.')