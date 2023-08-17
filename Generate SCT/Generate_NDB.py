import sqlite3
import os
# 读取数据库
## 打开数据库连接
DATABASEadress = input("Database Adress:")
conn = sqlite3.connect(DATABASEadress)
cursor = conn.cursor()
## 读取相关数据
cursor.execute('SELECT CODE_ID, VAL_FREQ, GEO_LAT_ACCURACY, GEO_LONG_ACCURACY FROM NDB ORDER BY CODE_ID')
NDBdata = cursor.fetchall()
## 关闭数据库连接
conn.close()

# 写入原生文件
## 将读取后的结果转换为string类型
NDBnewdata = ""
for i in NDBdata:
    NDBnewdata += f"{i[0]} {i[1]} {i[2]} {i[3]}\n"
## 将读取后的结果写入NDB.txt文件
with open('NDB.txt', 'w', encoding='utf-8') as f:
    f.write('[NDB]\n' + NDBnewdata)

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
print('NDB文件生成完毕，按任意键退出！')