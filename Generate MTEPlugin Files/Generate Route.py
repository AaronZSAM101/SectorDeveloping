import sqlite3
import time
##读取数据库
AIRAC_CYCLE = input('当前周期号:')
DATABASEadress = input(f'{AIRAC_CYCLE}期数据库地址:')
#FOR TEST: 开始计算代码执行时间
start_time = time.time()
conn = sqlite3.connect(DATABASEadress)
cursor = conn.cursor()
#region 旧方法
# cursor.execute=('''SELECT
# 	name,
# 	round( MinSafeAltitude * 3.281 ) AS 'MinSafeAltitude',
# 	"RESTRICT",
# 	TRANS_ALT 
# FROM
# 	FLIGHT_AIRLINE 
# WHERE
# 	NOT (
# 		StartAirportID = 'AGAVO' 
# 		OR StartAirportID = 'APITO' 
# 		OR StartAirportID = 'ASSAD' 
# 		OR StartAirportID = 'BEKOL' 
# 		OR StartAirportID = 'BISUN' 
# 		OR StartAirportID = 'BUNTA' 
# 		OR StartAirportID = 'GOLOT' 
# 		OR StartAirportID = 'GOPTO' 
# 		OR StartAirportID = 'INTIK' 
# 		OR StartAirportID = 'KAMUD' 
# 		OR StartAirportID = 'KATBO' 
# 		OR StartAirportID = 'LAMEN' 
# 		OR StartAirportID = 'LANDA'
# 		OR StartAirportID = 'LINSO' 
# 		OR StartAirportID = 'MAGIT' 
# 		OR StartAirportID = 'MAGOG' 
# 		OR StartAirportID = 'MORIT' 
# 		OR StartAirportID = 'NIXAL' 
# 		OR StartAirportID = 'NONIM' 
# 		OR StartAirportID = 'POLHO' 
# 		OR StartAirportID = 'PURPA' 
# 		OR StartAirportID = 'RCBS' 
# 		OR StartAirportID = 'RCFN'
# 		OR StartAirportID = 'RCQC'
# 		OR StartAirportID = 'RCKH' 
# 		OR StartAirportID = 'RCMQ' 
# 		OR StartAirportID = 'RCNN' 
# 		OR StartAirportID = 'RCSS' 
# 		OR StartAirportID = 'RCTP' 
# 		OR StartAirportID = 'RCYU' 
# 		OR StartAirportID = 'RULAD' 
# 		OR StartAirportID = 'SAGAG' 
# 		OR StartAirportID = 'SARIN' 
# 		OR StartAirportID = 'SARUL' 
# 		OR StartAirportID = 'SIKOU' 
# 		OR StartAirportID = 'SIMLI' 
# 		OR StartAirportID = 'TAMOT'
# 		OR StartAirportID = 'TEBAK' 
# 		OR StartAirportID = 'TEBUS' 
# 		OR StartAirportID = 'TELOK' 
# 		OR StartAirportID = 'TOMUK' 
# 		OR StartAirportID = 'VHHH' 
# 		OR StartAirportID = 'VMMC' 
# 		OR StartAirportID = 'ZAO'
# 	)
# ''')
#endregion

#region新方法
cursor.execute=('''
SELECT
    name,
    ROUND(MinSafeAltitude * 3.281) AS 'MinSafeAltitude',
    "RESTRICT",
    TRANS_ALT
FROM
    FLIGHT_AIRLINE
WHERE
    LENGTH(StartAirportID) = 4
    AND not (StartAirportID LIKE 'RC%' OR StartAirportID LIKE 'VH%' or StartAirportID LIKE 'VM%' OR StartAirportID  = 'ZAO');
''')
RTEdata = cursor.fetchall()
conn.close
#endregion

#region 导出数据
RTENewdata = ''
for i in RTEdata:
    RTENewdata += f",,{i[0]},,{i[3]},{i[1]},,{i[2]}\n"
print(RTENewdata)
#endregion