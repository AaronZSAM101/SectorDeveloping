import sqlite3
import os
import time
#region 读取数据库中的中国大陆机场
## 打开数据库连接
AIRAC_CYCLE = input('当前周期号:')
DATABASEaddress = input("Database Address:")
conn = sqlite3.connect(DATABASEaddress)
cursor = conn.cursor()
## 读取相关数据
cursor.execute('''SELECT
	CODE_ID,
	GEO_LAT_ACCURACY,
	GEO_LONG_ACCURACY,
	TXT_NAME
FROM
	AD_HP 
WHERE
	NOT ( CODE_TYPE_MIL_OPS = 'MA' OR CODE_ID = 'VHHH' OR CODE_ID = 'VMMC' ) 
ORDER BY
	CODE_ID;
               ''')
ADdata = cursor.fetchall()
## 关闭数据库连接
conn.close
#endregion

#region 导出结果
ADNewdata=""
for i in ADdata:
    ADNewdata += f"{i[0]}\t{i[1]}\t{i[2]}\t{i[0]}\n"
#endregion

#region 删除原生ICAO_Airports.txt 中 的国内机场
##列出要删除的机场ICAO前两个字符
ZBBB_FIR_CODE = ["ZB", "ZG", "ZH", "ZJ", "ZL", "ZP", "ZS", "ZU", "ZW", "ZY"]
##打开文件以读取和写入
with open("icao.txt", "r+", errors='ignore') as file:
    lines = file.readlines()
    file.seek(0)
    for line in lines:
        if not any(line.startswith(code) for code in ZBBB_FIR_CODE):
            file.write(line)
    file.truncate()
#endregion

#region 删除带有分号的行
##打开ICAO_Airports.txt文件
with open('icao.txt', 'r') as file:
    lines = file.readlines()
##使用列表推导式筛选出不以英文分号开头的行
filtered_lines = (line for line in lines if not line.startswith(';'))
## 打开同一文件以写入筛选后的内容
with open('icao.txt', 'w') as file:
    file.writelines(filtered_lines)
#endregion

#region 将第三列删除，并复制第一列的内容为新的第三列
with open('icao.txt', 'r') as file:
    lines = file.readlines()

new_lines = []
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 4:
        parts.pop()  # 删除最后一个字段，即机场名称
        parts.append(parts[0])  # 将第一个字段（ICAO代码）复制到最后
    new_line = '\t'.join(parts)
    new_lines.append(new_line+'\n')

with open('icao.txt', 'w') as file:
    file.writelines(new_lines)
#endregion

#region 将读取数据库的结果写入ICAO_ZBBB.txt中
with open('icao_ZBBB.txt', 'a+', encoding='gbk') as f:
    f.write(ADNewdata)
#endregion

#region 坐标转换
def convert_coordinates(coord_str, format):
    coord_str = coord_str.rstrip('NE')
    if format == "lat":
        degree = str(coord_str[1:3])
        minute = int(coord_str[3:5])
        seconds = int(coord_str[5:])
    else:
        degree = str(coord_str[1:4])
        minute = int(coord_str[4:6])
        seconds = int(coord_str[6:])
    minute_in_degrees = minute / 60
    seconds_in_degrees = seconds / 3600
    degrees_in_decimal = float(degree) + minute_in_degrees + seconds_in_degrees

    return f"{degrees_in_decimal:.7f}"

# 打开原始文件和新文件
with open('icao_ZBBB.txt', 'r') as file:
    lines = file.readlines()

new_lines = []
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 4:
        latitude = convert_coordinates(parts[1], "lat")
        longitude = convert_coordinates(parts[2], "lon")
        parts[1] = latitude
        parts[2] = longitude
    new_line = '\t'.join(parts)
    new_lines.append(new_line)

# 写入新文件
with open(f'icao.txt', 'a+') as file:
    file.writelines([line + '\n' for line in new_lines])
#endregion

#region 写入注释信息
# 打开文件以读取原始内容
with open(f'icao.txt', 'r', encoding='gbk') as file:
    # 读取原始内容
    existing_content = file.read()

# 在首行添加新的注释信息
LOCAL_TIME=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
new_content = f";DATA provided by Aero-Nav & CAAC\n;CYCLE: {AIRAC_CYCLE}\n;Generate Date: {LOCAL_TIME}\n" + existing_content

# 打开文件以覆盖写入新内容
with open(f'icao.txt', 'w') as file:
    # 写入新内容
    file.write(new_content)
#endregion

#region 删除不必要的文件
print(f'{AIRAC_CYCLE}期icao.txt文件生成完毕！')
os.remove('icao_ZBBB.txt')
#endregion