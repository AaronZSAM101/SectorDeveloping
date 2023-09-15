
# 思路：
# （通过CSDT版本导出）
# 1.打开airports.dat文件，删除包含";"的行，再按照首字母进行排序
# 2.将机场ICAO 纬度 经度中间使用\t进行split
# 3.再将第一个split的内容复制到经度之后，以\t进行split
# 4.存储到icao.txt中
# （完全自制导出）
# 1.打开公版airports.dat文件，删除包含";"的行，再按照首字母进行排序
# 2.删除公版中前两位字母为ZB ZG ZH ZJ ZL ZP ZS ZU ZW ZY的行
# 3.读取局方库AD_HP表的CODE_ID,GEO_LAT_ACCURACY,GEO_LONG_ACCURACY
# 4.将局方库的内容转换成airports.dat的格式，并写入公版airpots.dat中
# 5.将机场ICAO 纬度 经度中间使用\t进行split
# 6.再将第一个split的内容复制到经度之后，以\t进行split
# 7.存储到icao.txt中



#region CSDT版本导出
# 0. 定义split
def AIRPORTSsplit(input_string):
    part1 = input_string[0:4]
    part2 = input_string[4:15]
    part3 = input_string[15:]
    return f"{part1}\t{part2}\t{part3}\t{part1}"

# 1. 打开airports.dat文件，删除包含";"的行，再按照首字母进行排序
airportsdat_address=input('File Address:')
with open(airportsdat_address, "r") as file:
    lines = file.readlines()
    lines = [line for line in lines if ";" not in line]
    sorted_lines = sorted(lines)
sorted_content = '\n'.join(sorted_lines)
output_string = sorted_content

# 2. 将文本进行split
airportsdatoriginal = output_string
result = AIRPORTSsplit(airportsdatoriginal)

# 3. 将结果存储到icao.txt中
with open("icao.txt", "w") as output_file:
    for line in result:
        output_file.write(line + "\n")

print("操作已完成并已保存到icao.txt中")
#endregion