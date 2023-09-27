import sqlite3
import re
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
    ROUND(MinSafeAltitude * 3.281,0) AS 'MinSafeAltitude',
    "RESTRICT",
    TRANS_ALT
FROM
    FLIGHT_AIRLINE
WHERE
    LENGTH(StartAirportID) = 4
    AND NOT (StartAirportID LIKE 'RC%' OR StartAirportID LIKE 'VH%' OR StartAirportID = 'VMMC' OR StartAirportID LIKE 'ZAO%');
''')
# 处理查询结果并进行正则表达式替换
RTEData = []
for row in cursor.fetchall():
    name, min_safe_altitude, restrict, trans_alt = row
    # 使用正则表达式进行替换
    trans_alt = re.sub(r'(\d{2})(?=/|$)', r'S\1', trans_alt)
    RTEData.append((name, min_safe_altitude, restrict, trans_alt))
# 关闭数据库连接
conn.close()
#endregion

#region 导出数据
RTENewdata = ''
for i in RTEData:
    RTENewdata += f",,{i[0]},,{i[3]},{i[1]},,{i[2]}\n"
print(RTENewdata)
#endregion