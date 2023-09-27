import sqlite3
import re
import csv
import time
#region 读取数据
##读取数据库
AIRAC_CYCLE = input('当前周期号:')
DATABASEadress = input(f'{AIRAC_CYCLE}期数据库地址:')
#FOR TEST: 开始计算代码执行时间
start_time = time.time()
conn = sqlite3.connect(DATABASEadress)
cursor = conn.cursor()
# 执行查询
cursor.execute('''
SELECT
    name,
    ROUND(MinSafeAltitude * 3.281) AS 'MinSafeAltitude',
    "RESTRICT",
    TRANS_ALT,
    StartAirportID,
    EndAirportID
FROM
    FLIGHT_AIRLINE
WHERE
    LENGTH(StartAirportID) = 4
    AND NOT (StartAirportID LIKE 'RC%' OR StartAirportID LIKE 'VH%' OR StartAirportID = 'VMMC' OR StartAirportID LIKE 'ZAO%');
''')
# 处理查询结果并进行正则表达式替换
RTEData = []
for row in cursor.fetchall():
    name, min_safe_altitude, restrict, trans_alt, start_airport_id, end_airport_id = row
    # 将纯数字的行，数字前批量加上'S‘
    trans_alt = re.sub(r'(\d{2})(?=/|$)', r'S\1', trans_alt)
    
    # 如果 AltList 列包含中文字符或者星号，将其替换为空字符串
    if re.match(r'^[\u4e00-\u9fa5]+$', trans_alt) or '*' in trans_alt:
        trans_alt = ''
    else:
        # 否则，仅保留中文后的两个数字并在前加上 'S'
        chinese_numbers_match = re.search(r'[^\d]*(\d{2})[^\d]*', trans_alt)
        if chinese_numbers_match:
            trans_alt = 'S' + chinese_numbers_match.group(1)
    
    RTEData.append((name, min_safe_altitude, restrict, trans_alt, start_airport_id, end_airport_id))
#endregion

#region 创建一个新的csv文件并写入刚才的查询结果
with open('Route.csv', 'w', newline='') as csvfile:
    fieldnames = ['Dep', 'Arr', 'Name', 'EvenOdd', 'AltList', 'MinAlt', 'Route', 'Remarks']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for FilledData in RTEData:
        writer.writerow(
        {'Dep': FilledData[4],
        'Arr': FilledData[5],
        'Name': FilledData[0],
        'EvenOdd': '',
        'AltList': FilledData[3],
        'MinAlt': FilledData[1],
        'Route': '',
        'Remarks': FilledData[2]
    }
    )
# 关闭数据库连接
conn.close()
#endregion

#region 处理CSDT导出的航路文件
# 打开名为2309.txt的文件进行处理
with open(f'{AIRAC_CYCLE}.txt', 'r', encoding='gbk') as file:
    lines = file.readlines()
# 打开原始的Route.csv文件以读取内容
with open('Route.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    route_data = list(reader)
# 创建一个字典，以Route.csv文件的Name列为键，2309.txt文件的第二列为值
name_to_route = {row['Name']: '' for row in route_data}
# 处理每一行并将其填充到Route.csv中
for line in lines:
    # 将分号替换为制表符，并按制表符分割行
    parts = line.replace(';', '\t').strip().split('\t')
    
    # 确保行至少包含两列
    if len(parts) >= 2:
        # 提取第一个列的值
        name_from_txt = parts[0]
        
        # 提取第二个列的值（对应Route列）
        route_from_txt = parts[1]
        
        # 检查Route.csv中是否存在匹配的Name
        if name_from_txt in name_to_route:
            name_to_route[name_from_txt] = route_from_txt
# 更新Route.csv中的Route列
for row in route_data:
    name = row['Name']
    if name in name_to_route:
        row['Route'] = name_to_route[name]
# 在填充完成后，处理Arr列小于5个字符的行
for row in route_data:
    arr_value = row['Arr']
    if len(arr_value) < 5:
        # 找到Route列中最后一个空格的位置
        last_space_index = row['Route'].rfind(' ')
        if last_space_index != -1:
            # 删除最后一个空格后的内容
            row['Route'] = row['Route'][:last_space_index]
#endregion

#region 写回合并后的数据到Route.csv文件中
with open('Route.csv', 'w', newline='') as csvfile:
    fieldnames = ['Dep', 'Arr', 'Name', 'EvenOdd', 'AltList', 'MinAlt', 'Route', 'Remarks']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(route_data)
#endregion

#FOR TEST: 结束计算代码执行时间
end_time = time.time()
execution_time = end_time - start_time

input(f'{AIRAC_CYCLE}期扇区数据生成完毕，总用时{execution_time:.2f}秒.')