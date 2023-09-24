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

