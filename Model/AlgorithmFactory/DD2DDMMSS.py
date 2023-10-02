def decimal_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = (decimal_degrees - degrees - minutes / 60) * 3600
    return degrees, minutes, seconds

def dms_format(degrees, minutes, seconds):
    return f"{degrees} {minutes} {seconds:.2f}"

def convert_decimal_to_dms(coordinate):
    if coordinate < 0:
        direction = "S" if coordinate < 0 else "W"
        coordinate = abs(coordinate)
    else:
        direction = "N" if coordinate > 0 else "E"
    degrees, minutes, seconds = decimal_to_dms(coordinate)
    formatted_coord = dms_format(degrees, minutes, seconds)
    return f"{formatted_coord} {direction}"

# 从文件中读取经度和纬度，以逗号分隔
input_filename = "600米.txt"  # 替换成你的输入文件名
output_filename = "output_coordinates.txt"  # 替换成你的输出文件名

with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
    for line in input_file:
        coordinates = line.strip().split(',')
        if len(coordinates) == 2:
            longitude, latitude = map(float, coordinates)
            dms_longitude = convert_decimal_to_dms(longitude)
            dms_latitude = convert_decimal_to_dms(latitude)
            output_file.write(f"{dms_latitude} {dms_longitude}\n")

print(f"转换完成，结果保存在 {output_filename}")