#region 坐标转换
def convert_coordinates(coord_str, format):
    coord_str = coord_str.rstrip('NE')
    if format == "lat":
        degree = str(coord_str[1:3])
        minute = int(coord_str[3:5])
        seconds = int(coord_str[5:])
    else:
        degree = str(coord_str[1:4])
        minute = int(coord_str[4:6])
        seconds = int(coord_str[6:])
    minute_in_degrees = minute / 60
    seconds_in_degrees = seconds / 3600
    degrees_in_decimal = float(degree) + minute_in_degrees + seconds_in_degrees

    return f"{degrees_in_decimal:.7f}"

# 打开原始文件和新文件
with open('icao_ZBBB.txt', 'r') as file:
    lines = file.readlines()

new_lines = []
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) == 4:
        latitude = convert_coordinates(parts[1], "lat")
        longitude = convert_coordinates(parts[2], "lon")
        parts[1] = latitude
        parts[2] = longitude
    new_line = '\t'.join(parts)
    new_lines.append(new_line)

# 写入新文件
with open(f'icao.txt', 'a+') as file:
    file.writelines([line + '\n' for line in new_lines])
#endregion