# 将表RWY的AD_HP_ID与表AD_HP中的AD_HP_ID进行对应，再获取其CODE_ID、TXT_NAME
# 将表RWY的RWY_ID与表RWY_DIRECTION的RWY_ID进行对应，再获取其TXT_DESIG、VAL_MAG_BRG、GEO_LAT、GEO_LONG
# 拼合所有的项目
# 将转换好的数据写入rwy.txt


# 成品
import sqlite3

# 打开数据库连接
DATABASEadress = input("Database Adress:")
conn = sqlite3.connect(DATABASEadress)
cursor = conn.cursor()

# 读取表AD_HP的AD_HP_ID、CODE_ID、TXT_NAME
cursor.execute('SELECT AD_HP_ID, CODE_ID, TXT_NAME FROM AD_HP')
ad_hp_data = cursor.fetchall()

# 读取表RWY的RWY_ID、AD_HP_ID、CODE_AIRPORT
cursor.execute('SELECT RWY_ID, AD_HP_ID, CODE_AIRPORT FROM RWY')
rwy_data = cursor.fetchall()

# 读取表RWY_DIRECTION的RWY_ID、TXT_DESIG、VAL_MAG_BRG、GEO_LAT、GEO_LONG
cursor.execute('SELECT RWY_ID, TXT_DESIG, VAL_MAG_BRG, GEO_LAT, GEO_LONG FROM RWY_DIRECTION')
rwy_direction_data = cursor.fetchall()

# 关闭数据库连接
conn.close()

# 拼合跑道数据


# 将输出写入txt文件
with open('output.txt', 'w') as f:
    f.write("AD_HP数据：\n")
    for ad_hp in ad_hp_data:
        f.write(str(ad_hp) + '\n')

    f.write("\nRWY数据：\n")
    for rwy in rwy_data:
        f.write(str(rwy) + '\n')

    f.write("\nRWY_DIRECTION数据：\n")
    for rwy_direction in rwy_direction_data:
        f.write(str(rwy_direction) + '\n')

print("输出已写入output.txt文件中")