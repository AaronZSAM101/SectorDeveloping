# 坐标转换
## 定义ES格式切片
def convert_coordinates(coord_str, format):
    if format == "lat":
        degree = int(coord_str[:2])
        minute = int(coord_str[2:4])
        seconds = float(coord_str[4:])
    else:
        degree = int(coord_str[:3])
        minute = int(coord_str[3:5])
        seconds = float(coord_str[5:])
    return f"{degree:03d}.{minute:02d}.{seconds:06.3f}"
## 切片后数据拼合
input_filename = "AD.txt"
output_filename = "ADoutput.txt"
with open(input_filename, "r", encoding='utf-8') as input_file, open(output_filename, "w", encoding='utf-8') as output_file:
    for line in input_file:
        parts = line.split()
        converted_parts = []
        for part in parts:
            try:
                if part.startswith("N"):
                    converted_part = convert_coordinates(part[1:], "lat")
                    converted_parts.append(part[0] + converted_part)
                elif part.startswith("E"):
                    converted_part = convert_coordinates(part[1:], "lon")
                    converted_parts.append(part[0] + converted_part)
                else:
                    converted_parts.append(part)
            except Exception as e:
                print(e, part)

        output_line = ' '.join(converted_parts)
        output_file.write(output_line + "\n")