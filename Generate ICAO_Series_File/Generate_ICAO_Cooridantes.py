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

#region 删除原生icao.txt的国内机场和一些看起来奇奇怪怪的机场以及根本就不是机场/起降点的地方
##列出要删除的机场ICAO前两个字符
ZBBB_FIR_CODE = [
"ZB", "ZG", "ZH", "ZJ", "ZL", "ZP", "ZS", "ZU", "ZW", "ZY",
"ZZ"
]
IGNORE_AERONAV_ARPT = [
"8V", "2W", "6C", "1O", "55", "9K", "6T", "4F", "3T", "02",
"3K", "2L", "4W", "6X", "7I", "5P", "7C", "86", "9O", "48",
"1T", "2O", "03", "9M", "94", "75", "14", "9N", "5K", "0A",
"61", "40", "5X", "62", "6W", "7M", "8F", "5I", "8O", "3I",
"22", "31", "64", "98", "6K", "4A", "7O", "00", "1L", "4M",
"3X", "2A", "33", "88", "19", "90", "93", "3W", "07", "69",
"5V", "4O", "84", "23", "2D", "AA", "4G", "47", "25", "27",
"3F", "5S", "1V", "97", "4V", "5W", "11", "72", "0I", "2S",
"26", "9P", "1A", "0V", "3V", "1C", "79", "68", "1X", "3N",
"76", "95", "56", "83", "8I", "7F", "8K", "6L", "45", "67",
"10", "8X", "80", "1M", "06", "5N", "6F", "2U", "44", "20",
"34", "6N", "0M", "7N", "89", "5F", "78", "7P", "0N", "8A",
"5C", "65", "3G", "21", "42", "4T", "41", "3S", "82", "1G",
"24", "43", "29", "4X", "91", "96", "9V", "58", "9I", "6M",
"36", "0K", "2C", "7G", "13", "4P", "7L", "2N", "5L", "04",
"0F", "09", "5T", "1N", "37", "39", "5O", "28", "6A", "60",
"5A", "99", "0O", "08", "38", "57", "01", "3A", "8T", "5M",
"8C", "6G", "51", "35", "2I", "12", "18", "52", "8N", "9A",
"05", "9C", "92", "9T", "0C", "0G", "49", "2T", "0W", "7T",
"4N", "2K", "8G", "2M", "3P", "7X", "1I", "3M", "77", "8W",
"66", "8P", "2X", "7W", "54", "6I", "9F", "2G", "2F", "6O",
"3O", "1P", "87", "0L", "4K", "1S", "1F", "3L", "1W", "71",
"7A", "6P", "5G", "30", "81", "8M", "0X", "32", "74", "7K",
"53", "73", "0T", "17", "2P", "50", "59", "85", "4I", "15",
"63", "16", "70", "2V", "46"
]
##打开要处理的文件以读取内容
with open('icao.txt', 'r') as file:
    lines = file.readlines()

##列出要删除的前两个字符在IGNORE_AERONAV_ARPT或ZBBB_FIR_CODE中包含的行
lines_to_delete = [line for line in lines if line[:2] in IGNORE_AERONAV_ARPT or line[:2] in ZBBB_FIR_CODE]

##打开同一文件以写入不包含要删除行的内容
with open('icao.txt', 'w') as file:
    file.writelines(line for line in lines if line not in lines_to_delete)
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