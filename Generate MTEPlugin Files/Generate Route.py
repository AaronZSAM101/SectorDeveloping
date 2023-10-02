import sqlite3
import re
import csv
import time
import pandas as pd
import os
import datetime
#region 定义时间
def print_with_timestamp(text):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    result = f'{formatted_datetime} {text}'
    print(result)
#endregion

#region 读取数据
# 读取数据库
AIRAC_CYCLE = input('当前周期号:')
DATABASEadress = input(f'{AIRAC_CYCLE}期数据库地址:')
print_with_timestamp('开始进行处理...')
start_time = time.time() #FOR TEST: 开始计算代码执行时间
conn = sqlite3.connect(DATABASEadress)
cursor = conn.cursor()
cursor.execute('''
SELECT
    name,
    ROUND(MinSafeAltitude * 3.281) AS 'MinSafeAltitude',
    "RESTRICT",
    TRANS_ALT,
    StartAirportID,
    EndAirportID,
    END_CITY
FROM
    FLIGHT_AIRLINE
WHERE
    LENGTH(StartAirportID) = 4
    AND NOT (StartAirportID LIKE 'RC%' OR StartAirportID LIKE 'VH%' OR StartAirportID = 'VMMC' OR StartAirportID LIKE 'ZAO%');
''')

query_airline = "SELECT * FROM FLIGHT_AIRLINE"
# 从数据库中读取FLIGHT_AIRLINE表的数据
query_airline = "SELECT * FROM FLIGHT_AIRLINE"
df_airline = pd.read_sql_query(query_airline, conn)
# 从数据库中读取FLIGHT_AIRLINE_POINT表的数据
query_airline_point = "SELECT * FROM FLIGHT_AIRLINE_POINT"
df_airline_point = pd.read_sql_query(query_airline_point, conn)
# 导出数据到CSV文件，使用GBK编码
df_airline.to_csv(('FLIGHT_AIRLINE.csv'), index=False, encoding='gbk')
df_airline_point.to_csv(('FLIGHT_AIRLINE_POINT.csv'), index=False, encoding='gbk')
#endregion

print_with_timestamp('数据库读取完成，正在进行AltList和TransAlt的处理...')

#region 处理查询结果并将数字进行正则表达式替换
RTEData = []
for row in cursor.fetchall():
    name, min_safe_altitude, restrict, trans_alt, start_airport_id, end_airport_id, end_city = row

    # 处理 Trans_Alt 列
    if '-' not in trans_alt:
        trans_alt = re.sub(r'(\d+)(?=/|$)', r'S\1', trans_alt) # 对于不带短杠的文本，在所有的数字文本前加上S
    else:
        first_part = re.split(r'-', trans_alt)[0] # 对于带短杠的文本，提取第一个短横杠前的文本
        # 用正则获取所有数字组，逐个格式化（即在数字文本前加上S） 
        numbers = re.findall(r'\d+', first_part)
        for number in numbers:
            formatted_number = 'S' + number
            first_part = first_part.replace(number, formatted_number, 1)
        # 替换原始 trans_alt 为处理后的 first_part
        trans_alt = first_part

        # 删除：上升地段 夏 *
    trans_alt = trans_alt.replace('上升地段', '')
    trans_alt = trans_alt.replace('目视', '')
    trans_alt = trans_alt.replace('夏', '')
    if '*' in trans_alt:
        trans_alt = ''
        # 删除第一个 "S" 前的所有内容
    trans_alt = re.sub(r'^.*?S', 'S', trans_alt)
        # 替换 目视06以下 03(含)以下
    trans_alt = trans_alt.replace('06以下', 'S06')
    trans_alt = trans_alt.replace('03(含)以下', 'S03')

    # 处理Arr列
    if len(end_airport_id) == 5:
        arr_value = end_city
    else:
        arr_value = end_airport_id

    RTEData.append(
        {
        'Dep': start_airport_id,    
        'Arr': arr_value, 
        'Name': name, 
        'EvenOdd': '',
        'AltList': trans_alt,
        'MinAlt': min_safe_altitude,
        'Route': '',
        'Remarks': restrict,
        }
    )

print_with_timestamp('AltList和TransAlt处理完成，正在将查询结果写入Route.csv中...')

with open(('Route.csv'), 'w', newline='', encoding='utf-8') as csvfile: # 创建一个新的csv文件并写入刚才的查询结果
    fieldnames = ['Dep', 'Arr', 'Name', 'EvenOdd', 'AltList', 'MinAlt', 'Route', 'Remarks']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for FilledData in RTEData:
        writer.writerow(
            {
                'Dep': FilledData['Dep'],
                'Arr': FilledData['Arr'],
                'Name': FilledData['Name'],
                'EvenOdd': '',
                'AltList': FilledData['AltList'],
                'MinAlt': FilledData['MinAlt'],
                'Route': '',
                'Remarks': FilledData['Remarks'],
            }
        )
conn.close() # 关闭数据库连接
#endregion

print_with_timestamp('查询结果已写入Route.csv，正在处理Route列数据...')

#region 处理航路文件
# 打开CSDT航路文件进行处理
with open((f'{AIRAC_CYCLE}.txt'), 'r', encoding='utf-8') as file:
    lines = file.readlines()
# 打开原始的Route.csv文件以读取内容
with open(('Route.csv'), 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    route_data = list(reader)
# 创建一个字典，以Route.csv文件的Name列为键，航路文件的第二列为值
name_to_route = {row['Name']: '' for row in route_data}
# 处理每一行并将其填充到Route.csv中
for line in lines:
    parts = line.replace(';', '\t').strip().split('\t') # 将分号替换为制表符，并按制表符分割行
    if len(parts) >= 2: # 确保行至少包含两列
        name_from_txt = parts[0] # 提取第一个列的值
        route_from_txt = parts[1] # 提取第二个列的值（对应Route列）
        if name_from_txt in name_to_route: # 检查Route.csv中是否存在匹配的Name
            name_to_route[name_from_txt] = route_from_txt
# 更新Route.csv中的Route列
for row in route_data:
    name = row['Name']
    if name in name_to_route:
        row['Route'] = name_to_route[name]
# 在填充完成后，处理Arr列小于5个字符的行所对应的Route
for row in route_data:
    arr_value = row['Arr']
    if len(arr_value) < 5:
        # 找到Route列中最后一个空格的位置
        last_space_index = row['Route'].rfind(' ')
        if last_space_index != -1:
            # 删除最后一个空格后的内容
            row['Route'] = row['Route'][:last_space_index]
#endregion

print_with_timestamp('Route列数据处理完成，正在将城市名与机场ICAO进行对应...')

#region 将中文的城市地名替换为机场名
# 读取CityMatching.csv文件并创建城市到机场ICAO的映射字典
city_mapping = {}
with open(('CityMatching.csv'), 'r', newline='', encoding='utf-8') as city_file:
    city_reader = csv.reader(city_file)
    for row in city_reader:
        city_names = row[0].split(',')  # 分割逗号分隔的城市名称
        icao = row[1]
        for city_name in city_names:
            city_mapping[city_name.strip()] = icao.strip()

# 处理Route.csv文件中的Arr列
with open(('Route.csv'), 'r', newline='', encoding='utf-8') as route_file:
    reader = csv.DictReader(route_file)
    route_data = list(reader)
for row in route_data:
    arr_value = row['Arr']
    arr_cities = arr_value.split(',')  # 分割逗号分隔的城市名称
    new_arr_values = []
    for city_name in arr_cities:
        city_name = city_name.strip()  # 去除前后空格
        if city_name in city_mapping:
            new_arr_values.append(city_mapping[city_name])
        else:
            new_arr_values.append(city_name)  # 如果找不到匹配，保留原始城市名称
    row['Arr'] = '/'.join(new_arr_values)  # 用新的Arr值更新数据

# 处理航路文件并更新Route列
with open((f'{AIRAC_CYCLE}.txt'), 'r', encoding='utf-8') as file:
    lines = file.readlines()
for row in route_data:
    name = row['Name']
    for line in lines:
        if name in line:
            parts = line.replace(';', '\t').strip().split('\t')
            if len(parts) >= 2:
                route_from_txt = parts[1].strip()  # 提取航路信息
                row['Route'] = route_from_txt  # 更新Route列

# 将更新后的数据写回Route.csv文件，更新Arr和Route列
with open(('Route.csv'), 'w', newline='', encoding='gbk') as csvfile:
    fieldnames = ['Dep', 'Arr', 'Name', 'EvenOdd', 'AltList', 'MinAlt', 'Route', 'Remarks']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(route_data)
#endregion

print_with_timestamp(f'所有数据均已填充到{AIRAC_CYCLE}期Route.csv文件中！')

#FOR TEST: 结束计算代码执行时间
end_time = time.time()
execution_time = end_time - start_time
input(f'{AIRAC_CYCLE}期MTEP航路检查数据生成完毕！总用时{execution_time:.2f}秒.')