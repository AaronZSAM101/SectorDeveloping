import sqlite3
#region 读取数据库中的中国大陆机场
## 打开数据库连接
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
    ADNewdata += f"\n{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}"
#endregion

#region 删除原生ICAO_Airports.txt 中 的国内机场
# 列出要删除的机场ICAO前两个字符
ZBBB_FIR_CODE = ["ZB", "ZG", "ZH", "ZJ", "ZL", "ZP", "ZS", "ZU", "ZW", "ZY"]

# 打开文件以读取和写入
with open("ICAO_Airports.txt", "r+", errors='ignore') as file:
    lines = file.readlines()
    file.seek(0)
    for line in lines:
        if not any(line.startswith(code) for code in ZBBB_FIR_CODE):
            file.write(line)
    file.truncate()
#endregion

#region 删除带有分号的行
# 打开ICAO_Airports.txt文件
with open('ICAO_Airports.txt', 'r') as file:
    lines = file.readlines()

# 使用列表推导式筛选出不以英文分号开头的行
filtered_lines = (line for line in lines if not line.startswith(';'))

# 打开同一文件以写入筛选后的内容
with open('ICAO_Airports.txt', 'w') as file:
    file.writelines(filtered_lines)
#endregion

#region 坐标转换

#endregion