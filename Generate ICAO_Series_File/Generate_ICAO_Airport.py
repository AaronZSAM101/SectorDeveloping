import sqlite3
import os
#region 从数据库读取数据
## 打开数据库连接
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
# 列出要删除的前两个字符
ZBBB_FIR_CODE = ["ZB", "ZG", "ZH", "ZJ", "ZL", "ZP", "ZS", "ZU", "ZW", "ZY"]

# 打开文件以读取和写入
with open("D:\ProgramData\Projects\SectorDeveloping\Generate ICAO_Series_File\ICAO_Airports.txt", "r+", encoding='gbk') as file:
    # 读取文件的所有行
    lines = file.readlines()

    # 将文件指针移到文件开头
    file.seek(0)

    # 遍历每一行
    for line in lines:
        # 检查前两个字符是否在要删除的列表中
        if not any(line.startswith(code) for code in ZBBB_FIR_CODE):
            # 如果不在列表中，则将该行写入文件
            file.write(line)

    # 截断文件，以删除未使用的内容
    file.truncate()
#endregion

#region 将读取数据库的结果写入ICAO_Airports_2309.txt中
with open('D:\ProgramData\Projects\SectorDeveloping\Generate ICAO_Series_File\ICAO_Airports.txt', 'a+', encoding='gbk') as f:
    f.write(ADNewdata)
#endregion
print('当期ICAO_Airports文件生成完成！')