#region 删除带分号的行
with open('ICAO_Airlines.txt', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
filtered_lines = (line for line in lines if not line.startswith(';'))
with open('ICAO_Airlines.txt', 'w', encoding='utf-8', errors='ignore') as f:
    f.writelines(filtered_lines)
#endregion

#region 删除CHINA航司
with open("ICAO_Airlines.txt", "r", encoding='utf-8', errors='ignore') as file:
    lines = file.readlines()

new_lines = []

for line in lines:
    if "CHINA" in line:
        parts = line.split("\t", 3) 
        if len(parts) >= 4:
            new_line = "\t".join(parts[:3]) + "\n"
            new_lines.append(new_line)
    else:
        new_lines.append(line)

with open("ICAO_Airlines.txt", "w", encoding='utf-8', errors='ignore') as file:
    file.writelines(new_lines)
#endregion

#region 写入自主维护的CHINA航司
with open('China_Callsign.txt', 'r', encoding='utf-8', errors='ignore') as f:
    CHINA_CALLSIGN = f.readlines()
with open('ICAO_Airlines.txt', 'a', encoding='gbk', errors='ignore') as f:
    f.writelines(CHINA_CALLSIGN)
#endregion


print('中国呼号生成完毕')