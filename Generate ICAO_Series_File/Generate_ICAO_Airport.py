import sqlite3
import os
import time
#region 从数据库读取数据
## 打开数据库连接
AIRAC_CYCLE = input('当前周期号:')
DATABASEaddress = input("Database Address:")
conn = sqlite3.connect(DATABASEaddress)
cursor = conn.cursor()
## 读取相关数据
cursor.execute('''SELECT CODE_ID, TXT_NAME FROM AD_HP 
               WHERE NOT(CODE_TYPE_MIL_OPS = 'MA' OR CODE_ID = 'VHHH' OR CODE_ID = 'VMMC')
               ORDER BY CODE_ID;
               ''')
ADdata = cursor.fetchall()
## 关闭数据库连接
conn.close
#endregion

#region 导出结果
ADNewdata=""
for i in ADdata:
    ADNewdata += f"\n{i[0]}\t{i[1]}\tChina"
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

#region 将读取数据库的结果写入ICAO_Airports.txt中
with open('ICAO_Airports.txt', 'a+', encoding='gbk') as f:
    f.write(ADNewdata)
#endregion

#region 写入注释信息
# 打开文件以读取原始内容
with open('ICAO_Airports.txt', 'r', encoding='gbk') as file:
    # 读取原始内容
    existing_content = file.read()

# 在首行添加新的注释信息
LOCAL_TIME=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
new_content = f";DATA provided by Aero-Nav & CAAC\n;CYCLE: {AIRAC_CYCLE}\n;Generate Date: {LOCAL_TIME}\n" + existing_content

# 打开文件以覆盖写入新内容
with open('ICAO_Airports.txt', 'w') as file:
    # 写入新内容
    file.write(new_content)
#endregion

print('当期ICAO_Airports文件生成完成！')